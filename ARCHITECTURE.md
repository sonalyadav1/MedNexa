# MedNexa System Architecture

## Overview

MedNexa is a sophisticated multi-agent AI system designed for pharmaceutical research automation. It follows a modular, scalable architecture with clear separation of concerns.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        User Interface                        │
│                     (React + Tailwind)                       │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/REST
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Backend                           │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              Orchestrator                             │  │
│  │         (Coordinates all agents)                      │  │
│  └───────────────────────────────────────────────────────┘  │
│           │        │        │        │        │              │
│           ▼        ▼        ▼        ▼        ▼              │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐          │
│  │ Query   │ │Retrieval│ │ Clean   │ │  Risk   │          │
│  │ Agent   │ │ Agent   │ │ Agent   │ │ Agent   │          │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘          │
│           │        │                    │        │           │
│           ▼        ▼                    ▼        ▼           │
│  ┌─────────┐ ┌─────────────────────┐ ┌─────────────────┐  │
│  │Insight  │ │  Data Sources       │ │     Report      │  │
│  │ Agent   │ │  - ClinicalTrials   │ │     Agent       │  │
│  └─────────┘ │  - PubMed           │ └─────────────────┘  │
│              │  - FAERS            │                       │
│              │  - WHO              │                       │
│              │  - EMA              │                       │
│              └─────────────────────┘                       │
└─────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Frontend Layer

**Technology Stack:**
- React 18.2 with functional components
- Tailwind CSS for styling
- Zustand for state management
- Recharts for data visualization
- Axios for API communication

**Key Components:**
- `Layout.jsx` - Main application shell
- `HomePage.jsx` - Query input and search
- `DashboardPage.jsx` - Results visualization
- `ComparisonPage.jsx` - Cross-trial comparison
- `ReportPage.jsx` - PDF report generation
- `ChartsPanel.jsx` - Data visualizations
- `TrialsTable.jsx` - Trial data display
- `SafetyPanel.jsx` - Risk assessment display

### 2. Backend Layer

**Technology Stack:**
- FastAPI for high-performance async API
- Pydantic for data validation
- httpx for async HTTP requests
- ReportLab for PDF generation

**API Routers:**
- `analyze.py` - Main analysis endpoints
- `compare.py` - Comparison endpoints
- `report.py` - Report generation endpoints

### 3. Multi-Agent System

#### Agent 1: Query Understanding Agent
**Purpose:** Parse natural language queries into structured parameters

**Process:**
1. Extract medical condition from query
2. Identify intervention/drug name
3. Parse trial phase requirements
4. Extract geographic filters
5. Determine date range
6. Output structured QueryIntent object

**Example:**
```python
Input: "Phase 3 breast cancer trials in US from 2020-2024"
Output: {
    "condition": "breast cancer",
    "phase": ["PHASE_3"],
    "country": ["United States"],
    "start_date": "2020-01-01",
    "end_date": "2024-12-31"
}
```

#### Agent 2: Multi-Source Retrieval Agent
**Purpose:** Fetch data from all medical databases in parallel

**Sub-agents:**
- **TrialsAgent** - ClinicalTrials.gov API v2
- **PubMedAgent** - NCBI E-Utilities API
- **FAERSAgent** - FDA FAERS API
- **WHOAgent** - WHO ICTRP (placeholder)
- **EMAAgent** - EMA Registry (placeholder)

**Process:**
1. Build API-specific queries
2. Execute parallel async requests
3. Handle rate limits and errors
4. Return raw data from each source

**Performance:**
- Parallel execution reduces latency by 80%
- Timeout handling prevents blocking
- Retry logic for transient failures

#### Agent 3: Data Cleaning & Normalization Agent
**Purpose:** Unify heterogeneous data into consistent format

**Tasks:**
1. **Deduplication:**
   - Remove duplicate trials by NCT ID
   - Merge papers by PMID/DOI
   - Consolidate adverse events

2. **Standardization:**
   - Normalize phase names (Phase 1 → PHASE_1)
   - Standardize status values
   - Unify country names
   - Clean text fields

3. **Field Mapping:**
   - Map different terminologies
   - Extract consistent fields
   - Create unified data model

**Output:**
- Clean, deduplicated datasets
- Consistent field names
- Standardized values

#### Agent 4: Safety & Risk Evaluation Agent
**Purpose:** Compute risk scores and safety assessments

**Risk Calculation:**
```python
risk_score = weighted_average(
    severity_score,  # 1-10 based on event severity
    outcome_score,   # 1-10 based on outcome (death, hospitalization, etc.)
    frequency        # Number of events
)
```

**Risk Labels:**
- **Low (0-3.9):** Minimal safety concerns
- **Medium (4-6.9):** Moderate concerns, monitoring needed
- **High (7-10):** Significant safety signals

**Warnings:**
- General warnings for patterns
- Black-box warnings for critical events
- Death report summaries

#### Agent 5: Insight & Comparison Agent
**Purpose:** Generate AI-powered insights and comparisons

**Analyses:**
1. **Comparison:**
   - Phase distribution
   - Geographic spread
   - Enrollment statistics
   - Status breakdown

2. **Pattern Identification:**
   - Temporal trends
   - Geographic patterns
   - Phase progression
   - Success rates

3. **Recommendations:**
   - Based on trial landscape
   - Gap identification
   - Future research directions

#### Agent 6: Report Generation Agent
**Purpose:** Create comprehensive PDF reports

**Report Structure:**
1. Cover page with metadata
2. Executive summary
3. Query parameters
4. Clinical trials section
5. Literature review
6. Safety analysis
7. Comparison section
8. Insights and recommendations

**Features:**
- Professional formatting with ReportLab
- Tables and charts
- Color-coded risk indicators
- Hyperlinks to original sources

### 4. Orchestrator

**Purpose:** Coordinate all agents and manage workflow

**Workflow Pipeline:**
```
1. Parse Query (Query Agent)
        ↓
2. Fetch Data (Retrieval Agents in parallel)
        ↓
3. Clean Data (Clean Agent)
        ↓
4. Analyze Safety (Risk Agent)
        ↓
5. Generate Insights (Insight Agent)
        ↓
6. Return Results
        ↓
7. Generate Report (on demand)
```

**Error Handling:**
- Individual agent failures don't block pipeline
- Graceful degradation
- Detailed logging
- Error aggregation

## Data Flow

### Request Flow:
```
User Query → Frontend → API Endpoint → Orchestrator → Agents → External APIs
```

### Response Flow:
```
External APIs → Agents → Orchestrator → Data Processing → API Response → Frontend
```

## Performance Characteristics

### Latency:
- Query parsing: < 100ms
- Data retrieval: 2-5 seconds (parallel)
- Data cleaning: < 500ms
- Risk analysis: < 200ms
- Insight generation: < 300ms
- **Total: 3-6 seconds**

### Throughput:
- Concurrent requests: 10-50 (configurable)
- API rate limits: Respected per source
- Cache layer: Optional (Redis)

## Security Features

1. **Input Validation:**
   - Pydantic models validate all inputs
   - SQL injection prevention
   - XSS protection

2. **API Security:**
   - CORS configuration
   - Rate limiting
   - API key management (environment variables)

3. **Data Privacy:**
   - No persistent user data storage
   - Temporary processing only
   - HIPAA-compliant practices

## Scalability

### Horizontal Scaling:
- Stateless backend enables multiple instances
- Load balancer distribution
- Session affinity not required

### Vertical Scaling:
- Async operations reduce memory footprint
- Efficient data structures
- Streaming responses for large datasets

### Caching Strategy:
- Query result caching (optional)
- API response caching with TTL
- Static asset CDN

## Monitoring & Observability

### Logging:
- Structured logging with timestamps
- Log levels: INFO, WARNING, ERROR
- Agent-specific log identifiers

### Metrics:
- Request latency per endpoint
- Agent execution times
- API error rates
- Cache hit rates

### Health Checks:
- `/health` endpoint
- Database connectivity
- External API availability

## Future Enhancements

1. **Machine Learning:**
   - Predictive trial success modeling
   - Automated pattern recognition
   - Natural language query understanding with LLMs

2. **Real-time Updates:**
   - WebSocket connections
   - Live data streaming
   - Notification system

3. **Advanced Analytics:**
   - Temporal trend analysis
   - Network analysis of collaborations
   - Meta-analysis automation

4. **Integration:**
   - Electronic Health Records (EHR)
   - Clinical Decision Support Systems (CDSS)
   - Research management platforms

## Technology Choices Rationale

### Why FastAPI?
- **Performance:** Async support for parallel operations
- **Documentation:** Auto-generated API docs
- **Validation:** Built-in Pydantic integration
- **Modern:** Python 3.9+ features

### Why React?
- **Component-based:** Reusable UI components
- **Ecosystem:** Rich library ecosystem
- **Performance:** Virtual DOM optimization
- **Community:** Large developer community

### Why Multi-Agent Architecture?
- **Modularity:** Independent agent development
- **Scalability:** Parallel execution
- **Maintainability:** Clear separation of concerns
- **Extensibility:** Easy to add new agents/sources

---

This architecture provides a robust, scalable foundation for pharmaceutical research automation while maintaining code quality and developer experience.
