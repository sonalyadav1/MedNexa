"""
Insight & Comparison Agent
Analyzes trials, finds patterns, generates comparisons and AI-powered insights
"""
from typing import List, Dict, Any
from models.schemas import Trial, Paper, ComparisonResult, InsightSummary
from utils.logger import setup_logger
from collections import Counter, defaultdict
import statistics

logger = setup_logger(__name__)

class InsightAgent:
    """Agent for generating insights and comparisons"""
    
    def __init__(self):
        pass
    
    def generate_comparison(self, trials: List[Trial]) -> ComparisonResult:
        """
        Generate comparison analysis across trials
        
        Args:
            trials: List of trials to compare
            
        Returns:
            ComparisonResult with comparative analysis
        """
        logger.info(f"Generating comparison for {len(trials)} trials")
        
        if not trials:
            return self._create_empty_comparison()
        
        # Extract common interventions
        all_interventions = []
        for trial in trials:
            all_interventions.extend(trial.intervention)
        intervention_counts = Counter(all_interventions)
        common_interventions = [i for i, count in intervention_counts.most_common(10)]
        
        # Extract common conditions
        all_conditions = []
        for trial in trials:
            all_conditions.extend(trial.condition)
        condition_counts = Counter(all_conditions)
        common_conditions = [c for c, count in condition_counts.most_common(10)]
        
        # Phase distribution
        phases = [trial.phase for trial in trials if trial.phase]
        phase_distribution = dict(Counter(phases))
        
        # Country distribution
        all_countries = []
        for trial in trials:
            all_countries.extend(trial.country)
        country_distribution = dict(Counter(all_countries).most_common(15))
        
        # Enrollment statistics
        enrollments = [trial.enrollment for trial in trials if trial.enrollment]
        enrollment_stats = self._calculate_enrollment_stats(enrollments)
        
        # Efficacy summary (simplified AI generation)
        efficacy_summary = self._generate_efficacy_summary(trials)
        
        # Design differences
        design_differences = self._identify_design_differences(trials)
        
        # Risk comparison
        risk_comparison = self._compare_risks(trials)
        
        comparison = ComparisonResult(
            trial_count=len(trials),
            common_interventions=common_interventions,
            common_conditions=common_conditions,
            phase_distribution=phase_distribution,
            country_distribution=country_distribution,
            enrollment_stats=enrollment_stats,
            efficacy_summary=efficacy_summary,
            design_differences=design_differences,
            risk_comparison=risk_comparison
        )
        
        logger.info("Comparison generated successfully")
        return comparison
    
    def generate_insights(self, trials: List[Trial], papers: List[Paper],
                         comparison: ComparisonResult) -> InsightSummary:
        """
        Generate AI-powered insights from all data
        
        Args:
            trials: List of trials
            papers: List of papers
            comparison: Comparison results
            
        Returns:
            InsightSummary with key findings and recommendations
        """
        logger.info("Generating insights")
        
        # Generate overview
        overview = self._generate_overview(trials, papers, comparison)
        
        # Extract key findings
        key_findings = self._extract_key_findings(trials, papers, comparison)
        
        # Identify patterns
        patterns = self._identify_patterns(trials, comparison)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(trials, comparison)
        
        # Identify gaps
        gaps = self._identify_gaps(trials, papers)
        
        insights = InsightSummary(
            overview=overview,
            key_findings=key_findings,
            patterns=patterns,
            recommendations=recommendations,
            gaps=gaps
        )
        
        logger.info("Insights generated successfully")
        return insights
    
    def _calculate_enrollment_stats(self, enrollments: List[int]) -> Dict[str, Any]:
        """Calculate enrollment statistics"""
        if not enrollments:
            return {
                "total": 0,
                "mean": 0,
                "median": 0,
                "min": 0,
                "max": 0
            }
        
        return {
            "total": sum(enrollments),
            "mean": round(statistics.mean(enrollments), 1),
            "median": round(statistics.median(enrollments), 1),
            "min": min(enrollments),
            "max": max(enrollments)
        }
    
    def _generate_efficacy_summary(self, trials: List[Trial]) -> str:
        """Generate efficacy summary from trials"""
        completed = sum(1 for t in trials if t.status == "Completed")
        active = sum(1 for t in trials if t.status in ["Recruiting", "Active"])
        terminated = sum(1 for t in trials if t.status == "Terminated")
        
        summary_parts = []
        
        if completed > 0:
            summary_parts.append(f"{completed} completed trials provide established efficacy data")
        
        if active > 0:
            summary_parts.append(f"{active} ongoing trials are actively collecting data")
        
        if terminated > 0:
            summary_parts.append(f"{terminated} trials were terminated, suggesting potential safety or efficacy concerns")
        
        # Phase analysis
        phase_3_4 = sum(1 for t in trials if t.phase in ["PHASE_3", "PHASE_4"])
        if phase_3_4 > 0:
            summary_parts.append(f"{phase_3_4} late-phase trials indicate mature development stage")
        
        return ". ".join(summary_parts) + "." if summary_parts else "Limited efficacy data available."
    
    def _identify_design_differences(self, trials: List[Trial]) -> List[str]:
        """Identify key design differences across trials"""
        differences = []
        
        # Phase diversity
        phases = set(t.phase for t in trials if t.phase)
        if len(phases) > 1:
            differences.append(f"Trials span {len(phases)} different phases: {', '.join(sorted(phases))}")
        
        # Geographic diversity
        all_countries = set()
        for trial in trials:
            all_countries.update(trial.country)
        if len(all_countries) > 5:
            differences.append(f"Global distribution across {len(all_countries)} countries")
        
        # Enrollment variability
        enrollments = [t.enrollment for t in trials if t.enrollment]
        if enrollments and max(enrollments) > min(enrollments) * 10:
            differences.append(f"Wide enrollment range: {min(enrollments)} to {max(enrollments)} participants")
        
        # Sponsor diversity
        sponsors = set(t.sponsor for t in trials if t.sponsor)
        if len(sponsors) > 3:
            differences.append(f"Multiple sponsors ({len(sponsors)}) indicate broad research interest")
        
        return differences
    
    def _compare_risks(self, trials: List[Trial]) -> Dict[str, Any]:
        """Compare risk profiles across trials"""
        # This is simplified - in production, you'd integrate with safety data
        
        terminated = [t for t in trials if t.status == "Terminated"]
        completed = [t for t in trials if t.status == "Completed"]
        
        return {
            "completed_trials": len(completed),
            "terminated_trials": len(terminated),
            "termination_rate": round(len(terminated) / len(trials) * 100, 1) if trials else 0,
            "status_distribution": dict(Counter(t.status for t in trials))
        }
    
    def _generate_overview(self, trials: List[Trial], papers: List[Paper],
                          comparison: ComparisonResult) -> str:
        """Generate comprehensive overview"""
        parts = [
            f"Analysis of {len(trials)} clinical trials and {len(papers)} scientific publications",
            f"covering {comparison.trial_count} unique interventions",
            f"across {len(comparison.country_distribution)} countries."
        ]
        
        if comparison.common_conditions:
            parts.append(f"Primary focus: {comparison.common_conditions[0]}.")
        
        completed = sum(1 for t in trials if t.status == "Completed")
        if completed > 0:
            parts.append(f"{completed} trials have reported outcomes.")
        
        return " ".join(parts)
    
    def _extract_key_findings(self, trials: List[Trial], papers: List[Paper],
                             comparison: ComparisonResult) -> List[str]:
        """Extract key findings from data"""
        findings = []
        
        # Trial volume finding
        if len(trials) > 20:
            findings.append(f"Extensive research activity with {len(trials)} registered trials")
        elif len(trials) < 5:
            findings.append(f"Limited trial activity with only {len(trials)} registered trials")
        
        # Phase findings
        if comparison.phase_distribution:
            max_phase = max(comparison.phase_distribution.items(), key=lambda x: x[1])
            findings.append(f"Most trials in {max_phase[0]} ({max_phase[1]} trials)")
        
        # Geographic findings
        if comparison.country_distribution:
            top_country = max(comparison.country_distribution.items(), key=lambda x: x[1])
            findings.append(f"{top_country[0]} leads research with {top_country[1]} trials")
        
        # Enrollment findings
        if comparison.enrollment_stats["total"] > 0:
            findings.append(
                f"Total enrollment of {comparison.enrollment_stats['total']:,} participants "
                f"(median: {comparison.enrollment_stats['median']:.0f} per trial)"
            )
        
        # Literature findings
        if papers:
            recent_papers = sum(1 for p in papers 
                              if p.publication_date and p.publication_date.startswith(("2023", "2024", "2025")))
            if recent_papers > 0:
                findings.append(f"{recent_papers} recent publications (2023-2025)")
        
        return findings
    
    def _identify_patterns(self, trials: List[Trial], 
                          comparison: ComparisonResult) -> List[str]:
        """Identify patterns across trials"""
        patterns = []
        
        # Temporal patterns
        recent_trials = sum(1 for t in trials 
                          if t.start_date and t.start_date.startswith(("2023", "2024", "2025")))
        if recent_trials > len(trials) * 0.5:
            patterns.append("Increasing research activity in recent years")
        
        # Status patterns - safely access risk_comparison
        termination_rate = comparison.risk_comparison.get("termination_rate", 0) if comparison.risk_comparison else 0
        if termination_rate > 20:
            patterns.append(f"High termination rate ({termination_rate}%) may indicate challenges")
        
        # Geographic patterns
        if len(comparison.country_distribution) > 10:
            patterns.append("Globally distributed research indicates widespread interest")
        
        # Phase progression
        phases = comparison.phase_distribution
        if phases.get("PHASE3") or phases.get("Phase 3") or phases.get("PHASE_3"):
            if phases.get("PHASE4") or phases.get("Phase 4") or phases.get("PHASE_4"):
                patterns.append("Presence of late-phase trials suggests mature therapeutic development")
        
        return patterns
    
    def _generate_recommendations(self, trials: List[Trial],
                                 comparison: ComparisonResult) -> List[str]:
        """Generate recommendations based on analysis"""
        recommendations = []
        
        # Based on phase distribution - safely access with defaults
        phase_dist = comparison.phase_distribution or {}
        phase1_count = phase_dist.get("PHASE_1", 0) or phase_dist.get("Phase 1", 0) or phase_dist.get("PHASE1", 0) or 0
        phase3_count = phase_dist.get("PHASE_3", 0) or phase_dist.get("Phase 3", 0) or phase_dist.get("PHASE3", 0) or 0
        
        if phase1_count > phase3_count * 2 and phase3_count > 0:
            recommendations.append("Consider monitoring Phase 1 trials for emerging safety signals")
        
        # Based on geographic distribution
        if len(comparison.country_distribution or {}) < 5:
            recommendations.append("Limited geographic diversity - consider expanding to additional regions")
        
        # Based on enrollment - safely access with defaults
        enrollment_stats = comparison.enrollment_stats or {}
        mean_enrollment = enrollment_stats.get("mean", 100)
        if mean_enrollment and mean_enrollment < 50:
            recommendations.append("Small sample sizes - larger trials needed for robust conclusions")
        
        # Based on status
        active_trials = sum(1 for t in trials if t.status in ["Recruiting", "Active", "RECRUITING", "ACTIVE"])
        if trials and active_trials > len(trials) * 0.5:
            recommendations.append("Many active trials - expect significant new data in coming months")
        
        # Literature gap
        completed = sum(1 for t in trials if t.status in ["Completed", "COMPLETED"])
        if completed > 5:
            recommendations.append("Review publications from completed trials for outcome data")
        
        return recommendations
    
    def _identify_gaps(self, trials: List[Trial], papers: List[Paper]) -> List[str]:
        """Identify research gaps"""
        gaps = []
        
        # Phase gaps
        phases_present = set(t.phase for t in trials if t.phase)
        all_phases = {"PHASE_1", "PHASE_2", "PHASE_3", "PHASE_4"}
        missing_phases = all_phases - phases_present
        
        if missing_phases:
            gaps.append(f"Missing trial phases: {', '.join(sorted(missing_phases))}")
        
        # Pediatric trials
        pediatric = sum(1 for t in trials 
                       if any(term in t.title.lower() 
                             for term in ["pediatric", "child", "infant"]))
        if pediatric == 0 and len(trials) > 10:
            gaps.append("No pediatric trials identified")
        
        # Long-term follow-up
        phase_4 = sum(1 for t in trials if t.phase == "PHASE_4")
        if phase_4 == 0 and len(trials) > 10:
            gaps.append("Limited post-market surveillance data (no Phase 4 trials)")
        
        # Publication gap
        completed = sum(1 for t in trials if t.status == "Completed")
        if completed > 0 and len(papers) < completed * 0.3:
            gaps.append("Publication gap - many completed trials lack published results")
        
        return gaps
    
    def _create_empty_comparison(self) -> ComparisonResult:
        """Create empty comparison result"""
        return ComparisonResult(
            trial_count=0,
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
            efficacy_summary="No data available for comparison.",
            design_differences=[],
            risk_comparison={}
        )
