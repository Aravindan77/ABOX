// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/security/Pausable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";

/**
 * @title BountyVault
 * @notice Anti-Gravity Bug Bounty Platform - Smart Contract Vault
 * @dev Manages bounty funds with AI-driven auto-release mechanism
 * 
 * Core Features:
 * 1. Escrow bounty funds for projects
 * 2. Auto-release payments when AI/Validator approves bugs
 * 3. Multi-signature validation for high-value payouts
 * 4. Emergency pause mechanism
 */
contract BountyVault is AccessControl, ReentrancyGuard, Pausable {
    using SafeERC20 for IERC20;

    // ============ Roles ============
    bytes32 public constant VALIDATOR_ROLE = keccak256("VALIDATOR_ROLE");
    bytes32 public constant AI_ORACLE_ROLE = keccak256("AI_ORACLE_ROLE");
    bytes32 public constant PROJECT_OWNER_ROLE = keccak256("PROJECT_OWNER_ROLE");
    bytes32 public constant EMERGENCY_ROLE = keccak256("EMERGENCY_ROLE");

    // ============ Structs ============
    
    struct Project {
        address owner;
        uint256 totalDeposited;
        uint256 availableBalance;
        uint256 totalPaid;
        bool isActive;
        mapping(address => bool) authorizedTokens;
    }

    struct BugReport {
        bytes32 bugId;
        bytes32 projectId;
        address researcher;
        uint256 bountyAmount;
        address tokenAddress; // address(0) for native MATIC
        BugStatus status;
        uint256 aiConfidence; // 0-100
        uint256 cvssScore; // 0-100 (scaled from 0-10)
        uint256 submittedAt;
        uint256 validatedAt;
        address validator;
        bool requiresMultiSig;
        uint8 approvalCount;
    }

    enum BugStatus {
        Pending,
        AIValidated,
        HumanReview,
        Approved,
        Rejected,
        Paid,
        Disputed
    }

    // ============ State Variables ============
    
    mapping(bytes32 => Project) public projects;
    mapping(bytes32 => BugReport) public bugReports;
    mapping(bytes32 => mapping(address => bool)) public multiSigApprovals;
    
    uint256 public constant AI_CONFIDENCE_THRESHOLD = 85; // 85% confidence for auto-release
    uint256 public constant HIGH_VALUE_THRESHOLD = 1000 * 10**18; // 1000 MATIC requires multi-sig
    uint256 public constant REQUIRED_APPROVALS = 2;
    
    uint256 public totalProjectsCreated;
    uint256 public totalBugsSubmitted;
    uint256 public totalBountiesPaid;

    // ============ Events ============
    
    event ProjectCreated(bytes32 indexed projectId, address indexed owner, uint256 timestamp);
    event FundsDeposited(bytes32 indexed projectId, address indexed token, uint256 amount);
    event BugSubmitted(bytes32 indexed bugId, bytes32 indexed projectId, address indexed researcher);
    event AIValidation(bytes32 indexed bugId, uint256 aiConfidence, uint256 cvssScore);
    event BugApproved(bytes32 indexed bugId, address indexed validator);
    event BountyPaid(bytes32 indexed bugId, address indexed researcher, uint256 amount, address token);
    event BugRejected(bytes32 indexed bugId, string reason);
    event MultiSigApproval(bytes32 indexed bugId, address indexed validator, uint8 approvalCount);
    event EmergencyWithdraw(bytes32 indexed projectId, address indexed owner, uint256 amount);

    // ============ Modifiers ============
    
    modifier onlyProjectOwner(bytes32 projectId) {
        require(projects[projectId].owner == msg.sender, "Not project owner");
        _;
    }

    modifier projectExists(bytes32 projectId) {
        require(projects[projectId].owner != address(0), "Project does not exist");
        _;
    }

    modifier bugExists(bytes32 bugId) {
        require(bugReports[bugId].researcher != address(0), "Bug does not exist");
        _;
    }

    // ============ Constructor ============
    
    constructor() {
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(EMERGENCY_ROLE, msg.sender);
    }

    // ============ Project Management ============
    
    /**
     * @notice Create a new bug bounty project
     * @param projectId Unique identifier for the project
     */
    function createProject(bytes32 projectId) external whenNotPaused {
        require(projects[projectId].owner == address(0), "Project already exists");
        
        Project storage project = projects[projectId];
        project.owner = msg.sender;
        project.isActive = true;
        
        totalProjectsCreated++;
        
        emit ProjectCreated(projectId, msg.sender, block.timestamp);
    }

    /**
     * @notice Deposit funds into project vault (native MATIC)
     * @param projectId Project to fund
     */
    function depositFunds(bytes32 projectId) 
        external 
        payable 
        projectExists(projectId) 
        whenNotPaused 
    {
        require(msg.value > 0, "Must deposit funds");
        
        Project storage project = projects[projectId];
        project.totalDeposited += msg.value;
        project.availableBalance += msg.value;
        
        emit FundsDeposited(projectId, address(0), msg.value);
    }

    /**
     * @notice Deposit ERC20 tokens into project vault
     * @param projectId Project to fund
     * @param token ERC20 token address
     * @param amount Amount to deposit
     */
    function depositTokens(bytes32 projectId, address token, uint256 amount)
        external
        projectExists(projectId)
        whenNotPaused
    {
        require(amount > 0, "Must deposit tokens");
        require(token != address(0), "Invalid token address");
        
        Project storage project = projects[projectId];
        project.authorizedTokens[token] = true;
        
        IERC20(token).safeTransferFrom(msg.sender, address(this), amount);
        
        project.totalDeposited += amount;
        project.availableBalance += amount;
        
        emit FundsDeposited(projectId, token, amount);
    }

    // ============ Bug Report Submission ============
    
    /**
     * @notice Submit a bug report (called by backend after AI validation)
     * @param bugId Unique bug identifier
     * @param projectId Associated project
     * @param researcher Wallet address of researcher
     * @param bountyAmount Proposed payout amount
     * @param tokenAddress Payment token (address(0) for MATIC)
     * @param aiConfidence AI model confidence (0-100)
     * @param cvssScore CVSS severity score (0-100)
     */
    function submitBug(
        bytes32 bugId,
        bytes32 projectId,
        address researcher,
        uint256 bountyAmount,
        address tokenAddress,
        uint256 aiConfidence,
        uint256 cvssScore
    ) 
        external 
        onlyRole(AI_ORACLE_ROLE)
        projectExists(projectId)
        whenNotPaused
    {
        require(bugReports[bugId].researcher == address(0), "Bug already exists");
        require(researcher != address(0), "Invalid researcher");
        require(bountyAmount > 0, "Invalid bounty amount");
        require(projects[projectId].availableBalance >= bountyAmount, "Insufficient funds");
        
        BugReport storage bug = bugReports[bugId];
        bug.bugId = bugId;
        bug.projectId = projectId;
        bug.researcher = researcher;
        bug.bountyAmount = bountyAmount;
        bug.tokenAddress = tokenAddress;
        bug.aiConfidence = aiConfidence;
        bug.cvssScore = cvssScore;
        bug.submittedAt = block.timestamp;
        bug.status = BugStatus.Pending;
        
        // Determine if multi-sig is required
        bug.requiresMultiSig = bountyAmount >= HIGH_VALUE_THRESHOLD;
        
        totalBugsSubmitted++;
        
        emit BugSubmitted(bugId, projectId, researcher);
        emit AIValidation(bugId, aiConfidence, cvssScore);
        
        // Auto-approve if AI confidence is high and amount is low
        if (aiConfidence >= AI_CONFIDENCE_THRESHOLD && !bug.requiresMultiSig) {
            _autoApproveBug(bugId);
        } else {
            bug.status = BugStatus.HumanReview;
        }
    }

    // ============ Validation & Approval ============
    
    /**
     * @notice Internal auto-approval for high-confidence bugs
     */
    function _autoApproveBug(bytes32 bugId) internal {
        BugReport storage bug = bugReports[bugId];
        bug.status = BugStatus.Approved;
        bug.validatedAt = block.timestamp;
        bug.validator = address(this); // Self-validated
        
        emit BugApproved(bugId, address(this));
        
        // Auto-release payment
        _releaseBounty(bugId);
    }

    /**
     * @notice Manual approval by validator (for human review cases)
     * @param bugId Bug to approve
     */
    function approveBug(bytes32 bugId) 
        external 
        onlyRole(VALIDATOR_ROLE)
        bugExists(bugId)
        whenNotPaused
    {
        BugReport storage bug = bugReports[bugId];
        require(bug.status == BugStatus.HumanReview || bug.status == BugStatus.AIValidated, "Invalid status");
        
        if (bug.requiresMultiSig) {
            require(!multiSigApprovals[bugId][msg.sender], "Already approved");
            
            multiSigApprovals[bugId][msg.sender] = true;
            bug.approvalCount++;
            
            emit MultiSigApproval(bugId, msg.sender, bug.approvalCount);
            
            if (bug.approvalCount >= REQUIRED_APPROVALS) {
                bug.status = BugStatus.Approved;
                bug.validatedAt = block.timestamp;
                bug.validator = msg.sender;
                
                emit BugApproved(bugId, msg.sender);
                _releaseBounty(bugId);
            }
        } else {
            bug.status = BugStatus.Approved;
            bug.validatedAt = block.timestamp;
            bug.validator = msg.sender;
            
            emit BugApproved(bugId, msg.sender);
            _releaseBounty(bugId);
        }
    }

    /**
     * @notice Reject a bug report
     * @param bugId Bug to reject
     * @param reason Rejection reason
     */
    function rejectBug(bytes32 bugId, string calldata reason)
        external
        onlyRole(VALIDATOR_ROLE)
        bugExists(bugId)
        whenNotPaused
    {
        BugReport storage bug = bugReports[bugId];
        require(bug.status != BugStatus.Paid, "Already paid");
        
        bug.status = BugStatus.Rejected;
        
        emit BugRejected(bugId, reason);
    }

    // ============ Payment Release ============
    
    /**
     * @notice Internal function to release bounty payment
     */
    function _releaseBounty(bytes32 bugId) internal nonReentrant {
        BugReport storage bug = bugReports[bugId];
        require(bug.status == BugStatus.Approved, "Not approved");
        
        Project storage project = projects[bug.projectId];
        require(project.availableBalance >= bug.bountyAmount, "Insufficient balance");
        
        project.availableBalance -= bug.bountyAmount;
        project.totalPaid += bug.bountyAmount;
        bug.status = BugStatus.Paid;
        
        // Transfer funds
        if (bug.tokenAddress == address(0)) {
            // Native MATIC transfer
            (bool success, ) = bug.researcher.call{value: bug.bountyAmount}("");
            require(success, "Transfer failed");
        } else {
            // ERC20 transfer
            IERC20(bug.tokenAddress).safeTransfer(bug.researcher, bug.bountyAmount);
        }
        
        totalBountiesPaid += bug.bountyAmount;
        
        emit BountyPaid(bugId, bug.researcher, bug.bountyAmount, bug.tokenAddress);
    }

    // ============ Emergency Functions ============
    
    /**
     * @notice Emergency withdraw for project owners
     * @param projectId Project to withdraw from
     */
    function emergencyWithdraw(bytes32 projectId)
        external
        onlyProjectOwner(projectId)
        whenPaused
    {
        Project storage project = projects[projectId];
        uint256 amount = project.availableBalance;
        require(amount > 0, "No funds to withdraw");
        
        project.availableBalance = 0;
        
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Withdraw failed");
        
        emit EmergencyWithdraw(projectId, msg.sender, amount);
    }

    /**
     * @notice Pause contract (emergency only)
     */
    function pause() external onlyRole(EMERGENCY_ROLE) {
        _pause();
    }

    /**
     * @notice Unpause contract
     */
    function unpause() external onlyRole(EMERGENCY_ROLE) {
        _unpause();
    }

    // ============ View Functions ============
    
    function getProjectBalance(bytes32 projectId) external view returns (uint256) {
        return projects[projectId].availableBalance;
    }

    function getBugStatus(bytes32 bugId) external view returns (BugStatus) {
        return bugReports[bugId].status;
    }

    function getContractStats() external view returns (
        uint256 totalProjects,
        uint256 totalBugs,
        uint256 totalPaid
    ) {
        return (totalProjectsCreated, totalBugsSubmitted, totalBountiesPaid);
    }

    // ============ Receive Function ============
    
    receive() external payable {
        // Allow contract to receive MATIC
    }
}
