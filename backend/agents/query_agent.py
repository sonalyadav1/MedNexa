"""
Query Understanding Agent
Parses natural language queries and extracts structured information
"""
import re
from typing import Dict, Any, List, Optional
from models.schemas import QueryIntent
from utils.logger import setup_logger
import json

logger = setup_logger(__name__)

class QueryAgent:
    """Agent for understanding and parsing user queries"""
    
    def __init__(self):
        self.phase_keywords = {
            "phase 1": ["phase 1", "phase i", "early phase"],
            "phase 2": ["phase 2", "phase ii"],
            "phase 3": ["phase 3", "phase iii", "late phase"],
            "phase 4": ["phase 4", "phase iv", "post-market"]
        }
        
        self.status_keywords = {
            "recruiting": ["recruiting", "enrolling"],
            "active": ["active", "ongoing"],
            "completed": ["completed", "finished"],
        }
    
    def parse_query(self, query: str, filters: Optional[Dict[str, Any]] = None) -> QueryIntent:
        """
        Parse natural language query into structured format
        
        Args:
            query: Natural language query
            filters: Additional filters
            
        Returns:
            QueryIntent: Structured query object
        """
        logger.info(f"Parsing query: {query}")
        
        query_lower = query.lower()
        
        # Extract condition
        condition = self._extract_condition(query_lower, filters)
        
        # Extract intervention/drug
        intervention = self._extract_intervention(query_lower, filters)
        
        # Extract phase
        phase = self._extract_phase(query_lower, filters)
        
        # Extract country
        country = self._extract_country(query_lower, filters)
        
        # Extract date range
        start_date, end_date = self._extract_date_range(query_lower, filters)
        
        # Max results
        max_results = filters.get("max_results", 50) if filters else 50
        
        result = QueryIntent(
            condition=condition,
            intervention=intervention,
            phase=phase,
            country=country,
            start_date=start_date,
            end_date=end_date,
            max_results=max_results,
            additional_filters=filters or {}
        )
        
        logger.info(f"Parsed query intent: {result.model_dump()}")
        return result
    
    def _extract_condition(self, query: str, filters: Optional[Dict]) -> Optional[str]:
        """Extract medical condition from query"""
        if filters and "condition" in filters:
            return filters["condition"]
        
        # Common condition patterns
        condition_patterns = [
            r"(?:for|treating|treatment of|patients with|condition)\s+([a-z\s]+?)(?:\s+(?:using|with|in|trial|study|phase))",
            r"([a-z\s]+?)\s+(?:trial|study|research)",
        ]
        
        # Look for specific disease names FIRST before trying regex patterns
        diseases = ["cancer", "diabetes", "alzheimer", "parkinson", "covid", "heart disease",
                   "hypertension", "asthma", "copd", "depression", "schizophrenia",
                   "breast cancer", "lung cancer", "prostate cancer", "leukemia",
                   "obesity", "arthritis", "hiv", "aids", "hepatitis", "stroke",
                   "epilepsy", "migraine", "anxiety", "bipolar", "ptsd", "adhd",
                   "multiple sclerosis", "crohn", "colitis", "psoriasis", "eczema",
                   "lymphoma", "melanoma", "myeloma", "sarcoma", "glioblastoma"]
        
        for disease in diseases:
            if disease in query:
                return disease
        
        for pattern in condition_patterns:
            match = re.search(pattern, query)
            if match:
                condition = match.group(1).strip()
                # Filter out common words
                if len(condition) > 3 and condition not in ["the", "and", "for", "with"]:
                    return condition
        
        # If still nothing found, use the whole query as condition (for simple queries like "cancer")
        clean_query = query.strip()
        if len(clean_query) > 2 and len(clean_query) < 50:
            # Remove common words
            stop_words = ["search", "find", "show", "get", "for", "the", "a", "an", "trials", "studies", "about"]
            words = clean_query.split()
            filtered = [w for w in words if w.lower() not in stop_words]
            if filtered:
                return " ".join(filtered)
        
        return None
    
    def _extract_intervention(self, query: str, filters: Optional[Dict]) -> Optional[str]:
        """Extract intervention/drug from query"""
        if filters and "intervention" in filters:
            return filters["intervention"]
        
        # Intervention patterns
        intervention_patterns = [
            r"(?:using|with|drug|medication|therapy)\s+([a-z0-9\s\-]+?)(?:\s+(?:for|in|on|phase|trial))",
            r"([a-z0-9\s\-]+?)\s+(?:therapy|treatment|drug|medication)",
        ]
        
        for pattern in intervention_patterns:
            match = re.search(pattern, query)
            if match:
                intervention = match.group(1).strip()
                if len(intervention) > 2:
                    return intervention
        
        return None
    
    def _extract_phase(self, query: str, filters: Optional[Dict]) -> Optional[List[str]]:
        """Extract trial phase from query"""
        if filters and "phase" in filters:
            phase_filter = filters["phase"]
            return [phase_filter] if isinstance(phase_filter, str) else phase_filter
        
        phases = []
        for phase, keywords in self.phase_keywords.items():
            if any(keyword in query for keyword in keywords):
                phases.append(phase.replace(" ", "_").upper())
        
        return phases if phases else None
    
    def _extract_country(self, query: str, filters: Optional[Dict]) -> Optional[List[str]]:
        """Extract country/region from query"""
        if filters and "country" in filters:
            country_filter = filters["country"]
            return [country_filter] if isinstance(country_filter, str) else country_filter
        
        countries = {
            "united states": ["us", "usa", "united states", "america"],
            "united kingdom": ["uk", "united kingdom", "britain"],
            "canada": ["canada", "canadian"],
            "germany": ["germany", "german"],
            "france": ["france", "french"],
            "japan": ["japan", "japanese"],
            "china": ["china", "chinese"],
            "india": ["india", "indian"],
            "australia": ["australia", "australian"]
        }
        
        found_countries = []
        for country, keywords in countries.items():
            if any(keyword in query for keyword in keywords):
                found_countries.append(country.title())
        
        return found_countries if found_countries else None
    
    def _extract_date_range(self, query: str, filters: Optional[Dict]) -> tuple:
        """Extract date range from query"""
        start_date = None
        end_date = None
        
        if filters:
            start_date = filters.get("start_date")
            end_date = filters.get("end_date")
        
        # Look for year patterns
        year_pattern = r"(20\d{2})"
        years = re.findall(year_pattern, query)
        
        if len(years) == 1:
            start_date = f"{years[0]}-01-01"
        elif len(years) >= 2:
            start_date = f"{min(years)}-01-01"
            end_date = f"{max(years)}-12-31"
        
        # Look for relative dates
        if "last year" in query or "past year" in query:
            start_date = "2024-01-01"
            end_date = "2024-12-31"
        elif "last 5 years" in query or "past 5 years" in query:
            start_date = "2020-01-01"
        
        return start_date, end_date
