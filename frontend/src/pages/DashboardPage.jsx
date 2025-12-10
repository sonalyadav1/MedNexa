import React, { useState } from 'react';
import { useAnalysisStore } from '../store/store';
import { useNavigate } from 'react-router-dom';
import LoadingSpinner from '../components/LoadingSpinner';
import Alert from '../components/Alert';
import TrialsTable from '../components/TrialsTable';
import PapersTable from '../components/PapersTable';
import SafetyPanel from '../components/SafetyPanel';
import ChartsPanel from '../components/ChartsPanel';
import InsightsPanel from '../components/InsightsPanel';
import { 
  BeakerIcon, 
  DocumentTextIcon, 
  ExclamationTriangleIcon, 
  ChartBarIcon,
  ShieldCheckIcon,
  LightBulbIcon
} from '@heroicons/react/24/outline';

const DashboardPage = () => {
  const navigate = useNavigate();
  const { currentAnalysis, isLoading } = useAnalysisStore();
  const [activeTab, setActiveTab] = useState('overview');

  if (!currentAnalysis && !isLoading) {
    return (
      <div className="text-center py-12">
        <Alert
          type="info"
          title="No Analysis Data"
          message="Please perform a search from the home page to view results."
        />
        <button
          onClick={() => navigate('/')}
          className="mt-4 btn-primary"
        >
          Go to Home
        </button>
      </div>
    );
  }

  if (isLoading) {
    return <LoadingSpinner size="xl" text="Loading analysis results..." />;
  }

  // Calculate stats
  const trialsCount = currentAnalysis?.trials?.length || 0;
  const papersCount = currentAnalysis?.papers?.length || 0;
  const adverseEventsCount = currentAnalysis?.safety?.adverse_events_count || 0;
  const riskScore = currentAnalysis?.safety?.risk_score || 0;
  const riskLabel = currentAnalysis?.safety?.risk_label || 'N/A';

  const tabs = [
    { id: 'overview', name: 'Overview', count: null },
    { id: 'trials', name: 'Clinical Trials', count: trialsCount },
    { id: 'literature', name: 'Literature', count: papersCount },
    { id: 'safety', name: 'Safety Analysis', count: adverseEventsCount },
    { id: 'insights', name: 'Insights', count: null },
  ];

  // Stats cards data
  const statsCards = [
    {
      title: 'Clinical Trials',
      value: trialsCount,
      icon: BeakerIcon,
      color: 'bg-blue-500',
      bgColor: 'bg-blue-50',
      textColor: 'text-blue-600'
    },
    {
      title: 'Research Papers',
      value: papersCount,
      icon: DocumentTextIcon,
      color: 'bg-green-500',
      bgColor: 'bg-green-50',
      textColor: 'text-green-600'
    },
    {
      title: 'Adverse Events',
      value: adverseEventsCount,
      icon: ExclamationTriangleIcon,
      color: 'bg-yellow-500',
      bgColor: 'bg-yellow-50',
      textColor: 'text-yellow-600'
    },
    {
      title: 'Risk Score',
      value: `${riskScore.toFixed(1)}/10`,
      subtitle: riskLabel,
      icon: ShieldCheckIcon,
      color: riskScore < 4 ? 'bg-green-500' : riskScore < 7 ? 'bg-yellow-500' : 'bg-red-500',
      bgColor: riskScore < 4 ? 'bg-green-50' : riskScore < 7 ? 'bg-yellow-50' : 'bg-red-50',
      textColor: riskScore < 4 ? 'text-green-600' : riskScore < 7 ? 'text-yellow-600' : 'text-red-600'
    }
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="card">
        <div className="flex justify-between items-start">
          <div>
            <h1 className="text-2xl font-bold text-gray-900 mb-2">
              Analysis Dashboard
            </h1>
            <div className="text-sm text-gray-600 space-y-1">
              {currentAnalysis.structured_query?.condition && (
                <p>
                  <span className="font-semibold">Condition:</span>{' '}
                  {currentAnalysis.structured_query.condition}
                </p>
              )}
              {currentAnalysis.structured_query?.intervention && (
                <p>
                  <span className="font-semibold">Intervention:</span>{' '}
                  {currentAnalysis.structured_query.intervention}
                </p>
              )}
              <p className="text-xs text-gray-400">
                Analysis performed at: {new Date(currentAnalysis.timestamp).toLocaleString()}
              </p>
            </div>
          </div>
          <button
            onClick={() => navigate('/report')}
            className="btn-primary"
          >
            Generate Report
          </button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {statsCards.map((stat, index) => {
          const Icon = stat.icon;
          return (
            <div key={index} className={`card ${stat.bgColor} border-l-4 ${stat.color.replace('bg-', 'border-')}`}>
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">{stat.title}</p>
                  <p className={`text-3xl font-bold ${stat.textColor}`}>{stat.value}</p>
                  {stat.subtitle && (
                    <p className={`text-sm font-medium ${stat.textColor}`}>{stat.subtitle}</p>
                  )}
                </div>
                <div className={`p-3 rounded-full ${stat.color}`}>
                  <Icon className="h-6 w-6 text-white" />
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Tabs */}
      <div className="border-b border-gray-200">
        <nav className="-mb-px flex space-x-8 overflow-x-auto">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`
                whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm
                ${
                  activeTab === tab.id
                    ? 'border-primary-500 text-primary-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }
              `}
            >
              {tab.name}
              {tab.count !== null && tab.count > 0 && (
                <span className="ml-2 py-0.5 px-2 rounded-full text-xs bg-gray-100">
                  {tab.count}
                </span>
              )}
            </button>
          ))}
        </nav>
      </div>

      {/* Tab Content */}
      <div className="mt-6">
        {activeTab === 'overview' && (
          <div className="space-y-6">
            <ChartsPanel analysis={currentAnalysis} />
            <InsightsPanel insights={currentAnalysis.combined_insights} />
          </div>
        )}

        {activeTab === 'trials' && (
          <TrialsTable trials={currentAnalysis.trials} />
        )}

        {activeTab === 'literature' && (
          <PapersTable papers={currentAnalysis.papers} />
        )}

        {activeTab === 'safety' && (
          <SafetyPanel safety={currentAnalysis.safety} />
        )}

        {activeTab === 'insights' && (
          <InsightsPanel insights={currentAnalysis.combined_insights} />
        )}
      </div>
    </div>
  );
};

export default DashboardPage;
