"""
Safety & Risk Evaluation Agent
Computes safety scores and risk analysis from adverse events and trial data
"""
from typing import List, Dict, Any
from models.schemas import AdverseEvent, Trial, SafetyAnalysis
from utils.logger import setup_logger
from collections import Counter

logger = setup_logger(__name__)

class RiskAgent:
    """Agent for evaluating safety and risk"""
    
    def __init__(self):
        # Severity weights
        self.severity_weights = {
            "Mild": 1,
            "Moderate": 3,
            "Severe": 7
        }
        
        # Outcome weights
        self.outcome_weights = {
            "Death": 10,
            "Hospitalization": 7,
            "Life-threatening": 8,
            "Disability": 6,
            "Serious": 5,
            "Non-serious": 1
        }
    
    def evaluate_safety(self, adverse_events: List[AdverseEvent], 
                       trials: List[Trial]) -> SafetyAnalysis:
        """
        Evaluate safety and compute risk score
        
        Args:
            adverse_events: List of adverse events
            trials: List of trials (for additional context)
            
        Returns:
            SafetyAnalysis object with risk assessment
        """
        logger.info(f"Evaluating safety with {len(adverse_events)} adverse events")
        
        if not adverse_events:
            return self._create_no_data_analysis()
        
        # Count serious events
        serious_events = sum(1 for e in adverse_events 
                           if e.severity in ["Severe", "Moderate"])
        
        # Count deaths
        deaths = sum(1 for e in adverse_events if "Death" in (e.outcome or ""))
        
        # Calculate risk score (0-10)
        risk_score = self._calculate_risk_score(adverse_events)
        
        # Determine risk label
        risk_label = self._get_risk_label(risk_score)
        
        # Generate safety summary
        safety_summary = self._generate_safety_summary(
            adverse_events, risk_score, serious_events, deaths
        )
        
        # Extract warnings
        warnings = self._extract_warnings(adverse_events)
        
        # Identify black box warnings (serious/fatal events)
        black_box_warnings = self._identify_black_box_warnings(adverse_events)
        
        analysis = SafetyAnalysis(
            risk_score=round(risk_score, 2),
            risk_label=risk_label,
            safety_summary=safety_summary,
            adverse_events_count=len(adverse_events),
            serious_events_count=serious_events,
            warnings=warnings,
            black_box_warnings=black_box_warnings,
            death_reports=deaths
        )
        
        logger.info(f"Safety evaluation complete: Risk Score = {risk_score:.2f} ({risk_label})")
        return analysis
    
    def _calculate_risk_score(self, events: List[AdverseEvent]) -> float:
        """Calculate overall risk score (0-10)"""
        if not events:
            return 0.0
        
        total_score = 0
        max_possible_score = 0
        
        for event in events:
            # Get severity weight
            severity_weight = self.severity_weights.get(event.severity, 2)
            
            # Get outcome weight
            outcome_weight = self.outcome_weights.get(event.outcome, 1)
            
            # Combined score
            event_score = (severity_weight + outcome_weight) / 2
            total_score += event_score
            max_possible_score += 10
        
        # Normalize to 0-10 scale
        if max_possible_score > 0:
            normalized_score = (total_score / len(events))
        else:
            normalized_score = 0
        
        # Cap at 10
        return min(normalized_score, 10.0)
    
    def _get_risk_label(self, risk_score: float) -> str:
        """Convert risk score to label"""
        if risk_score >= 7:
            return "High"
        elif risk_score >= 4:
            return "Medium"
        else:
            return "Low"
    
    def _generate_safety_summary(self, events: List[AdverseEvent], 
                                 risk_score: float, serious_events: int,
                                 deaths: int) -> str:
        """Generate human-readable safety summary"""
        total_events = len(events)
        
        # Count most common reactions
        reactions = [e.reaction for e in events if e.reaction]
        reaction_counts = Counter(reactions)
        top_reactions = reaction_counts.most_common(5)
        
        summary_parts = [
            f"Analysis of {total_events} adverse event reports reveals a {self._get_risk_label(risk_score).lower()} risk profile (score: {risk_score:.1f}/10)."
        ]
        
        if serious_events > 0:
            serious_pct = (serious_events / total_events) * 100
            summary_parts.append(
                f"{serious_events} serious adverse events reported ({serious_pct:.1f}% of total)."
            )
        
        if deaths > 0:
            summary_parts.append(
                f"⚠️ {deaths} death(s) reported in association with this intervention."
            )
        
        if top_reactions:
            top_3 = [r[0] for r in top_reactions[:3]]
            summary_parts.append(
                f"Most common reactions: {', '.join(top_3)}."
            )
        
        return " ".join(summary_parts)
    
    def _extract_warnings(self, events: List[AdverseEvent]) -> List[str]:
        """Extract general warnings from adverse events"""
        warnings = []
        
        # Count events by severity
        severe_count = sum(1 for e in events if e.severity == "Severe")
        moderate_count = sum(1 for e in events if e.severity == "Moderate")
        
        if severe_count > 5:
            warnings.append(f"High number of severe adverse events reported ({severe_count})")
        
        if moderate_count > 20:
            warnings.append(f"Elevated number of moderate adverse events ({moderate_count})")
        
        # Check for specific serious outcomes
        hospitalizations = sum(1 for e in events if "Hospitalization" in (e.outcome or ""))
        if hospitalizations > 10:
            warnings.append(f"Significant hospitalization reports ({hospitalizations})")
        
        # Check reaction patterns
        reactions = [e.reaction.lower() for e in events if e.reaction]
        
        serious_keywords = ["cardiac", "liver", "renal", "respiratory", "seizure", 
                          "stroke", "failure", "arrest"]
        
        for keyword in serious_keywords:
            matching = sum(1 for r in reactions if keyword in r)
            if matching > 5:
                warnings.append(f"Multiple reports of {keyword}-related events ({matching})")
        
        return warnings
    
    def _identify_black_box_warnings(self, events: List[AdverseEvent]) -> List[str]:
        """Identify critical warnings that should be highlighted"""
        black_box = []
        
        # Death reports
        death_count = sum(1 for e in events if "Death" in (e.outcome or ""))
        if death_count > 0:
            black_box.append(f"🛑 FATAL OUTCOMES: {death_count} death(s) reported")
        
        # Life-threatening events
        life_threatening = sum(1 for e in events 
                             if "life-threatening" in (e.outcome or "").lower())
        if life_threatening > 0:
            black_box.append(f"⚠️ Life-threatening events: {life_threatening} reported")
        
        # Organ failure
        reactions = [e.reaction.lower() for e in events if e.reaction]
        organ_failure = sum(1 for r in reactions if "failure" in r)
        if organ_failure > 5:
            black_box.append(f"⚠️ Organ failure events: {organ_failure} reported")
        
        # Cardiac events
        cardiac = sum(1 for r in reactions if "cardiac" in r or "heart" in r)
        if cardiac > 10:
            black_box.append(f"⚠️ Cardiac events: {cardiac} reported")
        
        return black_box
    
    def _create_no_data_analysis(self) -> SafetyAnalysis:
        """Create analysis when no adverse event data available"""
        return SafetyAnalysis(
            risk_score=0.0,
            risk_label="Unknown",
            safety_summary="No adverse event data available for analysis.",
            adverse_events_count=0,
            serious_events_count=0,
            warnings=["No safety data available"],
            black_box_warnings=[],
            death_reports=0
        )
