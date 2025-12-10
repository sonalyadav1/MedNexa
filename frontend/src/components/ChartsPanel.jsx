import React from 'react';
import { PieChart, Pie, BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, Cell, ResponsiveContainer } from 'recharts';

const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899', '#14b8a6', '#f97316'];

// Format label names - convert PHASE1 to "Phase 1", ACTIVE_NOT_RECRUITING to "Active"
const formatLabel = (name) => {
  if (!name) return '';
  
  const upperName = name.toUpperCase().trim();
  
  // Handle N/A case
  if (upperName === 'NA' || upperName === 'N/A' || upperName === 'NOT_APPLICABLE') {
    return 'N/A';
  }
  
  // Handle phase names
  if (upperName.includes('PHASE')) {
    // Early Phase 1
    if (upperName.includes('EARLY')) {
      return 'Early Phase 1';
    }
    const match = name.match(/PHASE\s*(\d+)/i);
    if (match) return `Phase ${match[1]}`;
  }
  
  // Handle status names - shorten long ones
  const statusMap = {
    'ACTIVE_NOT_RECRUITING': 'Active',
    'NOT_YET_RECRUITING': 'Not Recruiting',
    'ENROLLING_BY_INVITATION': 'By Invitation',
    'SUSPENDED': 'Suspended',
    'TERMINATED': 'Terminated',
    'COMPLETED': 'Completed',
    'WITHDRAWN': 'Withdrawn',
    'UNKNOWN': 'Unknown',
    'RECRUITING': 'Recruiting',
  };
  
  const normalizedName = upperName.replace(/\s+/g, '_');
  if (statusMap[normalizedName]) return statusMap[normalizedName];
  
  // Default: replace underscores, capitalize first letter of each word
  return name
    .replace(/_/g, ' ')
    .toLowerCase()
    .replace(/\b\w/g, c => c.toUpperCase());
};

// Custom label renderer for pie charts
const renderCustomizedLabel = ({ cx, cy, midAngle, innerRadius, outerRadius, percent, name }) => {
  const RADIAN = Math.PI / 180;
  const radius = outerRadius * 1.4;
  const x = cx + radius * Math.cos(-midAngle * RADIAN);
  const y = cy + radius * Math.sin(-midAngle * RADIAN);
  
  // Only show label if percentage is >= 1% (show all meaningful slices)
  if (percent < 0.01) return null;
  
  const formattedName = formatLabel(name);
  
  return (
    <text 
      x={x} 
      y={y} 
      fill="#374151"
      textAnchor={x > cx ? 'start' : 'end'} 
      dominantBaseline="central"
      style={{ 
        fontSize: '12px', 
        fontWeight: '500',
        fontFamily: 'Inter, system-ui, sans-serif'
      }}
    >
      {`${formattedName}: ${(percent * 100).toFixed(0)}%`}
    </text>
  );
};

// Custom tooltip formatter
const CustomTooltip = ({ active, payload }) => {
  if (active && payload && payload.length) {
    const data = payload[0];
    return (
      <div className="bg-white px-3 py-2 shadow-lg rounded-lg border border-gray-200">
        <p className="text-sm font-medium text-gray-900">
          {formatLabel(data.name)}
        </p>
        <p className="text-sm text-gray-600">
          Count: <span className="font-semibold">{data.value}</span>
        </p>
      </div>
    );
  }
  return null;
};

const ChartsPanel = ({ analysis }) => {
  if (!analysis || !analysis.charts) {
    return null;
  }

  const { charts } = analysis;

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      {/* Phase Distribution */}
      {charts.phase_distribution && charts.phase_distribution.data.length > 0 && (
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Phase Distribution</h3>
          <ResponsiveContainer width="100%" height={320}>
            <PieChart>
              <Pie
                data={charts.phase_distribution.data}
                cx="50%"
                cy="50%"
                labelLine={true}
                label={renderCustomizedLabel}
                outerRadius={85}
                innerRadius={0}
                fill="#8884d8"
                dataKey="value"
                paddingAngle={2}
              >
                {charts.phase_distribution.data.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip content={<CustomTooltip />} />
            </PieChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Status Distribution */}
      {charts.status_distribution && charts.status_distribution.data.length > 0 && (
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Trial Status</h3>
          <ResponsiveContainer width="100%" height={320}>
            <PieChart>
              <Pie
                data={charts.status_distribution.data}
                cx="50%"
                cy="50%"
                labelLine={true}
                label={renderCustomizedLabel}
                outerRadius={85}
                innerRadius={0}
                fill="#8884d8"
                dataKey="value"
                paddingAngle={2}
              >
                {charts.status_distribution.data.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip content={<CustomTooltip />} />
            </PieChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Country Distribution */}
      {charts.country_distribution && charts.country_distribution.data.length > 0 && (
        <div className="card lg:col-span-2">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Geographic Distribution (Top 10)</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={charts.country_distribution.data}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis 
                dataKey="country" 
                angle={-45} 
                textAnchor="end" 
                height={100}
                tick={{ fontSize: 11, fill: '#4b5563', fontFamily: 'Inter, system-ui, sans-serif' }}
              />
              <YAxis 
                tick={{ fontSize: 11, fill: '#4b5563', fontFamily: 'Inter, system-ui, sans-serif' }}
              />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: 'white', 
                  border: '1px solid #e5e7eb',
                  borderRadius: '8px',
                  fontSize: '12px',
                  fontFamily: 'Inter, system-ui, sans-serif'
                }}
              />
              <Bar dataKey="trials" fill="#3b82f6" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Timeline */}
      {charts.timeline && charts.timeline.data.length > 0 && (
        <div className="card lg:col-span-2">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Trial Timeline</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={charts.timeline.data}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis 
                dataKey="year" 
                tick={{ fontSize: 11, fill: '#4b5563', fontFamily: 'Inter, system-ui, sans-serif' }}
              />
              <YAxis 
                tick={{ fontSize: 11, fill: '#4b5563', fontFamily: 'Inter, system-ui, sans-serif' }}
              />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: 'white', 
                  border: '1px solid #e5e7eb',
                  borderRadius: '8px',
                  fontSize: '12px',
                  fontFamily: 'Inter, system-ui, sans-serif'
                }}
              />
              <Legend 
                wrapperStyle={{ fontSize: '12px', fontFamily: 'Inter, system-ui, sans-serif' }}
              />
              <Line type="monotone" dataKey="count" stroke="#3b82f6" strokeWidth={2} dot={{ r: 4 }} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Enrollment Stats */}
      {charts.enrollment_stats && (
        <div className="card lg:col-span-2">
          <h3 className="text-lg font-semibold mb-4">Enrollment Statistics</h3>
          <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
            <div className="text-center p-4 bg-primary-50 rounded-lg">
              <p className="text-sm text-gray-600 mb-1">Total</p>
              <p className="text-2xl font-bold text-primary-600">
                {charts.enrollment_stats.data.total?.toLocaleString()}
              </p>
            </div>
            <div className="text-center p-4 bg-blue-50 rounded-lg">
              <p className="text-sm text-gray-600 mb-1">Mean</p>
              <p className="text-2xl font-bold text-blue-600">
                {charts.enrollment_stats.data.mean?.toFixed(0)}
              </p>
            </div>
            <div className="text-center p-4 bg-green-50 rounded-lg">
              <p className="text-sm text-gray-600 mb-1">Median</p>
              <p className="text-2xl font-bold text-green-600">
                {charts.enrollment_stats.data.median?.toFixed(0)}
              </p>
            </div>
            <div className="text-center p-4 bg-yellow-50 rounded-lg">
              <p className="text-sm text-gray-600 mb-1">Min</p>
              <p className="text-2xl font-bold text-yellow-600">
                {charts.enrollment_stats.data.min}
              </p>
            </div>
            <div className="text-center p-4 bg-red-50 rounded-lg">
              <p className="text-sm text-gray-600 mb-1">Max</p>
              <p className="text-2xl font-bold text-red-600">
                {charts.enrollment_stats.data.max}
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ChartsPanel;
