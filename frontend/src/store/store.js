import { create } from 'zustand';

export const useAnalysisStore = create((set) => ({
  // State
  currentAnalysis: null,
  isLoading: false,
  error: null,
  history: [],

  // Actions
  setAnalysis: (analysis) =>
    set((state) => ({
      currentAnalysis: analysis,
      history: [analysis, ...state.history.slice(0, 9)], // Keep last 10
    })),

  setLoading: (loading) => set({ isLoading: loading }),

  setError: (error) => set({ error }),

  clearError: () => set({ error: null }),

  clearAnalysis: () => set({ currentAnalysis: null }),

  clearHistory: () => set({ history: [] }),
}));

export const useUIStore = create((set) => ({
  // State
  sidebarOpen: true,
  activeTab: 'trials',
  selectedTrials: [],
  filters: {},

  // Actions
  toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),

  setActiveTab: (tab) => set({ activeTab: tab }),

  setSelectedTrials: (trials) => set({ selectedTrials: trials }),

  toggleTrialSelection: (trialId) =>
    set((state) => ({
      selectedTrials: state.selectedTrials.includes(trialId)
        ? state.selectedTrials.filter((id) => id !== trialId)
        : [...state.selectedTrials, trialId],
    })),

  setFilters: (filters) => set({ filters }),

  clearFilters: () => set({ filters: {} }),
}));
