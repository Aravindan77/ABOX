const hre = require("hardhat");

async function main() {
    console.log("🚀 Deploying BountyVault contract...\n");

    const [deployer] = await hre.ethers.getSigners();
    console.log("📝 Deploying with account:", deployer.address);

    // Get account balance
    const balance = await hre.ethers.provider.getBalance(deployer.address);
    console.log("💰 Account balance:", hre.ethers.formatEther(balance), "MATIC\n");

    // Deploy BountyVault
    console.log("⏳ Deploying BountyVault...");
    const BountyVault = await hre.ethers.getContractFactory("BountyVault");
    const vault = await BountyVault.deploy();

    await vault.waitForDeployment();
    const vaultAddress = await vault.getAddress();

    console.log("✅ BountyVault deployed to:", vaultAddress);

    // Grant roles
    console.log("\n🔐 Configuring roles...");

    const AI_ORACLE_ROLE = await vault.AI_ORACLE_ROLE();
    const VALIDATOR_ROLE = await vault.VALIDATOR_ROLE();

    // Grant AI Oracle role to backend wallet
    const backendWallet = process.env.BACKEND_WALLET;
    if (backendWallet) {
        console.log("   Granting AI_ORACLE_ROLE to:", backendWallet);
        await vault.grantRole(AI_ORACLE_ROLE, backendWallet);
    }

    // Grant Validator role to deployer (for testing)
    console.log("   Granting VALIDATOR_ROLE to:", deployer.address);
    await vault.grantRole(VALIDATOR_ROLE, deployer.address);

    console.log("\n✅ Deployment complete!");
    console.log("\n📋 Contract Details:");
    console.log("   Address:", vaultAddress);
    console.log("   Network:", hre.network.name);
    console.log("   Deployer:", deployer.address);

    console.log("\n🔍 Verify contract with:");
    console.log(`   npx hardhat verify --network ${hre.network.name} ${vaultAddress}`);

    // Save deployment info
    const fs = require('fs');
    const deploymentInfo = {
        network: hre.network.name,
        contractAddress: vaultAddress,
        deployer: deployer.address,
        timestamp: new Date().toISOString(),
        blockNumber: await hre.ethers.provider.getBlockNumber()
    };

    fs.writeFileSync(
        `./deployments/${hre.network.name}-deployment.json`,
        JSON.stringify(deploymentInfo, null, 2)
    );

    console.log(`\n💾 Deployment info saved to ./deployments/${hre.network.name}-deployment.json`);
}

main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error("❌ Deployment failed:", error);
        process.exit(1);
    });
