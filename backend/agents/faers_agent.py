"""
FDA FAERS (Adverse Event Reporting System) Data Agent
Fetches drug safety data from FDA FAERS API
"""
import httpx
from typing import List, Optional
from models.schemas import AdverseEvent, QueryIntent
from utils.logger import setup_logger

logger = setup_logger(__name__)

class FAERSAgent:
    """Agent for fetching adverse event data from FDA FAERS"""
    
    BASE_URL = "https://api.fda.gov/drug/event.json"
    
    def __init__(self):
        pass
    
    async def fetch_adverse_events(self, query_intent: QueryIntent, max_results: int = 100) -> List[AdverseEvent]:
        """
        Fetch adverse events from FDA FAERS
        
        Args:
            query_intent: Structured query
            max_results: Maximum number of events to retrieve
            
        Returns:
            List of AdverseEvent objects
        """
        logger.info("Fetching adverse events from FDA FAERS")
        
        try:
            drug_name = query_intent.intervention or query_intent.condition
            
            if not drug_name:
                logger.info("No drug/condition specified for FAERS search")
                return []
            
            # Build search query
            search_query = self._build_search_query(drug_name)
            
            # Fetch data
            events = await self._fetch_events(search_query, max_results)
            
            logger.info(f"Fetched {len(events)} adverse events from FAERS")
            return events
            
        except Exception as e:
            logger.error(f"Error fetching adverse events: {str(e)}")
            return []
    
    def _build_search_query(self, drug_name: str) -> str:
        """Build FAERS API search query"""
        # Search in drug names (brand and generic)
        return f'patient.drug.medicinalproduct:"{drug_name}"'
    
    async def _fetch_events(self, search_query: str, max_results: int) -> List[AdverseEvent]:
        """Fetch adverse event data"""
        params = {
            "search": search_query,
            "limit": min(max_results, 100)  # FDA API limit is 100
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.get(self.BASE_URL, params=params)
                response.raise_for_status()
                
                data = response.json()
                results = data.get("results", [])
                
                events = []
                for result in results:
                    event = self._parse_event(result)
                    if event:
                        events.append(event)
                
                return events
                
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    logger.info("No adverse events found")
                    return []
                raise
    
    def _parse_event(self, result: dict) -> Optional[AdverseEvent]:
        """Parse FAERS API result into AdverseEvent object"""
        try:
            # Extract drug name
            patient = result.get("patient", {})
            drugs = patient.get("drug", [])
            drug_name = drugs[0].get("medicinalproduct", "Unknown") if drugs else "Unknown"
            
            # Extract reactions
            reactions = patient.get("reaction", [])
            reaction_list = [r.get("reactionmeddrapt", "") for r in reactions]
            reaction = ", ".join(reaction_list[:3]) if reaction_list else "Unknown"
            
            # Extract outcome
            serious = result.get("serious", "")
            outcome_code = result.get("seriousnessdeath") or result.get("seriousnesshospitalization")
            
            outcome = "Death" if result.get("seriousnessdeath") == "1" else \
                     "Hospitalization" if result.get("seriousnesshospitalization") == "1" else \
                     "Serious" if serious else "Non-serious"
            
            # Extract country
            occurrence_country = result.get("occurcountry", "")
            
            # Extract report date
            receive_date = result.get("receivedate", "")
            if receive_date and len(receive_date) == 8:
                # Format YYYYMMDD to YYYY-MM-DD
                report_date = f"{receive_date[:4]}-{receive_date[4:6]}-{receive_date[6:8]}"
            else:
                report_date = None
            
            # Determine severity
            severity = "Severe" if result.get("seriousnessdeath") == "1" else \
                      "Moderate" if result.get("seriousnesshospitalization") == "1" else \
                      "Mild"
            
            # Report ID
            report_id = result.get("safetyreportid", "")
            
            return AdverseEvent(
                report_id=report_id,
                drug_name=drug_name,
                reaction=reaction,
                outcome=outcome,
                country=occurrence_country,
                report_date=report_date,
                severity=severity,
                source="FDA FAERS"
            )
            
        except Exception as e:
            logger.warning(f"Error parsing adverse event: {str(e)}")
            return None
