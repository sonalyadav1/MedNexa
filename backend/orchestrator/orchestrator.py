"""
Multi-Agent Orchestrator
Coordinates all agents and manages the complete workflow pipeline
"""
import asyncio
from typing import Dict, Any, List
from models.schemas import (
    AnalysisRequest, AnalysisResponse, QueryIntent, Trial, Paper,
    AdverseEvent, SafetyAnalysis, ComparisonResult, InsightSummary
)
from agents.query_agent import QueryAgent
from agents.trials_agent import TrialsAgent
from agents.pubmed_agent import PubMedAgent
from agents.faers_agent import FAERSAgent
from agents.who_agent import WHOAgent
from agents.ema_agent import EMAAgent
from agents.clean_agent import CleanAgent
from agents.risk_agent import RiskAgent
from agents.insight_agent import InsightAgent
from agents.report_agent import ReportAgent
from utils.logger import setup_logger

logger = setup_logger(__name__)

class Orchestrator:
    """
    Main orchestrator that coordinates all agents in the MedNexa system
    
    Workflow:
    1. Query Understanding (Query Agent)
    2. Data Retrieval (Multiple agents in parallel)
    3. Data Cleaning & Normalization
    4. Safety & Risk Analysis
    5. Insight Generation & Comparison
    6. Report Generation (on demand)
    """
    
    def __init__(self):
        # Initialize all agents
        self.query_agent = QueryAgent()
        self.trials_agent = TrialsAgent()
        self.pubmed_agent = PubMedAgent()
        self.faers_agent = FAERSAgent()
        self.who_agent = WHOAgent()
        self.ema_agent = EMAAgent()
        self.clean_agent = CleanAgent()
        self.risk_agent = RiskAgent()
        self.insight_agent = InsightAgent()
        self.report_agent = ReportAgent()
        
        logger.info("Orchestrator initialized with all agents")
    
    async def analyze(self, request: AnalysisRequest) -> AnalysisResponse:
        """
        Execute complete analysis pipeline
        
        Args:
            request: Analysis request with query and filters
            
        Returns:
            Complete analysis response with all data and insights
        """
        logger.info(f"Starting analysis pipeline for query: {request.query}")
        
        try:
            # Step 1: Parse query
            logger.info("Step 1: Query Understanding")
            query_intent = self.query_agent.parse_query(request.query, request.filters)
            
            # Step 2: Fetch data from multiple sources in parallel
            logger.info("Step 2: Multi-Source Data Retrieval")
            trials, papers, adverse_events = await self._fetch_all_data(
                query_intent,
                include_literature=request.include_literature,
                include_safety=request.include_safety
            )
            
            # Step 3: Clean and normalize data
            logger.info("Step 3: Data Cleaning & Normalization")
            clean_trials = self.clean_agent.clean_trials(trials)
            clean_papers = self.clean_agent.clean_papers(papers)
            clean_events = self.clean_agent.clean_adverse_events(adverse_events)
            
            # Create unified dataset
            unified_data = self.clean_agent.create_unified_dataset(
                clean_trials, clean_papers, clean_events
            )
            
            # Step 4: Safety & Risk Analysis
            logger.info("Step 4: Safety & Risk Evaluation")
            safety_analysis = None
            if request.include_safety:
                safety_analysis = self.risk_agent.evaluate_safety(
                    clean_events, clean_trials
                )
            
            # Step 5: Generate comparison and insights
            logger.info("Step 5: Insight Generation & Comparison")
            comparison = self.insight_agent.generate_comparison(clean_trials)
            insights = self.insight_agent.generate_insights(
                clean_trials, clean_papers, comparison
            )
            
            # Step 6: Generate charts data
            charts = self._generate_charts_data(clean_trials, comparison)
            
            # Create response
            response = AnalysisResponse(
                structured_query=query_intent,
                trials=clean_trials[:request.max_trials],
                papers=clean_papers,
                safety=safety_analysis,
                combined_insights=insights,
                comparison=comparison,
                charts=charts
            )
            
            logger.info("Analysis pipeline completed successfully")
            return response
            
        except Exception as e:
            logger.error(f"Error in analysis pipeline: {str(e)}", exc_info=True)
            raise
    
    async def _fetch_all_data(self, query_intent: QueryIntent,
                             include_literature: bool = True,
                             include_safety: bool = True) -> tuple:
        """
        Fetch data from all sources in parallel
        
        Returns:
            Tuple of (trials, papers, adverse_events)
        """
        # Create tasks for parallel execution
        tasks = []
        
        # Always fetch trials
        tasks.append(self._fetch_trials(query_intent))
        
        # Optionally fetch literature
        if include_literature:
            tasks.append(self.pubmed_agent.fetch_papers(query_intent))
        else:
            tasks.append(self._return_empty_list())
        
        # Optionally fetch safety data
        if include_safety:
            tasks.append(self.faers_agent.fetch_adverse_events(query_intent))
        else:
            tasks.append(self._return_empty_list())
        
        # Execute all tasks in parallel
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle results and exceptions
        trials = results[0] if not isinstance(results[0], Exception) else []
        papers = results[1] if not isinstance(results[1], Exception) else []
        adverse_events = results[2] if not isinstance(results[2], Exception) else []
        
        # Log any errors
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Error in data fetch task {i}: {str(result)}")
        
        logger.info(f"Fetched: {len(trials)} trials, {len(papers)} papers, "
                   f"{len(adverse_events)} adverse events")
        
        return trials, papers, adverse_events
    
    async def _fetch_trials(self, query_intent: QueryIntent) -> List[Trial]:
        """Fetch trials from multiple registries"""
        # Fetch from primary sources in parallel
        tasks = [
            self.trials_agent.fetch_trials(query_intent),
            self.who_agent.fetch_trials(query_intent),
            self.ema_agent.fetch_trials(query_intent)
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Combine all trials
        all_trials = []
        for result in results:
            if isinstance(result, list):
                all_trials.extend(result)
        
        return all_trials
    
    async def _return_empty_list(self) -> List:
        """Return empty list (for optional data fetches)"""
        return []
    
    def _generate_charts_data(self, trials: List[Trial], 
                             comparison: ComparisonResult) -> Dict[str, Any]:
        """
        Generate data for frontend charts
        
        Returns:
            Dictionary with chart data
        """
        charts = {}
        
        # Phase distribution pie chart
        charts["phase_distribution"] = {
            "type": "pie",
            "data": [
                {"name": phase, "value": count}
                for phase, count in comparison.phase_distribution.items()
            ]
        }
        
        # Country distribution bar chart (top 10)
        top_countries = list(comparison.country_distribution.items())[:10]
        charts["country_distribution"] = {
            "type": "bar",
            "data": [
                {"country": country, "trials": count}
                for country, count in top_countries
            ]
        }
        
        # Status distribution
        status_counts = {}
        for trial in trials:
            status_counts[trial.status] = status_counts.get(trial.status, 0) + 1
        
        charts["status_distribution"] = {
            "type": "pie",
            "data": [
                {"name": status, "value": count}
                for status, count in status_counts.items()
            ]
        }
        
        # Enrollment stats
        charts["enrollment_stats"] = {
            "type": "stats",
            "data": comparison.enrollment_stats
        }
        
        # Timeline (if dates available)
        trials_with_dates = [t for t in trials if t.start_date]
        if trials_with_dates:
            # Group by year
            year_counts = {}
            for trial in trials_with_dates:
                year = trial.start_date[:4]
                year_counts[year] = year_counts.get(year, 0) + 1
            
            charts["timeline"] = {
                "type": "line",
                "data": [
                    {"year": year, "count": count}
                    for year, count in sorted(year_counts.items())
                ]
            }
        
        return charts
    
    async def compare_trials(self, trial_ids: List[str]) -> ComparisonResult:
        """
        Compare specific trials by ID
        
        Args:
            trial_ids: List of trial NCT IDs to compare
            
        Returns:
            Comparison result
        """
        logger.info(f"Comparing {len(trial_ids)} trials")
        
        # This would fetch specific trials by ID
        # For now, returns a basic comparison
        # In production, you'd fetch specific trial details
        
        return ComparisonResult(
            trial_count=len(trial_ids),
            common_interventions=[],
            common_conditions=[],
            phase_distribution={},
            country_distribution={},
            enrollment_stats={
                "total": 0,
                "mean": 0,
                "median": 0,
                "min": 0,
                "max": 0
            },
            efficacy_summary="Detailed comparison requires full trial data.",
            design_differences=[],
            risk_comparison={}
        )
    
    async def generate_report(self, analysis: AnalysisResponse,
                            title: str = "MedNexa Research Report"):
        """
        Generate PDF report from analysis
        
        Args:
            analysis: Complete analysis response
            title: Report title
            
        Returns:
            PDF bytes
        """
        logger.info("Generating PDF report")
        
        pdf_buffer = await self.report_agent.generate_report(analysis, title)
        
        logger.info("PDF report generated")
        return pdf_buffer
