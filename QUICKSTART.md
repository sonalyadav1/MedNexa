# MedNexa Quick Start Guide

## ⚡ Fast Setup (5 minutes)

### Option 1: Automated Start (Recommended)

#### macOS/Linux:
```bash
chmod +x start.sh
./start.sh
```

#### Windows:
```bash
start.bat
```

The script will:
1. Check prerequisites
2. Install all dependencies
3. Start backend (http://localhost:8000)
4. Start frontend (http://localhost:3000)

### Option 2: Manual Start

#### Terminal 1 - Backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python main.py
```

#### Terminal 2 - Frontend:
```bash
cd frontend
npm install
npm run dev
```

##  First Query

1. Open browser: http://localhost:3000
2. Enter a query:
   ```
   Find Phase 3 breast cancer immunotherapy trials
   ```
3. Click Search 
4. View results in Dashboard

##  What You'll See

### Dashboard Tabs:
- **Overview** - Charts and statistics
- **Clinical Trials** - 50+ trials from ClinicalTrials.gov
- **Literature** - Scientific papers from PubMed
- **Safety Analysis** - FDA adverse event data
- **Insights** - AI-generated recommendations

### Example Output:
```
 47 Clinical Trials Found
 20 Scientific Papers
 Safety Risk Score: 5.2/10 (Medium)
 15 Key Insights Generated
```

##  API Keys (Optional)

For better rate limits, add to `backend/.env`:

```env
# PubMed (Higher rate limits)
NCBI_API_KEY=your_key_here
NCBI_EMAIL=your@email.com

# Get key: https://www.ncbi.nlm.nih.gov/account/
```

## Try These Queries

1. **Drug Safety:**
   ```
   COVID-19 vaccine adverse events and safety data
   ```

2. **Disease Research:**
   ```
   Alzheimer's disease trials in Phase 2 from 2020-2024
   ```

3. **Geographic Search:**
   ```
   Cancer immunotherapy trials in United States and Europe
   ```

4. **Intervention Comparison:**
   ```
   Metformin vs insulin for Type 2 diabetes treatment
   ```

##  Generate Report

1. Complete a search
2. Go to Report page
3. Click "Generate & Download Report"
4. Get comprehensive PDF with:
   - Executive summary
   - All trial data
   - Charts & visualizations
   - Safety analysis
   - Recommendations

##  API Testing

Test API directly:

```bash
# Health check
curl http://localhost:8000/health

# Analyze query
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "query": "breast cancer trials",
    "max_trials": 10
  }'

# View API docs
open http://localhost:8000/docs
```

##  Troubleshooting

### Backend won't start:
```bash
cd backend
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Frontend won't start:
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Port already in use:
```bash
# Backend - Edit main.py port (default: 8000)
# Frontend - Edit vite.config.js port (default: 3000)
```

### No data returned:
- Check internet connection
- Verify API endpoints are accessible
- Review backend logs for errors

##  Next Steps

1. **Customize Agents:** Edit files in `backend/agents/`
2. **Add Data Sources:** Extend agents with new APIs
3. **Modify UI:** Update React components in `frontend/src/`
4. **Deploy:** See README for Docker deployment

##  Learn More

- Full Documentation: README.md
- API Reference: http://localhost:8000/docs
- Architecture Guide: README.md#architecture


**Need Help?** Check the full README.md or open an issue on GitHub.
