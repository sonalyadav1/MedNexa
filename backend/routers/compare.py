"""
Comparison Router
Handles trial comparison endpoints
"""
from fastapi import APIRouter, HTTPException
from typing import List
from models.schemas import ComparisonRequest, ComparisonResult
from orchestrator.orchestrator import Orchestrator
from utils.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter()

orchestrator = Orchestrator()

@router.post("/compare", response_model=ComparisonResult)
async def compare_trials(request: ComparisonRequest):
    """
    Compare multiple clinical trials
    
    Accepts a list of trial IDs and comparison criteria.
    Returns comparative analysis including:
    - Phase comparison
    - Enrollment comparison
    - Outcome comparison
    - Risk comparison
    """
    try:
        logger.info(f"Comparing {len(request.trial_ids)} trials")
        
        result = await orchestrator.compare_trials(request.trial_ids)
        
        return result
        
    except Exception as e:
        logger.error(f"Error in comparison endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Comparison failed: {str(e)}"
        )

@router.get("/compare-interventions")
async def compare_interventions(
    interventions: str,  # Comma-separated list
    condition: str = None
):
    """
    Compare different interventions for the same condition
    
    Query Parameters:
    - interventions: Comma-separated list of drug names
    - condition: Medical condition (optional)
    """
    try:
        from models.schemas import QueryIntent, AnalysisRequest
        from agents.trials_agent import TrialsAgent
        from agents.clean_agent import CleanAgent
        from agents.insight_agent import InsightAgent
        
        intervention_list = [i.strip() for i in interventions.split(",")]
        
        trials_agent = TrialsAgent()
        clean_agent = CleanAgent()
        insight_agent = InsightAgent()
        
        all_trials = []
        
        # Fetch trials for each intervention
        for intervention in intervention_list:
            query_intent = QueryIntent(
                condition=condition,
                intervention=intervention
            )
            
            trials = await trials_agent.fetch_trials(query_intent)
            all_trials.extend(trials)
        
        # Clean and compare
        clean_trials = clean_agent.clean_trials(all_trials)
        comparison = insight_agent.generate_comparison(clean_trials)
        
        return {
            "interventions": intervention_list,
            "comparison": comparison
        }
        
    except Exception as e:
        logger.error(f"Error comparing interventions: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Intervention comparison failed: {str(e)}"
        )
