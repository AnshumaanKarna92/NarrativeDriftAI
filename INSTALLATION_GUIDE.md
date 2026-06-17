# 🚀 Installation & Setup Guide

Complete step-by-step guide to get the project running on your machine.

---

## System Requirements

### Minimum Specifications
- **OS**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Python**: 3.8 or higher
- **Node.js**: 18.0 or higher (for frontend)
- **RAM**: 8GB (16GB recommended)
- **Disk Space**: 2GB free
- **Internet**: Required for SEC EDGAR API access

### Recommended Setup
- **OS**: Windows 11 or macOS 13+
- **Python**: 3.10 or 3.11
- **Node.js**: 18.17 LTS or 20 LTS
- **RAM**: 16GB
- **Disk Space**: 4GB (includes models and data)

---

## Installation Steps

### 1️⃣ Clone Repository

```bash
git clone https://github.com/AnshumaanKarna92/NarrativeDriftAI.git
cd NarrativeDriftAI
```

### 2️⃣ Create Python Virtual Environment

#### Windows
```powershell
python -m venv .venv
.venv\Scripts\activate
```

#### macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3️⃣ Install Python Dependencies

```bash
# Install main project dependencies
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

# Install research_project dependencies
cd research_project
pip install -r requirements.txt
cd ..
```

### 4️⃣ Install Frontend Dependencies

```bash
cd temp_NarrativeDriftAI/frontend
npm install
cd ../..
```

### 5️⃣ Verify Installation

```bash
# Check Python packages
pip list

# Check Node.js
node --version
npm --version

# Quick test: Import key packages
python -c "import pandas; import torch; print('✓ Python packages OK')"
```

---

## ⚙️ Configuration

### Environment Variables (Optional)

Create `.env` file in project root:

```env
# SEC EDGAR API
SEC_API_RATE_LIMIT=0.2  # seconds between requests
SEC_API_TIMEOUT=30      # seconds

# Backend
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
DEBUG=False

# Frontend
REACT_APP_API_URL=http://localhost:8000
REACT_APP_TIMEOUT=5000
```

### API Configuration

Edit `temp_NarrativeDriftAI/api/server.py` if needed:

```python
# Customize API settings
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]
API_RATE_LIMIT = "100/minute"
```

---

## ▶️ Running the Application

### Option A: Full System (Recommended for First Run)

**Step 1: Run Analysis Pipeline**
```bash
cd temp_NarrativeDriftAI
python src/main.py
```

Expected output:
```
[✓] Step 1/9: SEC Data Collection Complete
[✓] Step 2/9: Embeddings Generated
[✓] Step 3/9: ESG Hard vs Soft Analysis Complete
[✓] Step 4/9: Sentiment & Topic Analysis Complete
[✓] Step 5/9: Financial Econometrics Complete
[✓] Step 6/9: Macro Events Alignment Complete
[✓] Step 7/9: Knowledge Graph Built
[✓] Step 8/9: Event Attribution Complete
[✓] Step 9/9: Critic Agent Validation ✓ PASSED

Processing time: 28 seconds
All outputs saved to: data/results/
```

**Step 2: Start Backend API**

Open new terminal window:
```bash
cd temp_NarrativeDriftAI
python -m uvicorn api.server:app --reload --port 8000
```

Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
INFO:     Reload is enabled, watching for file changes
```

**Step 3: Start Frontend Dashboard**

Open another new terminal window:
```bash
cd temp_NarrativeDriftAI/frontend
npm run dev
```

Expected output:
```
  ▲ Next.js 16.2.6
  - Local:        http://localhost:3000
  - Environments: .env.local

✓ Ready in 3.2s
```

**Step 4: Open in Browser**

- Dashboard: http://localhost:3000
- API Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

### Option B: Just the Analysis Pipeline

If you only want to run analysis without frontend:

```bash
cd research_project
python pipeline.py
```

Outputs generated in:
- `data/processed/` - CSV results
- `results/tables/` - JSON reports
- `results/figures/` - Visualizations

---

### Option C: Just the API (No Frontend)

```bash
cd temp_NarrativeDriftAI
python -m uvicorn api.server:app --port 8000
```

Access API endpoints directly:
- `curl http://localhost:8000/api/health`
- `curl http://localhost:8000/api/status`
- `curl http://localhost:8000/api/analytics/summary`

---

## 🔍 Verification Checklist

After installation, verify everything works:

### Python Environment ✓
```bash
python -c "import pandas as pd; print('✓ Pandas OK')"
python -c "from sentence_transformers import SentenceTransformer; print('✓ SentenceTransformers OK')"
python -c "import torch; print('✓ PyTorch OK')"
python -c "import fastapi; print('✓ FastAPI OK')"
```

### Data Files ✓
```bash
# Check if data directories exist
ls temp_NarrativeDriftAI/data/results/
# Should show: CSV files, JSON files, PNG figures, advanced/ subdirectory
```

### Backend API ✓
```bash
# Test API availability
curl http://localhost:8000/api/health
# Should return: {"status": "healthy"}
```

### Frontend ✓
```bash
# Test frontend build
cd temp_NarrativeDriftAI/frontend
npm run build
# Should complete without errors
```

---

## 🐛 Troubleshooting

### Issue 1: "ModuleNotFoundError: No module named 'pandas'"

**Solution**:
```bash
# Verify virtual environment is activated
which python  # macOS/Linux
where python  # Windows

# Should show path to .venv directory

# If not, reactivate:
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate      # Windows

# Then reinstall:
pip install -r requirements.txt
```

### Issue 2: "Port 8000 already in use"

**Solution**:
```bash
# Use different port
python -m uvicorn api.server:app --port 8001

# Or kill process using port 8000
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :8000
kill -9 <PID>
```

### Issue 3: "Port 3000 already in use"

**Solution**:
```bash
# Use different port in frontend
cd frontend
PORT=3001 npm run dev
```

### Issue 4: "SEC API rate limit exceeded"

**Solution**:
```bash
# Increase delay between requests in config
# Edit temp_NarrativeDriftAI/src/config.py

SEC_API_RATE_LIMIT = 0.5  # Increase from 0.2
```

### Issue 5: "Out of memory during embedding generation"

**Solution**:
```bash
# Process in smaller batches
# Edit temp_NarrativeDriftAI/src/analysis/main.py

EMBEDDING_BATCH_SIZE = 50  # Decrease from 100
```

### Issue 6: "Node_modules installation very slow"

**Solution**:
```bash
# Use npm ci instead of npm install
cd temp_NarrativeDriftAI/frontend
npm ci
```

### Issue 7: "CORS errors when connecting frontend to API"

**Solution 1**: If API on different port, update CORS in `api/server.py`
```python
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:3001",  # Add any alternate port
]
```

**Solution 2**: Check API is actually running
```bash
curl -I http://localhost:8000/api/health
# Should return HTTP 200
```

---

## 📦 Package Dependencies

### Critical Python Packages
```
pandas (2.0.3)          - Data manipulation
numpy (1.24.3)          - Numerical computing
torch (2.0.1)           - Deep learning
sentence-transformers   - Text embeddings
fastapi (0.104.1)       - REST API framework
scikit-learn            - Machine learning
scipy                   - Scientific computing
statsmodels             - Econometric models
```

### Critical Node Packages
```
next (16.2.6)           - React framework
react (19.2.4)          - UI library
react-force-graph-3d    - 3D graph visualization
tailwindcss             - CSS framework
axios                   - HTTP client
```

---

## 🚀 Advanced Setup

### Running with Docker (Optional)

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt
RUN cd research_project && pip install -r requirements.txt

EXPOSE 8000
CMD ["python", "-m", "uvicorn", "api.server:app", "--host", "0.0.0.0"]
```

Build and run:
```bash
docker build -t narrative-drift .
docker run -p 8000:8000 narrative-drift
```

### Using with IDEs

#### Visual Studio Code
```bash
# Open in VS Code
code .

# Recommended extensions:
# - Python (Microsoft)
# - Pylance
# - FastAPI
# - ES7+ React/Redux/React-Native snippets
```

#### PyCharm
```bash
# Open project in PyCharm
# Go to: File > Open > Select project folder

# Configure interpreter:
# Settings > Project > Python Interpreter > Add > Existing Environment
# Browse to: .venv/bin/python
```

---

## 🔐 Security Considerations

### Production Deployment

If deploying to production:

1. **Set `DEBUG=False`** in `.env`
2. **Use environment secrets** for API keys
3. **Enable HTTPS** with SSL certificate
4. **Implement authentication** for API endpoints
5. **Add rate limiting** middleware
6. **Enable CORS properly** (not `*`)

### API Key Management

For SEC EDGAR access:
```bash
# Create .env.local (never commit to git)
echo "SEC_API_KEY=your_key_here" > .env.local
```

Add to `.gitignore`:
```
.env
.env.local
.env.*.local
```

---

## 📊 Expected Disk Usage

After full installation and running pipeline:

```
Project Structure:
├── Code files:           50 MB
├── Python packages:      500 MB
├── Node modules:         350 MB
├── Model weights:        400 MB
├── Data (CSV/JSON):      100 MB
├── Results figures:      50 MB
└── Cache files:          50 MB
─────────────────────────────────
Total:                   1.5 GB
```

---

## ✅ Next Steps After Installation

1. **Explore the Dashboard**
   - Open http://localhost:3000
   - Interact with 3D knowledge graph
   - View analytics dashboard

2. **Read Results**
   - Check `RESULTS_ANALYSIS.md`
   - Review `TECHNICAL_OVERVIEW.md`
   - Examine JSON reports in `data/results/`

3. **API Integration**
   - Test endpoints at http://localhost:8000/docs
   - Build custom applications
   - Integrate with other tools

4. **Customize Analysis**
   - Modify ESG keywords in `config.py`
   - Add new companies to analysis
   - Extend with additional data sources

---

## 📧 Support

If you encounter issues during installation:

1. **Check logs**: Look at terminal output for specific error messages
2. **Review troubleshooting**: See [Troubleshooting](#-troubleshooting) section above
3. **Check requirements**: Verify Python/Node.js versions match requirements
4. **Search issues**: Check GitHub issues for similar problems
5. **Contact**: Email anshumaan.karna@gmail.com

---

## 🎉 Success Indicators

Installation is complete when you can:

✓ Run `python src/main.py` successfully  
✓ Backend API responds at `http://localhost:8000/api/health`  
✓ Frontend loads at `http://localhost:3000`  
✓ 3D graph visualization renders  
✓ All 35 output files present in `data/results/`  
✓ Critic Agent validation passes  

Congratulations! 🎊 You're ready to explore the analysis.

