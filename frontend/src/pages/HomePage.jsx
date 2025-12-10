import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { MagnifyingGlassIcon, BeakerIcon, DocumentMagnifyingGlassIcon } from '@heroicons/react/24/outline';
import { analysisAPI } from '../api/api';
import { useAnalysisStore } from '../store/store';
import toast from 'react-hot-toast';
import LoadingSpinner from '../components/LoadingSpinner';

const HomePage = () => {
  const navigate = useNavigate();
  const { setAnalysis, setLoading, isLoading } = useAnalysisStore();
  const [query, setQuery] = useState('');

  const exampleQueries = [
    'Find Phase 3 trials for breast cancer immunotherapy',
    'Search for COVID-19 vaccine trials in the United States',
    'Diabetes treatment trials using metformin in 2023',
    'Alzheimer\'s disease clinical trials in Phase 2',
  ];

  const handleSearch = async (searchQuery) => {
    if (!searchQuery.trim()) {
      toast.error('Please enter a search query');
      return;
    }

    setLoading(true);
    
    try {
      const result = await analysisAPI.analyze(searchQuery);
      setAnalysis(result);
      toast.success('Analysis complete!');
      navigate('/dashboard');
    } catch (error) {
      console.error('Analysis error:', error);
      toast.error(error.response?.data?.detail || 'Analysis failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-[calc(100vh-200px)] flex flex-col items-center justify-center">
      {/* Hero Section */}
      <div className="text-center mb-12">
        <h1 className="text-5xl font-bold text-gray-900 mb-4">
          MedNexa
        </h1>
        <p className="text-xl text-gray-600 mb-2">
          Multi-Agent AI Pharma Research Assistant
        </p>
        <p className="text-md text-gray-500">
          End-to-end pharmaceutical research automation powered by AI
        </p>
      </div>

      {/* Search Box */}
      <div className="w-full max-w-3xl mb-8">
        <div className="relative">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSearch(query)}
            placeholder="Ask anything about clinical trials, drugs, or medical research..."
            className="w-full px-6 py-4 text-lg border-2 border-gray-300 rounded-full shadow-lg focus:outline-none focus:border-primary-500 focus:ring-2 focus:ring-primary-200 transition-all"
            disabled={isLoading}
          />
          <button
            onClick={() => handleSearch(query)}
            disabled={isLoading}
            className="absolute right-2 top-1/2 transform -translate-y-1/2 bg-primary-600 hover:bg-primary-700 text-white px-6 py-2 rounded-full transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? (
              <div className="h-5 w-5 animate-spin rounded-full border-2 border-white border-t-transparent"></div>
            ) : (
              <MagnifyingGlassIcon className="h-5 w-5" />
            )}
          </button>
        </div>
      </div>

      {/* Example Queries */}
      <div className="w-full max-w-3xl mb-12">
        <p className="text-sm text-gray-500 mb-3">Try these examples:</p>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {exampleQueries.map((exampleQuery, index) => (
            <button
              key={index}
              onClick={() => setQuery(exampleQuery)}
              className="text-left px-4 py-3 bg-white border border-gray-200 rounded-lg hover:border-primary-300 hover:bg-primary-50 transition-colors text-sm"
              disabled={isLoading}
            >
              {exampleQuery}
            </button>
          ))}
        </div>
      </div>

      {/* Features */}
      <div className="w-full max-w-5xl grid grid-cols-1 md:grid-cols-3 gap-6 mt-12">
        <div className="card text-center">
          <div className="flex justify-center mb-4">
            <BeakerIcon className="h-12 w-12 text-primary-600" />
          </div>
          <h3 className="text-lg font-semibold mb-2">Multi-Source Data</h3>
          <p className="text-sm text-gray-600">
            Aggregates data from ClinicalTrials.gov, PubMed, FDA FAERS, WHO, and EMA
          </p>
        </div>

        <div className="card text-center">
          <div className="flex justify-center mb-4">
            <DocumentMagnifyingGlassIcon className="h-12 w-12 text-primary-600" />
          </div>
          <h3 className="text-lg font-semibold mb-2">AI-Powered Analysis</h3>
          <p className="text-sm text-gray-600">
            Multi-agent system for intelligent data cleaning, safety analysis, and insights
          </p>
        </div>

        <div className="card text-center">
          <div className="flex justify-center mb-4">
            <MagnifyingGlassIcon className="h-12 w-12 text-primary-600" />
          </div>
          <h3 className="text-lg font-semibold mb-2">Comprehensive Reports</h3>
          <p className="text-sm text-gray-600">
            Generate detailed PDF reports with charts, comparisons, and recommendations
          </p>
        </div>
      </div>

      {isLoading && (
        <div className="mt-8">
          <LoadingSpinner size="lg" text="Analyzing data from multiple sources..." />
        </div>
      )}
    </div>
  );
};

export default HomePage;
