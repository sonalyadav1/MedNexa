import React, { useState } from 'react';

const TrialsTable = ({ trials }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');

  if (!trials || trials.length === 0) {
    return (
      <div className="card">
        <p className="text-gray-500 text-center py-8">No trials found</p>
      </div>
    );
  }

  // Filter trials
  const filteredTrials = trials.filter((trial) => {
    const matchesSearch =
      trial.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      trial.nct_id.toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesStatus = statusFilter === 'all' || trial.status === statusFilter;

    return matchesSearch && matchesStatus;
  });

  const statuses = ['all', ...new Set(trials.map((t) => t.status))];

  return (
    <div className="space-y-4">
      {/* Filters */}
      <div className="card">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <input
            type="text"
            placeholder="Search by title or NCT ID..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="input-field"
          />
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="input-field"
          >
            {statuses.map((status) => (
              <option key={status} value={status}>
                {status === 'all' ? 'All Statuses' : status}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Results Count */}
      <div className="text-sm text-gray-600">
        Showing {filteredTrials.length} of {trials.length} trials
      </div>

      {/* Trials List */}
      <div className="space-y-4">
        {filteredTrials.map((trial) => (
          <div key={trial.nct_id} className="card hover:shadow-lg transition-shadow">
            <div className="flex justify-between items-start mb-3">
              <h3 className="text-lg font-semibold text-gray-900 flex-1">
                {trial.title}
              </h3>
              <span className={`ml-4 px-3 py-1 rounded-full text-xs font-semibold whitespace-nowrap ${
                trial.status === 'Completed' ? 'bg-green-100 text-green-800' :
                trial.status === 'Recruiting' ? 'bg-blue-100 text-blue-800' :
                trial.status === 'Active' ? 'bg-yellow-100 text-yellow-800' :
                'bg-gray-100 text-gray-800'
              }`}>
                {trial.status}
              </span>
            </div>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm mb-3">
              <div>
                <span className="text-gray-600">NCT ID:</span>
                <a
                  href={trial.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="block text-primary-600 hover:underline font-medium"
                >
                  {trial.nct_id}
                </a>
              </div>
              {trial.phase && (
                <div>
                  <span className="text-gray-600">Phase:</span>
                  <p className="font-medium">{trial.phase.replace('_', ' ')}</p>
                </div>
              )}
              {trial.enrollment && (
                <div>
                  <span className="text-gray-600">Enrollment:</span>
                  <p className="font-medium">{trial.enrollment.toLocaleString()}</p>
                </div>
              )}
              {trial.sponsor && (
                <div>
                  <span className="text-gray-600">Sponsor:</span>
                  <p className="font-medium truncate" title={trial.sponsor}>
                    {trial.sponsor}
                  </p>
                </div>
              )}
            </div>

            {trial.condition && trial.condition.length > 0 && (
              <div className="mb-2">
                <span className="text-sm text-gray-600">Conditions: </span>
                <div className="flex flex-wrap gap-1 mt-1">
                  {trial.condition.slice(0, 3).map((cond, idx) => (
                    <span
                      key={idx}
                      className="px-2 py-1 bg-purple-100 text-purple-800 rounded text-xs"
                    >
                      {cond}
                    </span>
                  ))}
                  {trial.condition.length > 3 && (
                    <span className="px-2 py-1 bg-gray-100 text-gray-600 rounded text-xs">
                      +{trial.condition.length - 3} more
                    </span>
                  )}
                </div>
              </div>
            )}

            {trial.intervention && trial.intervention.length > 0 && (
              <div className="mb-2">
                <span className="text-sm text-gray-600">Interventions: </span>
                <div className="flex flex-wrap gap-1 mt-1">
                  {trial.intervention.slice(0, 3).map((int, idx) => (
                    <span
                      key={idx}
                      className="px-2 py-1 bg-blue-100 text-blue-800 rounded text-xs"
                    >
                      {int}
                    </span>
                  ))}
                  {trial.intervention.length > 3 && (
                    <span className="px-2 py-1 bg-gray-100 text-gray-600 rounded text-xs">
                      +{trial.intervention.length - 3} more
                    </span>
                  )}
                </div>
              </div>
            )}

            {trial.country && trial.country.length > 0 && (
              <div className="text-sm text-gray-600">
                <span className="font-medium">Countries:</span> {trial.country.slice(0, 5).join(', ')}
                {trial.country.length > 5 && ` +${trial.country.length - 5} more`}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default TrialsTable;
