"""
Data Cleaning & Normalization Agent
Removes duplicates, standardizes fields, and unifies data formats
"""
from typing import List, Dict, Any
from models.schemas import Trial, Paper, AdverseEvent
from utils.logger import setup_logger
import re
from collections import defaultdict

logger = setup_logger(__name__)

class CleanAgent:
    """Agent for cleaning and normalizing medical data"""
    
    def __init__(self):
        # Mapping for phase normalization
        self.phase_mapping = {
            "phase 1": "PHASE_1",
            "phase i": "PHASE_1",
            "phase 2": "PHASE_2",
            "phase ii": "PHASE_2",
            "phase 3": "PHASE_3",
            "phase iii": "PHASE_3",
            "phase 4": "PHASE_4",
            "phase iv": "PHASE_4",
            "early phase 1": "EARLY_PHASE_1",
            "n/a": "NA"
        }
        
        # Status normalization
        self.status_mapping = {
            "recruiting": "Recruiting",
            "active, not recruiting": "Active",
            "completed": "Completed",
            "terminated": "Terminated",
            "withdrawn": "Withdrawn",
            "suspended": "Suspended",
            "enrolling by invitation": "Recruiting"
        }
    
    def clean_trials(self, trials: List[Trial]) -> List[Trial]:
        """
        Clean and normalize trial data
        
        Args:
            trials: List of raw trials from various sources
            
        Returns:
            List of cleaned and deduplicated trials
        """
        logger.info(f"Cleaning {len(trials)} trials")
        
        # Remove duplicates based on NCT ID
        unique_trials = self._deduplicate_trials(trials)
        
        # Normalize each trial
        cleaned_trials = []
        for trial in unique_trials:
            cleaned_trial = self._normalize_trial(trial)
            cleaned_trials.append(cleaned_trial)
        
        logger.info(f"Cleaned to {len(cleaned_trials)} unique trials")
        return cleaned_trials
    
    def clean_papers(self, papers: List[Paper]) -> List[Paper]:
        """
        Clean and normalize paper data
        
        Args:
            papers: List of papers
            
        Returns:
            List of cleaned and deduplicated papers
        """
        logger.info(f"Cleaning {len(papers)} papers")
        
        # Remove duplicates based on PMID or DOI
        unique_papers = self._deduplicate_papers(papers)
        
        # Normalize each paper
        cleaned_papers = []
        for paper in unique_papers:
            cleaned_paper = self._normalize_paper(paper)
            cleaned_papers.append(cleaned_paper)
        
        logger.info(f"Cleaned to {len(cleaned_papers)} unique papers")
        return cleaned_papers
    
    def clean_adverse_events(self, events: List[AdverseEvent]) -> List[AdverseEvent]:
        """
        Clean and normalize adverse event data
        
        Args:
            events: List of adverse events
            
        Returns:
            List of cleaned events
        """
        logger.info(f"Cleaning {len(events)} adverse events")
        
        # Remove duplicates
        unique_events = self._deduplicate_events(events)
        
        # Normalize severity and outcomes
        cleaned_events = []
        for event in unique_events:
            cleaned_event = self._normalize_event(event)
            cleaned_events.append(cleaned_event)
        
        logger.info(f"Cleaned to {len(cleaned_events)} unique adverse events")
        return cleaned_events
    
    def _deduplicate_trials(self, trials: List[Trial]) -> List[Trial]:
        """Remove duplicate trials"""
        seen_ids = set()
        unique = []
        
        for trial in trials:
            if trial.nct_id not in seen_ids:
                seen_ids.add(trial.nct_id)
                unique.append(trial)
        
        return unique
    
    def _deduplicate_papers(self, papers: List[Paper]) -> List[Paper]:
        """Remove duplicate papers"""
        seen_ids = set()
        unique = []
        
        for paper in papers:
            identifier = paper.pmid or paper.doi or paper.title
            if identifier not in seen_ids:
                seen_ids.add(identifier)
                unique.append(paper)
        
        return unique
    
    def _deduplicate_events(self, events: List[AdverseEvent]) -> List[AdverseEvent]:
        """Remove duplicate adverse events"""
        seen_ids = set()
        unique = []
        
        for event in events:
            identifier = event.report_id or f"{event.drug_name}_{event.reaction}"
            if identifier not in seen_ids:
                seen_ids.add(identifier)
                unique.append(event)
        
        return unique
    
    def _normalize_trial(self, trial: Trial) -> Trial:
        """Normalize a single trial"""
        # Normalize phase
        if trial.phase:
            phase_lower = trial.phase.lower()
            trial.phase = self.phase_mapping.get(phase_lower, trial.phase.upper())
        
        # Normalize status
        if trial.status:
            status_lower = trial.status.lower()
            trial.status = self.status_mapping.get(status_lower, trial.status)
        
        # Clean and normalize conditions
        trial.condition = [self._clean_text(c) for c in trial.condition]
        
        # Clean and normalize interventions
        trial.intervention = [self._clean_text(i) for i in trial.intervention]
        
        # Standardize countries
        trial.country = [self._normalize_country(c) for c in trial.country]
        
        # Clean summary
        if trial.summary:
            trial.summary = self._clean_text(trial.summary)
        
        return trial
    
    def _normalize_paper(self, paper: Paper) -> Paper:
        """Normalize a single paper"""
        # Clean title
        if paper.title:
            paper.title = self._clean_text(paper.title)
        
        # Clean abstract
        if paper.abstract:
            paper.abstract = self._clean_text(paper.abstract)
        
        # Normalize author names
        paper.authors = [self._clean_text(a) for a in paper.authors]
        
        return paper
    
    def _normalize_event(self, event: AdverseEvent) -> AdverseEvent:
        """Normalize adverse event"""
        # Clean drug name
        event.drug_name = self._clean_text(event.drug_name)
        
        # Clean reaction
        event.reaction = self._clean_text(event.reaction)
        
        # Normalize country
        if event.country:
            event.country = self._normalize_country(event.country)
        
        return event
    
    def _clean_text(self, text: str) -> str:
        """Clean text: remove extra whitespace, special characters"""
        if not text:
            return text
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove HTML tags if any
        text = re.sub(r'<[^>]+>', '', text)
        
        # Strip leading/trailing whitespace
        text = text.strip()
        
        return text
    
    def _normalize_country(self, country: str) -> str:
        """Normalize country names"""
        if not country:
            return country
        
        country_mapping = {
            "us": "United States",
            "usa": "United States",
            "united states of america": "United States",
            "uk": "United Kingdom",
            "gb": "United Kingdom",
            "great britain": "United Kingdom"
        }
        
        country_lower = country.lower()
        return country_mapping.get(country_lower, country.title())
    
    def create_unified_dataset(self, trials: List[Trial], papers: List[Paper], 
                              events: List[AdverseEvent]) -> Dict[str, Any]:
        """
        Create a unified dataset with cross-references
        
        Returns:
            Dictionary with unified data and metadata
        """
        logger.info("Creating unified dataset")
        
        # Extract all unique conditions
        all_conditions = set()
        for trial in trials:
            all_conditions.update(trial.condition)
        
        # Extract all unique interventions
        all_interventions = set()
        for trial in trials:
            all_interventions.update(trial.intervention)
        
        # Create intervention-to-trials mapping
        intervention_map = defaultdict(list)
        for trial in trials:
            for intervention in trial.intervention:
                intervention_map[intervention].append(trial.nct_id)
        
        # Create condition-to-trials mapping
        condition_map = defaultdict(list)
        for trial in trials:
            for condition in trial.condition:
                condition_map[condition].append(trial.nct_id)
        
        unified = {
            "trials": trials,
            "papers": papers,
            "adverse_events": events,
            "metadata": {
                "total_trials": len(trials),
                "total_papers": len(papers),
                "total_adverse_events": len(events),
                "unique_conditions": list(all_conditions),
                "unique_interventions": list(all_interventions),
                "condition_map": dict(condition_map),
                "intervention_map": dict(intervention_map)
            }
        }
        
        return unified
