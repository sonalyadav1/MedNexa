"""
WHO ICTRP (International Clinical Trials Registry Platform) Agent
Fetches global trial data from WHO registry
"""
import httpx
from typing import List
from models.schemas import Trial, QueryIntent
from utils.logger import setup_logger
from bs4 import BeautifulSoup

logger = setup_logger(__name__)

class WHOAgent:
    """Agent for fetching data from WHO ICTRP"""
    
    BASE_URL = "https://trialsearch.who.int/api/trials"
    
    def __init__(self):
        pass
    
    async def fetch_trials(self, query_intent: QueryIntent) -> List[Trial]:
        """
        Fetch trials from WHO ICTRP
        
        Args:
            query_intent: Structured query
            
        Returns:
            List of Trial objects
        """
        logger.info("Fetching trials from WHO ICTRP")
        
        try:
            # Build search query
            search_query = self._build_search_query(query_intent)
            
            # Note: WHO ICTRP API requires registration, so we'll simulate/parse
            # In production, you'd use proper API credentials
            
            # For now, return empty list with proper structure
            # In real implementation, you would:
            # 1. Use WHO ICTRP API with credentials
            # 2. Parse the response
            # 3. Convert to Trial objects
            
            logger.info("WHO ICTRP integration ready (requires API credentials)")
            return []
            
        except Exception as e:
            logger.error(f"Error fetching WHO trials: {str(e)}")
            return []
    
    def _build_search_query(self, query_intent: QueryIntent) -> str:
        """Build WHO ICTRP search query"""
        query_parts = []
        
        if query_intent.condition:
            query_parts.append(query_intent.condition)
        
        if query_intent.intervention:
            query_parts.append(query_intent.intervention)
        
        return " AND ".join(query_parts) if query_parts else ""
