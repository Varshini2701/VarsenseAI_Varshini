import React from 'react';
import type { DashboardSummary } from '../services/api';

interface KPICardsProps {
  summary: DashboardSummary | null;
}

export const KPICards: React.FC<KPICardsProps> = ({ summary }) => {
  if (!summary) return null;

  return (
    <div className="kpi-grid">
      <div className="kpi-card">
        <span className="kpi-title">Total Cost</span>
        <span className="kpi-value currency">${summary.total_hr_cost.toLocaleString()}</span>
      </div>
      <div className="kpi-card">
        <span className="kpi-title">Avg Meeting Cost</span>
        <span className="kpi-value currency">${summary.average_meeting_cost.toLocaleString(undefined, { maximumFractionDigits: 2 })}</span>
      </div>
      <div className="kpi-card">
        <span className="kpi-title">Total Meetings</span>
        <span className="kpi-value">{summary.total_meetings}</span>
      </div>
      <div className="kpi-card">
        <span className="kpi-title">Total Projects</span>
        <span className="kpi-value">{summary.total_projects}</span>
      </div>
    </div>
  );
};
