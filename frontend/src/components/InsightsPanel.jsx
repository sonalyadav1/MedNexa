import React from 'react';
import { 
  LightBulbIcon, 
  ChartBarIcon, 
  ExclamationTriangleIcon,
  CheckCircleIcon 
} from '@heroicons/react/24/outline';

const InsightsPanel = ({ insights }) => {
  if (!insights) {
    return null;
  }

  return (
    <div className="space-y-6">
      {/* Overview */}
      <div className="card">
        <div className="flex items-start">
          <ChartBarIcon className="h-6 w-6 text-primary-600 mr-3 mt-1 flex-shrink-0" />
          <div>
            <h3 className="text-lg font-semibold mb-2">Overview</h3>
            <p className="text-gray-700">{insights.overview}</p>
          </div>
        </div>
      </div>

      {/* Key Findings */}
      {insights.key_findings && insights.key_findings.length > 0 && (
        <div className="card">
          <div className="flex items-start">
            <CheckCircleIcon className="h-6 w-6 text-green-600 mr-3 mt-1 flex-shrink-0" />
            <div className="flex-1">
              <h3 className="text-lg font-semibold mb-3">Key Findings</h3>
              <ul className="space-y-2">
                {insights.key_findings.map((finding, index) => (
                  <li key={index} className="flex items-start">
                    <span className="text-green-600 mr-2 mt-1">•</span>
                    <span className="text-gray-700">{finding}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      )}

      {/* Patterns */}
      {insights.patterns && insights.patterns.length > 0 && (
        <div className="card">
          <div className="flex items-start">
            <LightBulbIcon className="h-6 w-6 text-yellow-600 mr-3 mt-1 flex-shrink-0" />
            <div className="flex-1">
              <h3 className="text-lg font-semibold mb-3">Identified Patterns</h3>
              <ul className="space-y-2">
                {insights.patterns.map((pattern, index) => (
                  <li key={index} className="flex items-start">
                    <span className="text-yellow-600 mr-2 mt-1">•</span>
                    <span className="text-gray-700">{pattern}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      )}

      {/* Recommendations */}
      {insights.recommendations && insights.recommendations.length > 0 && (
        <div className="card bg-primary-50 border border-primary-200">
          <div className="flex items-start">
            <CheckCircleIcon className="h-6 w-6 text-primary-600 mr-3 mt-1 flex-shrink-0" />
            <div className="flex-1">
              <h3 className="text-lg font-semibold mb-3 text-primary-900">Recommendations</h3>
              <ul className="space-y-2">
                {insights.recommendations.map((rec, index) => (
                  <li key={index} className="flex items-start">
                    <span className="text-primary-600 mr-2 mt-1">•</span>
                    <span className="text-gray-800">{rec}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      )}

      {/* Research Gaps */}
      {insights.gaps && insights.gaps.length > 0 && (
        <div className="card bg-red-50 border border-red-200">
          <div className="flex items-start">
            <ExclamationTriangleIcon className="h-6 w-6 text-red-600 mr-3 mt-1 flex-shrink-0" />
            <div className="flex-1">
              <h3 className="text-lg font-semibold mb-3 text-red-900">Research Gaps</h3>
              <ul className="space-y-2">
                {insights.gaps.map((gap, index) => (
                  <li key={index} className="flex items-start">
                    <span className="text-red-600 mr-2 mt-1">•</span>
                    <span className="text-gray-800">{gap}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default InsightsPanel;
