# 🚀 Quick Start Guide - Anti-Gravity Bug Bounty Platform

## Prerequisites Checklist

- [ ] **Node.js 18+** installed
- [ ] **Python 3.11+** installed
- [ ] **Git** installed
- [ ] **MetaMask** wallet extension
- [ ] **Supabase** account created
- [ ] **Alchemy** account for RPC access
- [ ] **Pinata** or **Web3.Storage** for IPFS

---

## 🎯 Phase 1: Database Setup (Supabase)

### Step 1: Create Supabase Project
1. Go to [supabase.com](https://supabase.com)
2. Create new project
3. Note your project URL and API keys

### Step 2: Initialize Database
1. Open Supabase SQL Editor
2. Copy contents of `database/schema.sql`
3. Execute the SQL script
4. Verify tables are created

### Step 3: Configure Environment
```bash
# backend/.env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-key
```

---

## 🐍 Phase 2: Backend Setup

### Step 1: Create Virtual Environment
```bash
cd backend
python -m venv venv
```

### Step 2: Activate Virtual Environment
**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment
```bash
# Copy example and edit
copy .env.example .env
# Edit .env with your values
```

### Step 5: Run Backend
```bash
uvicorn main:app --reload
```

**Verify:** Visit http://localhost:8000/docs

---

## ⚛️ Phase 3: Frontend Setup

### Step 1: Install Dependencies
```bash
cd frontend
npm install
```

### Step 2: Configure Environment
```bash
# Copy example and edit
copy .env.example .env.local
# Edit .env.local with your values
```

### Step 3: Get WalletConnect Project ID
1. Go to [cloud.walletconnect.com](https://cloud.walletconnect.com)
2. Create new project
3. Copy Project ID to `.env.local`

### Step 4: Run Frontend
```bash
npm run dev
```

**Verify:** Visit http://localhost:3000

---

## 🔗 Phase 4: Smart Contracts

### Step 1: Install Dependencies
```bash
cd contracts
npm install
```

### Step 2: Configure Environment
```bash
# Copy example and edit
copy .env.example .env
# Edit .env with your values
```

### Step 3: Get Alchemy API Key
1. Go to [alchemy.com](https://www.alchemy.com)
2. Create new app (Polygon Mumbai)
3. Copy API key to `.env`

### Step 4: Compile Contracts
```bash
npx hardhat compile
```

### Step 5: Run Tests
```bash
npx hardhat test
```

### Step 6: Deploy to Mumbai Testnet
```bash
# Make sure you have test MATIC in your wallet
npx hardhat run scripts/deploy.js --network mumbai
```

### Step 7: Verify Contract
```bash
npx hardhat verify --network mumbai <CONTRACT_ADDRESS>
```

---

## 🧪 Phase 5: Testing the Platform

### Test Flow 1: Health Check
```bash
# Backend health
curl http://localhost:8000/health

# Expected response:
{
  "status": "healthy",
  "service": "anti-gravity-bug-bounty",
  "version": "1.0.0"
}
```

### Test Flow 2: Wallet Connection
1. Open http://localhost:3000
2. Click "Connect Wallet"
3. Select MetaMask
4. Approve connection
5. Verify wallet address displayed

### Test Flow 3: Bug Submission (Once Implemented)
1. Navigate to "Submit Bug"
2. Fill in bug details
3. Upload evidence files
4. Submit form
5. AI analyzes report
6. View AI classification results
7. Check smart contract for auto-approval

---

## 📊 Monitoring & Debugging

### Backend Logs
```bash
# View logs in real-time
tail -f logs/app.log
```

### Frontend Dev Tools
- Open browser DevTools (F12)
- Check Console for errors
- Network tab for API calls

### Smart Contract Events
```bash
# Listen to contract events
npx hardhat run scripts/listen-events.js --network mumbai
```

---

## 🔧 Common Issues & Solutions

### Issue: Backend won't start
**Solution:**
```bash
# Check Python version
python --version  # Should be 3.11+

# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Issue: Frontend build errors
**Solution:**
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Issue: Contract deployment fails
**Solution:**
```bash
# Check wallet has test MATIC
# Get from: https://faucet.polygon.technology/

# Verify RPC URL is correct
# Check .env file
```

### Issue: Wallet won't connect
**Solution:**
1. Ensure MetaMask is installed
2. Switch to Polygon Mumbai network
3. Check WalletConnect Project ID in `.env.local`

---

## 📚 Next Steps

### For Development:
1. ✅ Complete Phase 1-4 setup
2. 📝 Implement AI models (Phase 2 of task.md)
3. 🎨 Build frontend components
4. 🧪 Write comprehensive tests
5. 🔐 Security audit

### For Production:
1. 🌐 Deploy backend to cloud (AWS/GCP/Vercel)
2. 🚀 Deploy frontend to Vercel/Netlify
3. 🔗 Deploy contracts to Polygon Mainnet
4. 📊 Set up monitoring (Sentry, DataDog)
5. 🔒 Enable rate limiting & security features

---

## 🆘 Getting Help

- **Documentation:** See `docs/` folder
- **API Reference:** http://localhost:8000/docs
- **Smart Contract Docs:** `docs/SMART_CONTRACTS.md`
- **Architecture:** `docs/ARCHITECTURE.md`

---

## ✅ Verification Checklist

Before proceeding to development:

- [ ] Supabase database initialized
- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] Smart contracts compiled successfully
- [ ] Wallet connects to frontend
- [ ] API health check passes
- [ ] Environment variables configured

**Status:** Ready for Phase 2 Development! 🎉
