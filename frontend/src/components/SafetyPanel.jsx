import React from 'react';
import { ShieldExclamationIcon, ExclamationTriangleIcon } from '@heroicons/react/24/outline';

const SafetyPanel = ({ safety }) => {
  if (!safety) {
    return (
      <div className="card">
        <p className="text-gray-500 text-center py-8">No safety data available</p>
      </div>
    );
  }

  const getRiskColor = (label) => {
    switch (label.toLowerCase()) {
      case 'high':
        return 'text-red-600 bg-red-50 border-red-200';
      case 'medium':
        return 'text-yellow-600 bg-yellow-50 border-yellow-200';
      case 'low':
        return 'text-green-600 bg-green-50 border-green-200';
      default:
        return 'text-gray-600 bg-gray-50 border-gray-200';
    }
  };

  return (
    <div className="space-y-6">
      {/* Risk Score */}
      <div className={`card border-2 ${getRiskColor(safety.risk_label)}`}>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-2xl font-bold">Risk Assessment</h2>
          <ShieldExclamationIcon className="h-12 w-12" />
        </div>
        
        <div className="flex items-end gap-4 mb-4">
          <div className="text-6xl font-bold">{safety.risk_score.toFixed(1)}</div>
          <div className="text-2xl font-semibold mb-2">/10</div>
          <div className="text-2xl font-semibold mb-2 ml-4">
            ({safety.risk_label})
          </div>
        </div>

        <div className="w-full bg-gray-200 rounded-full h-4 mb-4">
          <div
            className={`h-4 rounded-full ${
              safety.risk_label === 'High' ? 'bg-red-600' :
              safety.risk_label === 'Medium' ? 'bg-yellow-600' :
              'bg-green-600'
            }`}
            style={{ width: `${(safety.risk_score / 10) * 100}%` }}
          ></div>
        </div>

        <p className="text-gray-700">{safety.safety_summary}</p>
      </div>

      {/* Statistics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="card bg-blue-50">
          <p className="text-sm text-gray-600 mb-1">Total Adverse Events</p>
          <p className="text-3xl font-bold text-blue-600">
            {safety.adverse_events_count.toLocaleString()}
          </p>
        </div>

        <div className="card bg-orange-50">
          <p className="text-sm text-gray-600 mb-1">Serious Events</p>
          <p className="text-3xl font-bold text-orange-600">
            {safety.serious_events_count.toLocaleString()}
          </p>
        </div>

        <div className="card bg-red-50">
          <p className="text-sm text-gray-600 mb-1">Death Reports</p>
          <p className="text-3xl font-bold text-red-600">
            {safety.death_reports.toLocaleString()}
          </p>
        </div>
      </div>

      {/* Black Box Warnings */}
      {safety.black_box_warnings && safety.black_box_warnings.length > 0 && (
        <div className="card bg-red-50 border-2 border-red-200">
          <div className="flex items-start">
            <ExclamationTriangleIcon className="h-6 w-6 text-red-600 mr-3 mt-1 flex-shrink-0" />
            <div className="flex-1">
              <h3 className="text-lg font-semibold mb-3 text-red-900">
                Critical Warnings
              </h3>
              <ul className="space-y-2">
                {safety.black_box_warnings.map((warning, index) => (
                  <li key={index} className="flex items-start">
                    <span className="text-red-600 mr-2 mt-1">⚠️</span>
                    <span className="text-gray-800 font-medium">{warning}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      )}

      {/* General Warnings */}
      {safety.warnings && safety.warnings.length > 0 && (
        <div className="card bg-yellow-50 border border-yellow-200">
          <div className="flex items-start">
            <ExclamationTriangleIcon className="h-6 w-6 text-yellow-600 mr-3 mt-1 flex-shrink-0" />
            <div className="flex-1">
              <h3 className="text-lg font-semibold mb-3 text-yellow-900">
                Safety Warnings
              </h3>
              <ul className="space-y-2">
                {safety.warnings.map((warning, index) => (
                  <li key={index} className="flex items-start">
                    <span className="text-yellow-600 mr-2 mt-1">•</span>
                    <span className="text-gray-800">{warning}</span>
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

export default SafetyPanel;
