"""
Report Generation Router
Handles PDF report generation
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from models.schemas import ReportRequest, AnalysisResponse
from orchestrator.orchestrator import Orchestrator
from utils.logger import setup_logger
from io import BytesIO

logger = setup_logger(__name__)
router = APIRouter()

orchestrator = Orchestrator()

@router.post("/generate-report")
async def generate_report(request: ReportRequest):
    """
    Generate PDF report from analysis data
    
    Accepts complete analysis data and generates a comprehensive PDF report including:
    - Executive summary
    - Trial listings
    - Literature review
    - Safety analysis
    - Comparison charts
    - Insights and recommendations
    
    Returns PDF file
    """
    try:
        logger.info("Generating PDF report")
        
        # Generate report
        pdf_buffer = await orchestrator.generate_report(
            request.analysis_data,
            request.report_title
        )
        
        # Return as streaming response
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=mednexa_report.pdf"
            }
        )
        
    except Exception as e:
        logger.error(f"Error generating report: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Report generation failed: {str(e)}"
        )

@router.get("/download-sample-report")
async def download_sample_report():
    """
    Download a sample MedNexa report
    
    Useful for testing and demonstration purposes
    """
    try:
        from models.schemas import (
            AnalysisResponse, QueryIntent, InsightSummary,
            ComparisonResult, SafetyAnalysis
        )
        from datetime import datetime
        
        # Create sample data
        sample_query = QueryIntent(
            condition="cancer",
            intervention="immunotherapy",
            max_results=50
        )
        
        sample_insights = InsightSummary(
            overview="Sample analysis of cancer immunotherapy trials.",
            key_findings=["Finding 1", "Finding 2"],
            patterns=["Pattern 1"],
            recommendations=["Recommendation 1"],
            gaps=["Gap 1"]
        )
        
        sample_comparison = ComparisonResult(
            trial_count=10,
            common_interventions=["Drug A", "Drug B"],
            common_conditions=["Cancer"],
            phase_distribution={"PHASE_2": 5, "PHASE_3": 5},
            country_distribution={"United States": 7, "Canada": 3},
            enrollment_stats={
                "total": 1000,
                "mean": 100,
                "median": 90,
                "min": 20,
                "max": 500
            },
            efficacy_summary="Sample efficacy summary.",
            design_differences=[],
            risk_comparison={}
        )
        
        sample_safety = SafetyAnalysis(
            risk_score=5.0,
            risk_label="Medium",
            safety_summary="Sample safety analysis.",
            adverse_events_count=50,
            serious_events_count=10,
            warnings=["Warning 1"],
            black_box_warnings=[],
            death_reports=0
        )
        
        sample_analysis = AnalysisResponse(
            structured_query=sample_query,
            trials=[],
            papers=[],
            safety=sample_safety,
            combined_insights=sample_insights,
            comparison=sample_comparison,
            charts={},
            timestamp=datetime.now()
        )
        
        # Generate report
        pdf_buffer = await orchestrator.generate_report(
            sample_analysis,
            "MedNexa Sample Report"
        )
        
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={
                "Content-Disposition": "attachment; filename=mednexa_sample_report.pdf"
            }
        )
        
    except Exception as e:
        logger.error(f"Error generating sample report: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Sample report generation failed: {str(e)}"
        )
