import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

export const analysisAPI = {
  analyze: async (query, filters = {}) => {
    const response = await api.post('/analyze', {
      query,
      filters,
      include_literature: true,
      include_safety: true,
      max_trials: 50,
    });
    return response.data;
  },

  getTrials: async (params) => {
    const response = await api.get('/get-trials', { params });
    return response.data;
  },

  getLiterature: async (params) => {
    const response = await api.get('/get-literature', { params });
    return response.data;
  },

  getSafetyData: async (drugName) => {
    const response = await api.get('/get-safety-data', {
      params: { drug_name: drugName },
    });
    return response.data;
  },
};

export const comparisonAPI = {
  compareTrials: async (trialIds, compareBy = []) => {
    const response = await api.post('/compare', {
      trial_ids: trialIds,
      compare_by: compareBy,
    });
    return response.data;
  },

  compareInterventions: async (interventions, condition = null) => {
    const response = await api.get('/compare-interventions', {
      params: {
        interventions: interventions.join(','),
        condition,
      },
    });
    return response.data;
  },
};

export const reportAPI = {
  generateReport: async (analysisData, reportTitle = 'MedNexa Research Report', includeCharts = true, includeReferences = true) => {
    const response = await api.post(
      '/generate-report',
      {
        analysis_data: analysisData,
        report_title: reportTitle,
        include_charts: includeCharts,
        include_references: includeReferences,
      },
      {
        responseType: 'blob',
      }
    );
    return response.data;
  },

  downloadSampleReport: async () => {
    const response = await api.get('/download-sample-report', {
      responseType: 'blob',
    });
    return response.data;
  },
};

export default api;
