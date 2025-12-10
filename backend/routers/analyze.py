"""
Analysis Router
Handles /analyze endpoint for complete pharma research analysis
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from models.schemas import AnalysisRequest, AnalysisResponse
from orchestrator.orchestrator import Orchestrator
from utils.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter()

# Create orchestrator instance
orchestrator = Orchestrator()

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_query(request: AnalysisRequest):
    """
    Main analysis endpoint
    
    Accepts a natural language query and performs:
    - Query parsing
    - Multi-source data retrieval
    - Data cleaning and normalization
    - Safety analysis
    - Insight generation
    - Comparison
    
    Returns complete analysis with trials, papers, safety data, and insights
    """
    try:
        logger.info(f"Received analysis request: {request.query}")
        
        # Execute full analysis pipeline
        result = await orchestrator.analyze(request)
        
        logger.info("Analysis completed successfully")
        return result
        
    except Exception as e:
        logger.error(f"Error in analysis endpoint: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )

@router.get("/get-trials")
async def get_trials(
    condition: str = None,
    intervention: str = None,
    phase: str = None,
    country: str = None,
    max_results: int = 50
):
    """
    Get clinical trials with specific filters
    
    Query Parameters:
    - condition: Medical condition
    - intervention: Drug/intervention name
    - phase: Trial phase (PHASE_1, PHASE_2, etc.)
    - country: Country name
    - max_results: Maximum number of results
    """
    try:
        from models.schemas import QueryIntent
        from agents.trials_agent import TrialsAgent
        from agents.clean_agent import CleanAgent
        
        query_intent = QueryIntent(
            condition=condition,
            intervention=intervention,
            phase=[phase] if phase else None,
            country=[country] if country else None,
            max_results=max_results
        )
        
        trials_agent = TrialsAgent()
        clean_agent = CleanAgent()
        
        # Fetch and clean trials
        trials = await trials_agent.fetch_trials(query_intent)
        clean_trials = clean_agent.clean_trials(trials)
        
        return {
            "count": len(clean_trials),
            "trials": clean_trials
        }
        
    except Exception as e:
        logger.error(f"Error fetching trials: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch trials: {str(e)}"
        )

@router.get("/get-literature")
async def get_literature(
    condition: str = None,
    intervention: str = None,
    max_results: int = 20
):
    """
    Get scientific literature from PubMed
    
    Query Parameters:
    - condition: Medical condition
    - intervention: Drug/intervention name
    - max_results: Maximum number of results
    """
    try:
        from models.schemas import QueryIntent
        from agents.pubmed_agent import PubMedAgent
        from agents.clean_agent import CleanAgent
        
        query_intent = QueryIntent(
            condition=condition,
            intervention=intervention
        )
        
        pubmed_agent = PubMedAgent()
        clean_agent = CleanAgent()
        
        # Fetch and clean papers
        papers = await pubmed_agent.fetch_papers(query_intent, max_results)
        clean_papers = clean_agent.clean_papers(papers)
        
        return {
            "count": len(clean_papers),
            "papers": clean_papers
        }
        
    except Exception as e:
        logger.error(f"Error fetching literature: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch literature: {str(e)}"
        )

@router.get("/get-safety-data")
async def get_safety_data(
    drug_name: str,
    max_results: int = 100
):
    """
    Get adverse event data from FDA FAERS
    
    Query Parameters:
    - drug_name: Drug or intervention name
    - max_results: Maximum number of results
    """
    try:
        from models.schemas import QueryIntent
        from agents.faers_agent import FAERSAgent
        from agents.clean_agent import CleanAgent
        from agents.risk_agent import RiskAgent
        
        query_intent = QueryIntent(intervention=drug_name)
        
        faers_agent = FAERSAgent()
        clean_agent = CleanAgent()
        risk_agent = RiskAgent()
        
        # Fetch and clean adverse events
        events = await faers_agent.fetch_adverse_events(query_intent, max_results)
        clean_events = clean_agent.clean_adverse_events(events)
        
        # Perform safety analysis
        safety_analysis = risk_agent.evaluate_safety(clean_events, [])
        
        return {
            "count": len(clean_events),
            "adverse_events": clean_events,
            "safety_analysis": safety_analysis
        }
        
    except Exception as e:
        logger.error(f"Error fetching safety data: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch safety data: {str(e)}"
        )
