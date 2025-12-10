"""
Report Generation Agent
Creates PDF reports with charts, tables, and analysis
"""
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.platypus import Frame, PageTemplate
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from io import BytesIO
from typing import List
from datetime import datetime
import os

from models.schemas import AnalysisResponse, Trial, Paper, SafetyAnalysis
from utils.logger import setup_logger

logger = setup_logger(__name__)

class ReportAgent:
    """Agent for generating PDF reports"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1e3a8a'),
            spaceAfter=30,
            alignment=TA_CENTER
        ))
        
        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='Subtitle',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#64748b'),
            spaceAfter=20,
            alignment=TA_CENTER
        ))
        
        # Section header
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#1e40af'),
            spaceAfter=12,
            spaceBefore=20
        ))
    
    async def generate_report(self, analysis: AnalysisResponse, 
                            title: str = "MedNexa Research Report",
                            include_charts: bool = True,
                            include_references: bool = True) -> BytesIO:
        """
        Generate PDF report from analysis data
        
        Args:
            analysis: Complete analysis response
            title: Report title
            include_charts: Whether to include charts and statistics
            include_references: Whether to include references section
            
        Returns:
            BytesIO object containing PDF
        """
        logger.info(f"Generating PDF report (charts={include_charts}, references={include_references})")
        
        # Create PDF buffer
        buffer = BytesIO()
        
        # Create document
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Build story (content)
        story = []
        
        # Cover page
        story.extend(self._create_cover_page(title, analysis))
        story.append(PageBreak())
        
        # Executive Summary
        story.extend(self._create_executive_summary(analysis))
        story.append(PageBreak())
        
        # Query Details
        story.extend(self._create_query_section(analysis))
        
        # Charts Section (if enabled)
        if include_charts and analysis.comparison:
            story.extend(self._create_charts_section(analysis))
            story.append(PageBreak())
        
        # Trials Section
        story.extend(self._create_trials_section(analysis.trials))
        story.append(PageBreak())
        
        # Literature Section
        if analysis.papers:
            story.extend(self._create_literature_section(analysis.papers))
            story.append(PageBreak())
        
        # Safety Analysis
        if analysis.safety:
            story.extend(self._create_safety_section(analysis.safety))
            story.append(PageBreak())
        
        # Comparison Analysis
        if analysis.comparison:
            story.extend(self._create_comparison_section(analysis.comparison))
            story.append(PageBreak())
        
        # Insights & Recommendations
        story.extend(self._create_insights_section(analysis.combined_insights))
        
        # References Section (if enabled)
        if include_references:
            story.append(PageBreak())
            story.extend(self._create_references_section(analysis))
        
        # Build PDF
        doc.build(story)
        
        # Get PDF from buffer
        buffer.seek(0)
        
        logger.info("PDF report generated successfully")
        return buffer
    
    def _create_cover_page(self, title: str, analysis: AnalysisResponse) -> List:
        """Create cover page"""
        elements = []
        
        # Title
        elements.append(Spacer(1, 2*inch))
        elements.append(Paragraph(title, self.styles['CustomTitle']))
        
        # Subtitle
        subtitle = f"Pharmaceutical Research Analysis Report"
        elements.append(Paragraph(subtitle, self.styles['Subtitle']))
        
        elements.append(Spacer(1, 0.5*inch))
        
        # Date
        date_text = f"Generated: {datetime.now().strftime('%B %d, %Y')}"
        elements.append(Paragraph(date_text, self.styles['Normal']))
        
        # Query summary
        if analysis.structured_query.condition or analysis.structured_query.intervention:
            elements.append(Spacer(1, 1*inch))
            query_parts = []
            if analysis.structured_query.condition:
                query_parts.append(f"Condition: {analysis.structured_query.condition}")
            if analysis.structured_query.intervention:
                query_parts.append(f"Intervention: {analysis.structured_query.intervention}")
            
            query_text = "<br/>".join(query_parts)
            elements.append(Paragraph(query_text, self.styles['Normal']))
        
        return elements
    
    def _create_executive_summary(self, analysis: AnalysisResponse) -> List:
        """Create executive summary section"""
        elements = []
        
        elements.append(Paragraph("Executive Summary", self.styles['SectionHeader']))
        
        # Overview
        elements.append(Paragraph(analysis.combined_insights.overview, self.styles['Normal']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Key statistics table
        stats_data = [
            ['Metric', 'Count'],
            ['Clinical Trials', str(len(analysis.trials))],
            ['Scientific Publications', str(len(analysis.papers))],
            ['Adverse Events', str(analysis.safety.adverse_events_count if analysis.safety else 0)],
            ['Countries Represented', str(len(analysis.comparison.country_distribution) if analysis.comparison else 0)]
        ]
        
        stats_table = Table(stats_data, colWidths=[3*inch, 2*inch])
        stats_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(stats_table)
        elements.append(Spacer(1, 0.3*inch))
        
        return elements
    
    def _create_query_section(self, analysis: AnalysisResponse) -> List:
        """Create query details section"""
        elements = []
        
        elements.append(Paragraph("Query Parameters", self.styles['SectionHeader']))
        
        query = analysis.structured_query
        
        query_data = [
            ['Parameter', 'Value'],
        ]
        
        if query.condition:
            query_data.append(['Condition', query.condition])
        if query.intervention:
            query_data.append(['Intervention', query.intervention])
        if query.phase:
            query_data.append(['Phase', ', '.join(query.phase)])
        if query.country:
            query_data.append(['Countries', ', '.join(query.country)])
        if query.start_date:
            query_data.append(['Start Date', query.start_date])
        if query.end_date:
            query_data.append(['End Date', query.end_date])
        
        query_table = Table(query_data, colWidths=[2*inch, 4*inch])
        query_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey)
        ]))
        
        elements.append(query_table)
        elements.append(Spacer(1, 0.3*inch))
        
        return elements
    
    def _create_trials_section(self, trials: List[Trial]) -> List:
        """Create clinical trials section"""
        elements = []
        
        elements.append(Paragraph(f"Clinical Trials Analysis ({len(trials)} trials)", 
                                 self.styles['SectionHeader']))
        
        if not trials:
            elements.append(Paragraph("No clinical trials found.", self.styles['Normal']))
            return elements
        
        # Show top 10 trials
        for i, trial in enumerate(trials[:10], 1):
            # Trial title
            trial_title = f"{i}. {trial.title}"
            elements.append(Paragraph(trial_title, self.styles['Heading3']))
            
            # Trial details
            details = []
            details.append(f"<b>NCT ID:</b> {trial.nct_id}")
            details.append(f"<b>Status:</b> {trial.status}")
            if trial.phase:
                details.append(f"<b>Phase:</b> {trial.phase}")
            if trial.enrollment:
                details.append(f"<b>Enrollment:</b> {trial.enrollment}")
            if trial.sponsor:
                details.append(f"<b>Sponsor:</b> {trial.sponsor}")
            
            details_text = " | ".join(details)
            elements.append(Paragraph(details_text, self.styles['Normal']))
            
            elements.append(Spacer(1, 0.1*inch))
        
        if len(trials) > 10:
            elements.append(Paragraph(f"<i>... and {len(trials) - 10} more trials</i>", 
                                     self.styles['Normal']))
        
        return elements
    
    def _create_literature_section(self, papers: List[Paper]) -> List:
        """Create literature review section"""
        elements = []
        
        elements.append(Paragraph(f"Scientific Literature ({len(papers)} publications)", 
                                 self.styles['SectionHeader']))
        
        # Show top 10 papers
        for i, paper in enumerate(papers[:10], 1):
            # Paper title
            paper_title = f"{i}. {paper.title}"
            elements.append(Paragraph(paper_title, self.styles['Heading3']))
            
            # Paper details
            details = []
            if paper.authors:
                authors_str = ", ".join(paper.authors[:3])
                if len(paper.authors) > 3:
                    authors_str += " et al."
                details.append(f"<b>Authors:</b> {authors_str}")
            if paper.journal:
                details.append(f"<b>Journal:</b> {paper.journal}")
            if paper.publication_date:
                details.append(f"<b>Date:</b> {paper.publication_date}")
            if paper.pmid:
                details.append(f"<b>PMID:</b> {paper.pmid}")
            
            details_text = " | ".join(details)
            elements.append(Paragraph(details_text, self.styles['Normal']))
            
            elements.append(Spacer(1, 0.1*inch))
        
        if len(papers) > 10:
            elements.append(Paragraph(f"<i>... and {len(papers) - 10} more publications</i>", 
                                     self.styles['Normal']))
        
        return elements
    
    def _create_safety_section(self, safety: SafetyAnalysis) -> List:
        """Create safety analysis section"""
        elements = []
        
        elements.append(Paragraph("Safety & Risk Analysis", self.styles['SectionHeader']))
        
        # Risk score
        risk_color = colors.green if safety.risk_score < 4 else \
                    colors.orange if safety.risk_score < 7 else colors.red
        
        risk_text = f"<b>Risk Score:</b> {safety.risk_score:.1f}/10 ({safety.risk_label})"
        elements.append(Paragraph(risk_text, self.styles['Heading3']))
        
        elements.append(Spacer(1, 0.1*inch))
        
        # Safety summary
        elements.append(Paragraph(safety.safety_summary, self.styles['Normal']))
        
        elements.append(Spacer(1, 0.2*inch))
        
        # Statistics table
        safety_data = [
            ['Metric', 'Count'],
            ['Total Adverse Events', str(safety.adverse_events_count)],
            ['Serious Events', str(safety.serious_events_count)],
            ['Death Reports', str(safety.death_reports)],
        ]
        
        safety_table = Table(safety_data, colWidths=[3*inch, 2*inch])
        safety_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#dc2626')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey)
        ]))
        
        elements.append(safety_table)
        elements.append(Spacer(1, 0.2*inch))
        
        # Warnings
        if safety.warnings:
            elements.append(Paragraph("<b>Warnings:</b>", self.styles['Heading3']))
            for warning in safety.warnings:
                elements.append(Paragraph(f"• {warning}", self.styles['Normal']))
        
        # Black box warnings
        if safety.black_box_warnings:
            elements.append(Spacer(1, 0.1*inch))
            elements.append(Paragraph("<b>Critical Warnings:</b>", self.styles['Heading3']))
            for warning in safety.black_box_warnings:
                elements.append(Paragraph(f"• {warning}", self.styles['Normal']))
        
        return elements
    
    def _create_comparison_section(self, comparison) -> List:
        """Create comparison analysis section"""
        elements = []
        
        elements.append(Paragraph("Comparative Analysis", self.styles['SectionHeader']))
        
        # Efficacy summary
        elements.append(Paragraph(comparison.efficacy_summary, self.styles['Normal']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Design differences
        if comparison.design_differences:
            elements.append(Paragraph("<b>Key Design Differences:</b>", self.styles['Heading3']))
            for diff in comparison.design_differences:
                elements.append(Paragraph(f"• {diff}", self.styles['Normal']))
        
        return elements
    
    def _create_insights_section(self, insights) -> List:
        """Create insights and recommendations section"""
        elements = []
        
        elements.append(Paragraph("Key Insights & Recommendations", self.styles['SectionHeader']))
        
        # Key findings
        if insights.key_findings:
            elements.append(Paragraph("<b>Key Findings:</b>", self.styles['Heading3']))
            for finding in insights.key_findings:
                elements.append(Paragraph(f"• {finding}", self.styles['Normal']))
            elements.append(Spacer(1, 0.1*inch))
        
        # Patterns
        if insights.patterns:
            elements.append(Paragraph("<b>Identified Patterns:</b>", self.styles['Heading3']))
            for pattern in insights.patterns:
                elements.append(Paragraph(f"• {pattern}", self.styles['Normal']))
            elements.append(Spacer(1, 0.1*inch))
        
        # Recommendations
        if insights.recommendations:
            elements.append(Paragraph("<b>Recommendations:</b>", self.styles['Heading3']))
            for rec in insights.recommendations:
                elements.append(Paragraph(f"• {rec}", self.styles['Normal']))
            elements.append(Spacer(1, 0.1*inch))
        
        # Gaps
        if insights.gaps:
            elements.append(Paragraph("<b>Research Gaps:</b>", self.styles['Heading3']))
            for gap in insights.gaps:
                elements.append(Paragraph(f"• {gap}", self.styles['Normal']))
        
        return elements
    
    def _create_charts_section(self, analysis: AnalysisResponse) -> List:
        """Create charts and statistics section with visual data representation"""
        elements = []
        
        elements.append(Paragraph("Statistical Overview & Charts", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.2*inch))
        
        comparison = analysis.comparison
        
        # Phase Distribution Table (visual representation)
        if comparison and comparison.phase_distribution:
            elements.append(Paragraph("<b>Trial Phase Distribution:</b>", self.styles['Heading3']))
            
            phase_data = [['Phase', 'Count', 'Percentage', 'Visual']]
            total = sum(comparison.phase_distribution.values())
            
            for phase, count in sorted(comparison.phase_distribution.items()):
                pct = (count / total * 100) if total > 0 else 0
                bar = '█' * int(pct / 5) + '░' * (20 - int(pct / 5))
                phase_data.append([phase, str(count), f"{pct:.1f}%", bar])
            
            phase_table = Table(phase_data, colWidths=[1.5*inch, 1*inch, 1*inch, 2.5*inch])
            phase_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (1, 1), (2, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
                ('TEXTCOLOR', (3, 1), (3, -1), colors.HexColor('#3b82f6'))
            ]))
            elements.append(phase_table)
            elements.append(Spacer(1, 0.3*inch))
        
        # Country Distribution
        if comparison and comparison.country_distribution:
            elements.append(Paragraph("<b>Geographic Distribution (Top 10):</b>", self.styles['Heading3']))
            
            country_data = [['Country', 'Trials', 'Percentage', 'Visual']]
            total = sum(comparison.country_distribution.values())
            
            sorted_countries = sorted(comparison.country_distribution.items(), 
                                      key=lambda x: x[1], reverse=True)[:10]
            
            for country, count in sorted_countries:
                pct = (count / total * 100) if total > 0 else 0
                bar = '█' * int(pct / 5) + '░' * (20 - int(pct / 5))
                country_data.append([country[:20], str(count), f"{pct:.1f}%", bar])
            
            country_table = Table(country_data, colWidths=[2*inch, 0.8*inch, 1*inch, 2.2*inch])
            country_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#059669')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (1, 1), (2, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ecfdf5')),
                ('TEXTCOLOR', (3, 1), (3, -1), colors.HexColor('#059669'))
            ]))
            elements.append(country_table)
            elements.append(Spacer(1, 0.3*inch))
        
        # Enrollment Statistics
        if comparison and comparison.enrollment_stats:
            elements.append(Paragraph("<b>Enrollment Statistics:</b>", self.styles['Heading3']))
            
            stats = comparison.enrollment_stats
            enroll_data = [
                ['Metric', 'Value'],
                ['Total Enrollment', f"{stats.get('total', 0):,}"],
                ['Mean per Trial', f"{stats.get('mean', 0):,.0f}"],
                ['Median per Trial', f"{stats.get('median', 0):,.0f}"],
                ['Minimum', f"{stats.get('min', 0):,}"],
                ['Maximum', f"{stats.get('max', 0):,}"]
            ]
            
            enroll_table = Table(enroll_data, colWidths=[2.5*inch, 2*inch])
            enroll_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#7c3aed')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (1, 1), (1, -1), 'RIGHT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f5f3ff'))
            ]))
            elements.append(enroll_table)
        
        return elements
    
    def _create_references_section(self, analysis: AnalysisResponse) -> List:
        """Create references and citations section"""
        elements = []
        
        elements.append(Paragraph("References & Citations", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.2*inch))
        
        ref_num = 1
        
        # Clinical Trial References
        if analysis.trials:
            elements.append(Paragraph("<b>Clinical Trial Sources:</b>", self.styles['Heading3']))
            elements.append(Spacer(1, 0.1*inch))
            
            for trial in analysis.trials[:15]:  # Limit to 15 references
                ref_text = f"[{ref_num}] {trial.title}. ClinicalTrials.gov Identifier: {trial.nct_id}. "
                if trial.sponsor:
                    ref_text += f"Sponsor: {trial.sponsor}. "
                if trial.url:
                    ref_text += f"Available at: {trial.url}"
                
                elements.append(Paragraph(ref_text, self.styles['Normal']))
                elements.append(Spacer(1, 0.05*inch))
                ref_num += 1
            
            if len(analysis.trials) > 15:
                elements.append(Paragraph(f"<i>... and {len(analysis.trials) - 15} additional trial references</i>", 
                                         self.styles['Normal']))
            elements.append(Spacer(1, 0.2*inch))
        
        # Literature References
        if analysis.papers:
            elements.append(Paragraph("<b>Scientific Literature:</b>", self.styles['Heading3']))
            elements.append(Spacer(1, 0.1*inch))
            
            for paper in analysis.papers[:15]:  # Limit to 15 references
                authors_str = ""
                if paper.authors:
                    if len(paper.authors) <= 3:
                        authors_str = ", ".join(paper.authors)
                    else:
                        authors_str = f"{paper.authors[0]} et al."
                
                ref_text = f"[{ref_num}] {authors_str}. {paper.title}. "
                if paper.journal:
                    ref_text += f"<i>{paper.journal}</i>. "
                if paper.publication_date:
                    ref_text += f"({paper.publication_date}). "
                if paper.pmid:
                    ref_text += f"PMID: {paper.pmid}. "
                if paper.doi:
                    ref_text += f"DOI: {paper.doi}"
                
                elements.append(Paragraph(ref_text, self.styles['Normal']))
                elements.append(Spacer(1, 0.05*inch))
                ref_num += 1
            
            if len(analysis.papers) > 15:
                elements.append(Paragraph(f"<i>... and {len(analysis.papers) - 15} additional publication references</i>", 
                                         self.styles['Normal']))
            elements.append(Spacer(1, 0.2*inch))
        
        # Data Sources
        elements.append(Paragraph("<b>Data Sources:</b>", self.styles['Heading3']))
        elements.append(Spacer(1, 0.1*inch))
        
        sources = [
            "ClinicalTrials.gov - U.S. National Library of Medicine (https://clinicaltrials.gov)",
            "PubMed - National Center for Biotechnology Information (https://pubmed.ncbi.nlm.nih.gov)",
            "FDA Adverse Event Reporting System (FAERS) - U.S. Food and Drug Administration"
        ]
        
        for source in sources:
            elements.append(Paragraph(f"• {source}", self.styles['Normal']))
        
        elements.append(Spacer(1, 0.3*inch))
        
        # Disclaimer
        elements.append(Paragraph("<b>Disclaimer:</b>", self.styles['Heading3']))
        disclaimer = ("This report is generated automatically based on publicly available data sources. "
                     "It is intended for research and informational purposes only and should not be used "
                     "as a substitute for professional medical advice, diagnosis, or treatment. Always "
                     "consult qualified healthcare professionals for medical decisions.")
        elements.append(Paragraph(disclaimer, self.styles['Normal']))
        
        return elements
