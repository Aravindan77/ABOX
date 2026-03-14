# 🚀 Anti-Gravity Bug Bounty Platform

> **Philosophy:** Remove friction and centralization through AI-driven validation, automated payments, and continuous reputation learning.

## 🎯 Core Principles

1. **Self-Validation** - AI auto-triages reports to reduce human overhead
2. **Auto-Release Payments** - Smart contracts eliminate financial friction
3. **Continuous Learning** - Reputation engine reduces trust friction

## 🏗️ Architecture

```
┌─────────────────┐      ┌──────────────────┐      ┌─────────────────┐
│   Next.js UI    │◄────►│  FastAPI Backend │◄────►│  Supabase DB    │
│  (Researchers)  │      │   (AI Engine)    │      │  (PostgreSQL)   │
└─────────────────┘      └──────────────────┘      └─────────────────┘
        │                         │                          
        │                         │                          
        ▼                         ▼                          
┌─────────────────┐      ┌──────────────────┐               
│ Smart Contracts │      │      IPFS        │               
│   (Polygon)     │      │   (Evidence)     │               
└─────────────────┘      └──────────────────┘               
```

## 🛠️ Tech Stack

### Frontend
- **Framework:** Next.js 14 (React, TypeScript)
- **Styling:** TailwindCSS + Shadcn UI
- **Web3:** Ethers.js, Wagmi, RainbowKit
- **Auth:** Wallet-based (MetaMask)

### Backend
- **API:** FastAPI (Python 3.11+)
- **AI/ML:** 
  - HuggingFace Transformers (NLP for triage)
  - Scikit-learn (Scoring & Classification)
- **Storage:** IPFS (Pinata/Web3.Storage)

### Blockchain
- **Smart Contracts:** Solidity 0.8.20+
- **Network:** Polygon (Mumbai Testnet → Mainnet)
- **Tools:** Hardhat, OpenZeppelin

### Database
- **Primary:** Supabase (PostgreSQL)
- **Schemas:** Users, Bugs, Reputation, Transactions

## 📦 Project Structure

```
bug-bounty-platform/
├── frontend/              # Next.js application
│   ├── app/              # App router pages
│   ├── components/       # React components
│   ├── lib/              # Utilities & hooks
│   ├── contracts/        # ABI files
│   └── public/           # Static assets
│
├── backend/              # FastAPI application
│   ├── app/
│   │   ├── api/         # API routes
│   │   ├── ml/          # AI/ML models
│   │   ├── services/    # Business logic
│   │   ├── models/      # Pydantic models
│   │   └── core/        # Config & utilities
│   ├── requirements.txt
│   └── main.py
│
├── contracts/            # Smart contracts
│   ├── contracts/       # Solidity files
│   ├── scripts/         # Deployment scripts
│   ├── test/            # Contract tests
│   └── hardhat.config.js
│
├── database/            # Database schemas
│   └── schema.sql
│
└── docs/               # Documentation
    ├── API.md
    ├── SMART_CONTRACTS.md
    └── DEPLOYMENT.md
```

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.11+
- MetaMask wallet
- Supabase account
- IPFS provider (Pinata/Web3.Storage)

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Smart Contracts
```bash
cd contracts
npm install
npx hardhat compile
npx hardhat test
npx hardhat run scripts/deploy.js --network mumbai
```

## 🎯 Core Features

### 1. AI Auto-Triage
- **OWASP Top 10 Classification** - Maps bug reports to vulnerability categories
- **CVSS Scoring** - Automated severity assessment
- **Spam Detection** - Filters low-quality submissions

### 2. Reputation Engine
- **Trust Score** - Wallet-based reputation (0-100)
- **Historical Success** - Tracks validated bugs
- **Fast-Track Validation** - High-reputation researchers get priority

### 3. Smart Contract Vault
- **Escrow System** - Holds bounty funds securely
- **Auto-Release** - Pays out on AI/validator approval
- **Multi-Signature** - Optional manual override

## 📊 Database Schema

See [database/schema.sql](database/schema.sql) for complete schema.

**Key Tables:**
- `users` - Researcher profiles & wallet addresses
- `bug_reports` - Submitted vulnerabilities
- `reputation_scores` - Trust metrics per wallet
- `bounty_transactions` - Payment history

## 🔐 Security Considerations

- All smart contracts audited before mainnet deployment
- Rate limiting on API endpoints
- Input validation on all user submissions
- IPFS content addressing for immutable evidence
- Multi-signature wallet for contract upgrades

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Contributing

See CONTRIBUTING.md for guidelines.

---

**Built with ❤️ for a frictionless bug bounty ecosystem**
