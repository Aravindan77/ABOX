# 🛡️ ABOX — Bug Bounty Platform

> Remove friction and centralization through AI-driven validation, automated payments, and continuous reputation learning.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/Python-3.11+-green.svg)
![Next.js](https://img.shields.io/badge/Next.js-14-black.svg)
![Solidity](https://img.shields.io/badge/Solidity-0.8.20+-363636.svg)
![Network](https://img.shields.io/badge/Network-Polygon-8247E5.svg)

---

## 🎯 Core Principles

| Principle | Description |
|---|---|
| 🤖 Self-Validation | AI auto-triages reports to reduce human overhead |
| 💸 Auto-Release Payments | Smart contracts eliminate financial friction |
| 📈 Continuous Learning | Reputation engine reduces trust friction |

---

## 🏗️ Architecture
```
┌─────────────────┐      ┌──────────────────┐      ┌─────────────────┐
│   Next.js UI    │◄────►│  FastAPI Backend │◄────►│  Supabase DB    │
│  (Researchers)  │      │   (AI Engine)    │      │  (PostgreSQL)   │
└─────────────────┘      └──────────────────┘      └─────────────────┘
        │                         │
        ▼                         ▼
┌─────────────────┐      ┌──────────────────┐
│ Smart Contracts │      │      IPFS        │
│   (Polygon)     │      │   (Evidence)     │
└─────────────────┘      └──────────────────┘
```

---

## 🛠️ Tech Stack

### Frontend
- **Framework:** Next.js 14 (React + TypeScript)
- **Styling:** TailwindCSS + Shadcn UI
- **Web3:** Ethers.js, Wagmi, RainbowKit
- **Auth:** Wallet-based (MetaMask)

### Backend
- **API:** FastAPI (Python 3.11+)
- **AI/ML:** HuggingFace Transformers, Scikit-learn
- **Storage:** IPFS via Pinata / Web3.Storage

### Blockchain
- **Contracts:** Solidity 0.8.20+
- **Network:** Polygon (Mumbai Testnet → Mainnet)
- **Tools:** Hardhat, OpenZeppelin

### Database
- **Primary:** Supabase (PostgreSQL)
- **Key Tables:** Users, Bug Reports, Reputation, Transactions

---

## 📦 Project Structure
```
ABOX/
├── frontend/              # Next.js application
│   ├── app/               # App router pages
│   ├── components/        # React components
│   ├── lib/               # Utilities & hooks
│   └── contracts/         # ABI files
│
├── backend/               # FastAPI application
│   ├── app/
│   │   ├── api/           # API routes
│   │   ├── ml/            # AI/ML models
│   │   ├── services/      # Business logic
│   │   ├── models/        # Pydantic models
│   │   └── core/          # Config & utilities
│   ├── requirements.txt
│   └── main.py
│
├── contracts/             # Smart contracts
│   ├── contracts/         # Solidity files
│   ├── scripts/           # Deployment scripts
│   └── hardhat.config.js
│
├── database/              # DB schema
│   └── schema.sql
│
└── streamlit_demo/        # Demo app
    └── app.py
```

---

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.11+
- MetaMask wallet
- Supabase account
- IPFS provider (Pinata or Web3.Storage)

### 1. Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux
pip install -r requirements.txt
uvicorn main:app --reload
```

### 2. Frontend
```bash
cd frontend
npm install
npm run dev
```

### 3. Smart Contracts
```bash
cd contracts
npm install
npx hardhat compile
npx hardhat test
npx hardhat run scripts/deploy.js --network mumbai
```

---

## 🎯 Core Features

### 🤖 AI Auto-Triage
- **OWASP Top 10 Classification** — Maps bug reports to vulnerability categories
- **CVSS Scoring** — Automated severity assessment
- **Spam Detection** — Filters low-quality submissions

### ⭐ Reputation Engine
- **Trust Score** — Wallet-based reputation (0–100)
- **Historical Tracking** — Validates bugs over time
- **Fast-Track Validation** — High-reputation researchers get priority

### 🔒 Smart Contract Vault
- **Escrow System** — Holds bounty funds securely
- **Auto-Release** — Pays out on AI/validator approval
- **Multi-Signature** — Optional manual override

---

## 🔐 Security

- Smart contracts audited before mainnet deployment
- Rate limiting on all API endpoints
- Input validation on all user submissions
- IPFS content addressing for immutable evidence
- Multi-signature wallet for contract upgrades

---

## 📝 License

MIT License — see [LICENSE](LICENSE) for details.

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

**Built with ❤️ for a frictionless bug bounty ecosystem**
