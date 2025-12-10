# MedNexa - Multi-Agent AI Pharma Research Assistant 

A comprehensive pharmaceutical research automation platform powered by multi-agent AI that performs end-to-end analysis across multiple global medical databases.

![MedNexa Banner](https://img.shields.io/badge/MedNexa-AI%20Pharma%20Research-blue)
![Python](https://img.shields.io/badge/Python-3.9+-green)
![React](https://img.shields.io/badge/React-18.2-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-teal)

##  Overview

MedNexa automates the entire pharmaceutical research workflow that traditionally takes researchers days or weeks. It aggregates data from 5 major medical databases, performs AI-powered analysis, generates safety assessments, and produces comprehensive reports.

### Problem Solved
Researchers waste significant time manually searching across multiple websites for clinical trials, scientific papers, safety alerts, and global health updates. MedNexa automates this entire workflow with intelligent multi-agent coordination.

##  Core Features

### 1. **Multi-Source Data Aggregation**
- **ClinicalTrials.gov** - US clinical trials database
- **PubMed/NCBI** - Scientific literature and papers
- **FDA FAERS** - Adverse event reports and drug safety
- **WHO ICTRP** - Global trial registries
- **EMA Registry** - European clinical trials

### 2. **Multi-Agent AI System** (6 Specialized Agents)

#### Agent 1: Query Understanding Agent
- Parses natural language queries
- Extracts conditions, interventions, phases, dates, regions
- Structures search parameters

#### Agent 2: Multi-Source Retrieval Agent
- Parallel data fetching from all 5 sources
- API integration with real endpoints
- Error handling and retry logic

#### Agent 3: Data Cleaning & Normalization Agent
- Removes duplicates across sources
- Standardizes field names and formats
- Maps different terminologies
- Creates unified data model

#### Agent 4: Safety & Risk Evaluation Agent
- Analyzes adverse events from FAERS
- Computes risk scores (0-10 scale)
- Identifies black-box warnings
- Generates safety summaries

#### Agent 5: Insight & Comparison Agent
- Cross-trial comparison
- Pattern identification
- Efficacy analysis
- Geographic and temporal trends

#### Agent 6: Report Generation Agent
- PDF report creation with ReportLab
- Charts and visualizations
- Complete analysis documentation

### 3. **Interactive Dashboard**
- Real-time data visualization with Recharts
- Filterable trial listings
- Safety analysis panels
- Comparison views
- Downloadable PDF reports

##  Architecture

```
MedNexa/
├── backend/                  # FastAPI Backend
│   ├── agents/              # Multi-agent system
│   │   ├── query_agent.py
│   │   ├── trials_agent.py
│   │   ├── pubmed_agent.py
│   │   ├── faers_agent.py
│   │   ├── who_agent.py
│   │   ├── ema_agent.py
│   │   ├── clean_agent.py
│   │   ├── risk_agent.py
│   │   ├── insight_agent.py
│   │   └── report_agent.py
│   ├── orchestrator/        # Agent coordination
│   │   └── orchestrator.py
│   ├── routers/             # API endpoints
│   │   ├── analyze.py
│   │   ├── compare.py
│   │   └── report.py
│   ├── models/              # Data models
│   │   └── schemas.py
│   ├── utils/               # Utilities
│   │   ├── config.py
│   │   └── logger.py
│   └── main.py              # FastAPI app
│
└── frontend/                # React Frontend
    ├── src/
    │   ├── pages/          # Main pages
    │   │   ├── HomePage.jsx
    │   │   ├── DashboardPage.jsx
    │   │   ├── ComparisonPage.jsx
    │   │   └── ReportPage.jsx
    │   ├── components/     # Reusable components
    │   │   ├── Layout.jsx
    │   │   ├── ChartsPanel.jsx
    │   │   ├── TrialsTable.jsx
    │   │   ├── PapersTable.jsx
    │   │   ├── SafetyPanel.jsx
    │   │   └── InsightsPanel.jsx
    │   ├── api/           # API integration
    │   │   └── api.js
    │   ├── store/         # State management
    │   │   └── store.js
    │   └── styles/        # Tailwind CSS
    └── package.json
```

##  Installation & Setup

### Prerequisites
- Python 3.9 or higher
- Node.js 16 or higher
- npm or yarn

### Backend Setup

1. **Navigate to backend directory:**
```bash
cd backend
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables:**
```bash
cp .env.example .env
```

Edit `.env` file:
```env
# Optional: Add your API keys for better rate limits
NCBI_API_KEY=your_ncbi_key_here
NCBI_EMAIL=your_email@example.com
OPENAI_API_KEY=your_openai_key  # Optional for enhanced AI
```

5. **Run the backend server:**
```bash
python main.py
```

The API will be available at `http://localhost:8000`
- Swagger docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Frontend Setup

1. **Navigate to frontend directory:**
```bash
cd frontend
```

2. **Install dependencies:**
```bash
npm install
```

3. **Start development server:**
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

##  Usage Guide

### 1. Basic Search

Navigate to the home page and enter a natural language query:

**Example Queries:**
- "Find Phase 3 trials for breast cancer immunotherapy"
- "COVID-19 vaccine trials in the United States"
- "Diabetes treatment trials using metformin in 2023"
- "Alzheimer's disease clinical trials in Phase 2"

### 2. View Results

The system will:
1. Parse your query
2. Search all 5 medical databases
3. Clean and normalize the data
4. Perform safety analysis
5. Generate insights and comparisons
6. Display results in the dashboard

### 3. Explore Dashboard

**Tabs Available:**
- **Overview** - Charts and key insights
- **Clinical Trials** - Detailed trial listings
- **Literature** - Scientific publications
- **Safety Analysis** - Risk assessment and warnings
- **Insights** - AI-generated recommendations

### 4. Generate Reports

Click "Generate Report" to create a comprehensive PDF including:
- Executive summary
- Trial listings
- Literature review
- Safety analysis
- Comparison charts
- Insights and recommendations

##  API Endpoints

### Analysis Endpoints

#### POST `/api/analyze`
Main analysis endpoint that performs complete research workflow.

**Request Body:**
```json
{
  "query": "Phase 3 breast cancer trials",
  "filters": {
    "condition": "breast cancer",
    "phase": "PHASE_3"
  },
  "include_literature": true,
  "include_safety": true,
  "max_trials": 50
}
```

**Response:**
```json
{
  "structured_query": {...},
  "trials": [...],
  "papers": [...],
  "safety": {...},
  "combined_insights": {...},
  "comparison": {...},
  "charts": {...}
}
```

#### GET `/api/get-trials`
Fetch clinical trials with filters.

**Query Parameters:**
- `condition` - Medical condition
- `intervention` - Drug/intervention name
- `phase` - Trial phase
- `country` - Country name
- `max_results` - Maximum results (default: 50)

#### GET `/api/get-literature`
Fetch scientific papers from PubMed.

#### GET `/api/get-safety-data`
Fetch adverse event data from FDA FAERS.

### Comparison Endpoints

#### POST `/api/compare`
Compare multiple trials by ID.

#### GET `/api/compare-interventions`
Compare different interventions for the same condition.

### Report Endpoints

#### POST `/api/generate-report`
Generate and download PDF report.

#### GET `/api/download-sample-report`
Download a sample report (no analysis required).

## 🔬 Data Sources & APIs

### 1. ClinicalTrials.gov API v2
- **Endpoint:** `https://clinicaltrials.gov/api/v2/studies`
- **Data:** Trial phases, interventions, enrollment, status
- **Rate Limit:** No authentication required

### 2. NCBI E-Utilities (PubMed)
- **Endpoint:** `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/`
- **Data:** Scientific papers, abstracts, citations
- **API Key:** Recommended for higher rate limits

### 3. FDA FAERS API
- **Endpoint:** `https://api.fda.gov/drug/event.json`
- **Data:** Adverse events, drug safety reports
- **Rate Limit:** 1000 requests/day (no key), 120,000/day (with key)

### 4. WHO ICTRP
- **Note:** Requires registration for API access
- **Data:** Global trial registry

### 5. EMA Clinical Trials
- **Note:** Requires specific authentication
- **Data:** European trial information

##  Frontend Technologies

- **React 18.2** - UI framework
- **React Router** - Navigation
- **Tailwind CSS** - Styling
- **Recharts** - Data visualization
- **Zustand** - State management
- **Axios** - HTTP client
- **React Hot Toast** - Notifications
- **Hero Icons** - Icon library

##  Backend Technologies

- **FastAPI** - Web framework
- **Pydantic** - Data validation
- **httpx** - Async HTTP client
- **ReportLab** - PDF generation
- **xmltodict** - XML parsing
- **pandas** - Data processing
- **matplotlib** - Chart generation

##  Data Models

### Trial Model
```python
{
  "nct_id": str,
  "title": str,
  "condition": List[str],
  "intervention": List[str],
  "phase": str,
  "status": str,
  "enrollment": int,
  "sponsor": str,
  "country": List[str],
  "summary": str
}
```

### Safety Analysis Model
```python
{
  "risk_score": float (0-10),
  "risk_label": str (Low/Medium/High),
  "safety_summary": str,
  "adverse_events_count": int,
  "serious_events_count": int,
  "warnings": List[str],
  "black_box_warnings": List[str],
  "death_reports": int
}
```

##  Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

##  Deployment

### Docker Deployment (Recommended)

Create `docker-compose.yml`:
```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - NCBI_API_KEY=${NCBI_API_KEY}
  
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
```

Run:
```bash
docker-compose up
```

### Manual Deployment

#### Backend (Uvicorn + Gunicorn)
```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

#### Frontend (Build for Production)
```bash
npm run build
npm run preview
```

##  Security Considerations

1. **API Keys:** Store in environment variables, never commit
2. **CORS:** Configure allowed origins in production
3. **Rate Limiting:** Implement for public APIs
4. **Input Validation:** All inputs validated with Pydantic
5. **HTTPS:** Use SSL certificates in production

##  Troubleshooting

### Common Issues

**Backend won't start:**
```bash
# Check Python version
python --version  # Should be 3.9+

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**Frontend build fails:**
```bash
# Clear cache
rm -rf node_modules package-lock.json
npm install
```

**API requests fail:**
- Check backend is running on port 8000
- Verify CORS settings in `main.py`
- Check network connectivity

**No data returned:**
- Verify API endpoints are accessible
- Check API rate limits
- Review backend logs

## Performance Optimization

1. **Caching:** Implement Redis for frequent queries
2. **Parallel Processing:** All data sources fetched concurrently
3. **Pagination:** Large result sets paginated
4. **Database:** Add PostgreSQL for persistent storage
5. **CDN:** Use CDN for frontend static assets

##  Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

##  License

MIT License - See LICENSE file for details

##  Authors

MedNexa Development Team

##  Acknowledgments

- ClinicalTrials.gov for clinical trial data
- NCBI/PubMed for scientific literature
- FDA for adverse event data
- WHO and EMA for global trial registries

## Contact

For questions or support:
- Email: sonal.y6390@gmail.com


