"""
Pydantic models for data validation and serialization
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class QueryIntent(BaseModel):
    """Structured query intent"""
    condition: Optional[str] = None
    intervention: Optional[str] = None
    phase: Optional[List[str]] = None
    country: Optional[List[str]] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    max_results: int = 50
    additional_filters: Optional[Dict[str, Any]] = None

class TrialStatus(str, Enum):
    RECRUITING = "Recruiting"
    ACTIVE = "Active, not recruiting"
    COMPLETED = "Completed"
    TERMINATED = "Terminated"
    WITHDRAWN = "Withdrawn"
    SUSPENDED = "Suspended"
    UNKNOWN = "Unknown"

class Trial(BaseModel):
    """Standardized clinical trial model"""
    nct_id: str
    title: str
    condition: List[str]
    intervention: List[str]
    phase: Optional[str] = None
    status: str
    enrollment: Optional[int] = None
    start_date: Optional[str] = None
    completion_date: Optional[str] = None
    sponsor: Optional[str] = None
    country: List[str] = []
    summary: Optional[str] = None
    source: str = "ClinicalTrials.gov"
    url: Optional[str] = None
    outcomes: Optional[List[str]] = None

class Paper(BaseModel):
    """Scientific paper model"""
    pmid: Optional[str] = None
    title: str
    authors: List[str] = []
    journal: Optional[str] = None
    publication_date: Optional[str] = None
    abstract: Optional[str] = None
    doi: Optional[str] = None
    url: Optional[str] = None
    keywords: List[str] = []
    citation_count: Optional[int] = None

class AdverseEvent(BaseModel):
    """Adverse event report model"""
    report_id: Optional[str] = None
    drug_name: str
    reaction: str
    outcome: Optional[str] = None
    country: Optional[str] = None
    report_date: Optional[str] = None
    severity: Optional[str] = None
    source: str = "FAERS"

class SafetyAnalysis(BaseModel):
    """Safety and risk analysis result"""
    risk_score: float = Field(ge=0, le=10)
    risk_label: str  # low/medium/high
    safety_summary: str
    adverse_events_count: int
    serious_events_count: int
    warnings: List[str] = []
    black_box_warnings: List[str] = []
    death_reports: int = 0

class ComparisonResult(BaseModel):
    """Trial comparison result"""
    trial_count: int
    common_interventions: List[str]
    common_conditions: List[str]
    phase_distribution: Dict[str, int]
    country_distribution: Dict[str, int]
    enrollment_stats: Dict[str, Any]
    efficacy_summary: str
    design_differences: List[str]
    risk_comparison: Dict[str, Any]

class InsightSummary(BaseModel):
    """AI-generated insights"""
    overview: str
    key_findings: List[str]
    patterns: List[str]
    recommendations: List[str]
    gaps: List[str]

class AnalysisRequest(BaseModel):
    """Analysis request model"""
    query: str
    filters: Optional[Dict[str, Any]] = None
    include_literature: bool = True
    include_safety: bool = True
    max_trials: int = 50

class AnalysisResponse(BaseModel):
    """Complete analysis response"""
    structured_query: QueryIntent
    trials: List[Trial]
    papers: List[Paper]
    safety: Optional[SafetyAnalysis] = None
    combined_insights: InsightSummary
    comparison: Optional[ComparisonResult] = None
    charts: Dict[str, Any] = {}
    timestamp: datetime = Field(default_factory=datetime.now)

class ComparisonRequest(BaseModel):
    """Comparison request model"""
    trial_ids: List[str]
    compare_by: List[str] = ["phase", "enrollment", "outcomes", "safety"]

class ReportRequest(BaseModel):
    """Report generation request"""
    analysis_data: AnalysisResponse
    report_title: str = "MedNexa Research Report"
    include_charts: bool = True
    include_references: bool = True
