import React from 'react';
import { useAnalysisStore } from '../store/store';
import Alert from '../components/Alert';

const ComparisonPage = () => {
  const { currentAnalysis } = useAnalysisStore();

  if (!currentAnalysis) {
    return (
      <div className="text-center py-12">
        <Alert
          type="info"
          title="No Analysis Data"
          message="Please perform a search first to compare trials."
        />
      </div>
    );
  }

  const comparison = currentAnalysis.comparison;

  return (
    <div className="space-y-6">
      <div className="card">
        <h1 className="text-2xl font-bold mb-4">Trial Comparison</h1>
        <p className="text-gray-600">
          Comparative analysis of {comparison.trial_count} clinical trials
        </p>
      </div>

      {/* Efficacy Summary */}
      <div className="card">
        <h2 className="text-xl font-semibold mb-4">Efficacy Summary</h2>
        <p className="text-gray-700">{comparison.efficacy_summary}</p>
      </div>

      {/* Common Interventions */}
      {comparison.common_interventions.length > 0 && (
        <div className="card">
          <h2 className="text-xl font-semibold mb-4">Common Interventions</h2>
          <div className="flex flex-wrap gap-2">
            {comparison.common_interventions.map((intervention, index) => (
              <span
                key={index}
                className="px-3 py-1 bg-primary-100 text-primary-800 rounded-full text-sm"
              >
                {intervention}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Common Conditions */}
      {comparison.common_conditions.length > 0 && (
        <div className="card">
          <h2 className="text-xl font-semibold mb-4">Common Conditions</h2>
          <div className="flex flex-wrap gap-2">
            {comparison.common_conditions.map((condition, index) => (
              <span
                key={index}
                className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm"
              >
                {condition}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Phase Distribution */}
      {Object.keys(comparison.phase_distribution).length > 0 && (
        <div className="card">
          <h2 className="text-xl font-semibold mb-4">Phase Distribution</h2>
          <div className="space-y-2">
            {Object.entries(comparison.phase_distribution).map(([phase, count]) => (
              <div key={phase} className="flex items-center">
                <span className="w-32 text-sm font-medium">{phase}</span>
                <div className="flex-1 bg-gray-200 rounded-full h-6 relative">
                  <div
                    className="bg-primary-600 h-6 rounded-full flex items-center justify-end pr-2"
                    style={{
                      width: `${(count / comparison.trial_count) * 100}%`,
                    }}
                  >
                    <span className="text-white text-xs font-semibold">{count}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Country Distribution */}
      {Object.keys(comparison.country_distribution).length > 0 && (
        <div className="card">
          <h2 className="text-xl font-semibold mb-4">Geographic Distribution</h2>
          <div className="space-y-2">
            {Object.entries(comparison.country_distribution)
              .slice(0, 10)
              .map(([country, count]) => (
                <div key={country} className="flex items-center">
                  <span className="w-40 text-sm font-medium truncate">{country}</span>
                  <div className="flex-1 bg-gray-200 rounded-full h-6 relative">
                    <div
                      className="bg-blue-600 h-6 rounded-full flex items-center justify-end pr-2"
                      style={{
                        width: `${(count / comparison.trial_count) * 100}%`,
                      }}
                    >
                      <span className="text-white text-xs font-semibold">{count}</span>
                    </div>
                  </div>
                </div>
              ))}
          </div>
        </div>
      )}

      {/* Enrollment Statistics */}
      <div className="card">
        <h2 className="text-xl font-semibold mb-4">Enrollment Statistics</h2>
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
          <div>
            <p className="text-sm text-gray-600">Total</p>
            <p className="text-2xl font-bold text-primary-600">
              {comparison.enrollment_stats.total?.toLocaleString()}
            </p>
          </div>
          <div>
            <p className="text-sm text-gray-600">Mean</p>
            <p className="text-2xl font-bold">
              {comparison.enrollment_stats.mean?.toFixed(0)}
            </p>
          </div>
          <div>
            <p className="text-sm text-gray-600">Median</p>
            <p className="text-2xl font-bold">
              {comparison.enrollment_stats.median?.toFixed(0)}
            </p>
          </div>
          <div>
            <p className="text-sm text-gray-600">Min</p>
            <p className="text-2xl font-bold">{comparison.enrollment_stats.min}</p>
          </div>
          <div>
            <p className="text-sm text-gray-600">Max</p>
            <p className="text-2xl font-bold">{comparison.enrollment_stats.max}</p>
          </div>
        </div>
      </div>

      {/* Design Differences */}
      {comparison.design_differences.length > 0 && (
        <div className="card">
          <h2 className="text-xl font-semibold mb-4">Key Design Differences</h2>
          <ul className="space-y-2">
            {comparison.design_differences.map((diff, index) => (
              <li key={index} className="flex items-start">
                <span className="text-primary-600 mr-2">•</span>
                <span className="text-gray-700">{diff}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default ComparisonPage;
