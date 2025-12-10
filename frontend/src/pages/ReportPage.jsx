import React, { useState } from 'react';
import { useAnalysisStore } from '../store/store';
import { reportAPI } from '../api/api';
import toast from 'react-hot-toast';
import Alert from '../components/Alert';
import LoadingSpinner from '../components/LoadingSpinner';
import { DocumentArrowDownIcon } from '@heroicons/react/24/outline';

const ReportPage = () => {
  const { currentAnalysis } = useAnalysisStore();
  const [isGenerating, setIsGenerating] = useState(false);
  const [reportTitle, setReportTitle] = useState('MedNexa Research Report');
  const [includeCharts, setIncludeCharts] = useState(true);
  const [includeReferences, setIncludeReferences] = useState(true);

  const handleGenerateReport = async () => {
    if (!currentAnalysis) {
      toast.error('No analysis data available');
      return;
    }

    setIsGenerating(true);
    
    try {
      const pdfBlob = await reportAPI.generateReport(
        currentAnalysis, 
        reportTitle,
        includeCharts,
        includeReferences
      );
      
      // Create download link
      const url = window.URL.createObjectURL(new Blob([pdfBlob]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `${reportTitle.replace(/\s+/g, '_')}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
      
      toast.success('Report generated successfully!');
    } catch (error) {
      console.error('Report generation error:', error);
      toast.error('Failed to generate report');
    } finally {
      setIsGenerating(false);
    }
  };

  const handleDownloadSample = async () => {
    setIsGenerating(true);
    
    try {
      const pdfBlob = await reportAPI.downloadSampleReport();
      
      const url = window.URL.createObjectURL(new Blob([pdfBlob]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'mednexa_sample_report.pdf');
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
      
      toast.success('Sample report downloaded!');
    } catch (error) {
      console.error('Sample report error:', error);
      toast.error('Failed to download sample report');
    } finally {
      setIsGenerating(false);
    }
  };

  if (!currentAnalysis) {
    return (
      <div className="space-y-6">
        <div className="card">
          <h1 className="text-2xl font-bold mb-4">Report Generation</h1>
          <Alert
            type="info"
            title="No Analysis Data"
            message="Perform an analysis first to generate a custom report, or download a sample report below."
          />
          
          <div className="mt-6">
            <button
              onClick={handleDownloadSample}
              disabled={isGenerating}
              className="btn-primary"
            >
              <DocumentArrowDownIcon className="h-5 w-5 inline mr-2" />
              Download Sample Report
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="card">
        <h1 className="text-2xl font-bold mb-4">Generate PDF Report</h1>
        <p className="text-gray-600">
          Create a comprehensive PDF report with all analysis results, charts, and insights.
        </p>
      </div>

      {/* Report Configuration */}
      <div className="card">
        <h2 className="text-xl font-semibold mb-4">Report Configuration</h2>
        
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Report Title
            </label>
            <input
              type="text"
              value={reportTitle}
              onChange={(e) => setReportTitle(e.target.value)}
              className="input-field"
              placeholder="Enter report title"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="flex items-center">
              <input
                type="checkbox"
                id="include_charts"
                checked={includeCharts}
                onChange={(e) => setIncludeCharts(e.target.checked)}
                className="h-4 w-4 text-primary-600 rounded border-gray-300"
              />
              <label htmlFor="include_charts" className="ml-2 text-sm text-gray-700">
                Include Charts & Statistics
              </label>
            </div>
            
            <div className="flex items-center">
              <input
                type="checkbox"
                id="include_references"
                checked={includeReferences}
                onChange={(e) => setIncludeReferences(e.target.checked)}
                className="h-4 w-4 text-primary-600 rounded border-gray-300"
              />
              <label htmlFor="include_references" className="ml-2 text-sm text-gray-700">
                Include References & Citations
              </label>
            </div>
          </div>
        </div>
      </div>

      {/* Report Preview */}
      <div className="card">
        <h2 className="text-xl font-semibold mb-4">Report Contents</h2>
        
        <div className="space-y-3">
          <div className="flex items-center text-sm">
            <div className="w-2 h-2 bg-green-500 rounded-full mr-3"></div>
            <span>Executive Summary</span>
            <span className="ml-auto text-gray-500">Included</span>
          </div>
          
          <div className="flex items-center text-sm">
            <div className="w-2 h-2 bg-green-500 rounded-full mr-3"></div>
            <span>Clinical Trials ({currentAnalysis.trials.length})</span>
            <span className="ml-auto text-gray-500">Included</span>
          </div>
          
          <div className="flex items-center text-sm">
            <div className="w-2 h-2 bg-green-500 rounded-full mr-3"></div>
            <span>Scientific Literature ({currentAnalysis.papers.length})</span>
            <span className="ml-auto text-gray-500">Included</span>
          </div>
          
          {currentAnalysis.safety && (
            <div className="flex items-center text-sm">
              <div className="w-2 h-2 bg-green-500 rounded-full mr-3"></div>
              <span>Safety Analysis</span>
              <span className="ml-auto text-gray-500">Included</span>
            </div>
          )}
          
          <div className="flex items-center text-sm">
            <div className="w-2 h-2 bg-green-500 rounded-full mr-3"></div>
            <span>Comparative Analysis</span>
            <span className="ml-auto text-gray-500">Included</span>
          </div>
          
          <div className="flex items-center text-sm">
            <div className="w-2 h-2 bg-green-500 rounded-full mr-3"></div>
            <span>Insights & Recommendations</span>
            <span className="ml-auto text-gray-500">Included</span>
          </div>
        </div>
      </div>

      {/* Generate Button */}
      <div className="card">
        {isGenerating ? (
          <LoadingSpinner text="Generating PDF report..." />
        ) : (
          <button
            onClick={handleGenerateReport}
            className="w-full btn-primary py-3 text-lg"
          >
            <DocumentArrowDownIcon className="h-6 w-6 inline mr-2" />
            Generate & Download Report
          </button>
        )}
      </div>
    </div>
  );
};

export default ReportPage;
