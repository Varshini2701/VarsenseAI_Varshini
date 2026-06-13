import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import type { AgentReport } from '../services/api';
import { runAgentAnalysis } from '../services/api';

interface AgentInsightsProps {
  reports: AgentReport[];
  onNewReport: (report: AgentReport) => void;
}

export const AgentInsights: React.FC<AgentInsightsProps> = ({ reports, onNewReport }) => {
  const [analyzing, setAnalyzing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleRunAnalysis = async () => {
    try {
      setAnalyzing(true);
      setError(null);
      const newReport = await runAgentAnalysis();
      onNewReport(newReport);
    } catch (err: any) {
      setError(err.message || 'Failed to run analysis');
    } finally {
      setAnalyzing(false);
    }
  };

  return (
    <div className="agent-insights-container">
      <div className="agent-header">
        <h2 className="table-title" style={{ marginBottom: 0, display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <span style={{ fontSize: '1.5rem' }}>🤖</span> Automated Insights Agent
        </h2>
        <button 
          className="run-agent-btn" 
          onClick={handleRunAnalysis} 
          disabled={analyzing}
        >
          {analyzing ? (
            <><span className="spinner-small"></span> Analyzing...</>
          ) : (
            <>Run Deep Analysis</>
          )}
        </button>
      </div>

      {error && (
        <div style={{ color: 'var(--error)', marginBottom: '1rem', padding: '1rem', background: 'rgba(239, 68, 68, 0.1)', borderRadius: '8px' }}>
          {error}
        </div>
      )}

      <div className="reports-feed">
        {reports.length === 0 ? (
          <div className="empty-state">
            <p>No anomaly reports generated yet. Click "Run Deep Analysis" to start.</p>
          </div>
        ) : (
          reports.map((report) => (
            <div key={report.id} className="report-card">
              <div className="report-timestamp">
                {new Date(report.timestamp).toLocaleString()}
              </div>
              <div className="report-content">
                <ReactMarkdown>{report.content}</ReactMarkdown>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};
