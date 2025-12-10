"""
ClinicalTrials.gov Data Retrieval Agent
Fetches trial data from ClinicalTrials.gov API
"""
import aiohttp
from typing import List, Optional, Dict, Any
from models.schemas import Trial, QueryIntent
from utils.logger import setup_logger
import asyncio
import urllib.parse
import ssl
import subprocess
import json

logger = setup_logger(__name__)

class TrialsAgent:
    """Agent for fetching data from ClinicalTrials.gov"""
    
    BASE_URL = "https://clinicaltrials.gov/api/v2/studies"
    
    def __init__(self):
        self.session = None
    
    async def fetch_trials(self, query_intent: QueryIntent) -> List[Trial]:
        """
        Fetch trials from ClinicalTrials.gov API
        
        Args:
            query_intent: Structured query
            
        Returns:
            List of Trial objects
        """
        logger.info("Fetching trials from ClinicalTrials.gov")
        
        try:
            # Build the URL
            page_size = min(query_intent.max_results, 50)
            
            # Build query parts
            query_parts = ["format=json", f"pageSize={page_size}"]
            
            # Add condition search
            if query_intent.condition:
                encoded_cond = urllib.parse.quote(query_intent.condition)
                query_parts.append(f"query.cond={encoded_cond}")
            
            # Add intervention search
            if query_intent.intervention:
                encoded_intr = urllib.parse.quote(query_intent.intervention)
                query_parts.append(f"query.intr={encoded_intr}")
            
            url = f"{self.BASE_URL}?{'&'.join(query_parts)}"
            logger.info(f"Fetching from URL: {url}")
            
            # Use curl via subprocess as fallback since Python HTTP libraries get 403
            try:
                result = await asyncio.create_subprocess_exec(
                    'curl', '-s', '-H', 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                    '-H', 'Accept: application/json',
                    url,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                stdout, stderr = await result.communicate()
                
                if result.returncode == 0 and stdout:
                    data = json.loads(stdout.decode('utf-8'))
                    trials = self._parse_trials(data)
                    logger.info(f"Fetched {len(trials)} trials from ClinicalTrials.gov using curl")
                    return trials
                else:
                    logger.error(f"Curl failed: {stderr.decode('utf-8') if stderr else 'Unknown error'}")
                    return []
                    
            except Exception as curl_error:
                logger.error(f"Curl subprocess failed: {str(curl_error)}")
                # Fall back to aiohttp
                return await self._fetch_with_aiohttp(url, page_size, query_intent)
                
        except Exception as e:
            logger.error(f"Error fetching trials: {str(e)}")
            return []
    
    async def _fetch_with_aiohttp(self, url: str, page_size: int, query_intent: QueryIntent) -> List[Trial]:
        """Fallback method using aiohttp"""
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "application/json",
                "Accept-Language": "en-US,en;q=0.9",
            }
            
            # Create SSL context that doesn't verify certificates (for development)
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            
            timeout = aiohttp.ClientTimeout(total=60)
            connector = aiohttp.TCPConnector(ssl=ssl_context)
            
            async with aiohttp.ClientSession(
                headers=headers, 
                timeout=timeout,
                connector=connector
            ) as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._parse_trials(data)
                    else:
                        logger.error(f"aiohttp failed with status: {response.status}")
                        return []
        except Exception as e:
            logger.error(f"aiohttp fallback failed: {str(e)}")
            return []
    
    def _build_params(self, query_intent: QueryIntent) -> Dict[str, Any]:
        """Build API parameters from query intent"""
        params = {
            "format": "json",
            "pageSize": min(query_intent.max_results, 50)
        }
        
        # Condition search
        if query_intent.condition:
            params["query.cond"] = query_intent.condition
            
        # Intervention/drug search  
        if query_intent.intervention:
            params["query.intr"] = query_intent.intervention
        
        # Add phase filter if specified
        if query_intent.phase:
            phase_filters = []
            for p in query_intent.phase:
                p_upper = p.upper().replace(" ", "")
                if "PHASE" in p_upper:
                    phase_num = p_upper.replace("PHASE_", "").replace("PHASE", "")
                    phase_filters.append(f"PHASE{phase_num}")
                elif p in ["1", "2", "3", "4"]:
                    phase_filters.append(f"PHASE{p}")
            if phase_filters:
                params["filter.phase"] = ",".join(phase_filters)
        
        # Add country filter
        if query_intent.country:
            params["query.locn"] = ",".join(query_intent.country)
        
        logger.info(f"Built API params: {params}")
        return params
    
    def _parse_trials(self, data: Dict[str, Any]) -> List[Trial]:
        """Parse API response into Trial objects"""
        trials = []
        
        studies = data.get("studies", [])
        logger.info(f"Parsing {len(studies)} studies from API response")
        
        for study in studies:
            try:
                protocol = study.get("protocolSection", {})
                identification = protocol.get("identificationModule", {})
                status_module = protocol.get("statusModule", {})
                description = protocol.get("descriptionModule", {})
                conditions = protocol.get("conditionsModule", {})
                design = protocol.get("designModule", {})
                arms = protocol.get("armsInterventionsModule", {})
                sponsor = protocol.get("sponsorCollaboratorsModule", {})
                locations = protocol.get("contactsLocationsModule", {})
                outcomes = protocol.get("outcomesModule", {})
                
                # Extract NCT ID
                nct_id = identification.get("nctId", "")
                
                # Extract title
                title = identification.get("briefTitle", "")
                
                # Extract conditions
                condition_list = conditions.get("conditions", [])
                
                # Extract interventions
                interventions = arms.get("interventions", [])
                intervention_list = [i.get("name", "") for i in interventions]
                
                # Extract phase
                phase_info = design.get("phases", [])
                phase = phase_info[0] if phase_info else None
                
                # Extract status
                overall_status = status_module.get("overallStatus", "Unknown")
                
                # Extract enrollment
                enrollment_info = design.get("enrollmentInfo", {})
                enrollment = enrollment_info.get("count")
                
                # Extract dates
                start_date_struct = status_module.get("startDateStruct", {})
                start_date = start_date_struct.get("date")
                
                completion_date_struct = status_module.get("completionDateStruct", {})
                completion_date = completion_date_struct.get("date")
                
                # Extract sponsor
                lead_sponsor = sponsor.get("leadSponsor", {})
                sponsor_name = lead_sponsor.get("name")
                
                # Extract countries
                location_list = locations.get("locations", [])
                countries = list(set([loc.get("country", "") for loc in location_list if loc.get("country")]))
                
                # Extract summary
                summary = description.get("briefSummary", "")
                
                # Extract URL
                url = f"https://clinicaltrials.gov/study/{nct_id}"
                
                # Extract outcomes
                primary_outcomes = outcomes.get("primaryOutcomes", [])
                outcome_list = [o.get("measure", "") for o in primary_outcomes]
                
                trial = Trial(
                    nct_id=nct_id,
                    title=title,
                    condition=condition_list,
                    intervention=intervention_list,
                    phase=phase,
                    status=overall_status,
                    enrollment=enrollment,
                    start_date=start_date,
                    completion_date=completion_date,
                    sponsor=sponsor_name,
                    country=countries,
                    summary=summary,
                    source="ClinicalTrials.gov",
                    url=url,
                    outcomes=outcome_list
                )
                
                trials.append(trial)
                
            except Exception as e:
                logger.warning(f"Error parsing trial: {str(e)}")
                continue
        
        return trials
