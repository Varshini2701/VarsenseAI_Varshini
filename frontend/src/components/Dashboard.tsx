import React, { useEffect, useState } from 'react';
import { fetchProjects, fetchMeetings, fetchCosts, fetchDashboardSummary, fetchProjectSummary, fetchTrend, fetchAttributions, fetchAgentReports } from '../services/api';
import type { Project, Meeting, MeetingCost, DashboardSummary, ProjectCostSummary, MonthlyTrend, AttributionResult, AgentReport } from '../services/api';
import { DataTable } from './DataTable';
import { KPICards } from './KPICards';
import { ChartsDashboard } from './ChartsDashboard';
import { HeroSection } from './HeroSection';
import { AgentInsights } from './AgentInsights';
import { MeetingCalendar } from './MeetingCalendar';

export const Dashboard: React.FC = () => {
  const [projects, setProjects] = useState<Project[]>([]);
  const [meetings, setMeetings] = useState<Meeting[]>([]);
  const [costs, setCosts] = useState<MeetingCost[]>([]);
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [projectSummaries, setProjectSummaries] = useState<ProjectCostSummary[]>([]);
  const [trends, setTrends] = useState<MonthlyTrend[]>([]);
  const [attributions, setAttributions] = useState<AttributionResult[]>([]);
  const [reports, setReports] = useState<AgentReport[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadData = async () => {
      try {
        setLoading(true);
        const [projData, meetData, costData, summaryData, projSumData, trendData, attData, repData] = await Promise.all([
          fetchProjects(),
          fetchMeetings(),
          fetchCosts(),
          fetchDashboardSummary(),
          fetchProjectSummary(),
          fetchTrend(),
          fetchAttributions(),
          fetchAgentReports()
        ]);
        setProjects(projData);
        setMeetings(meetData);
        setCosts(costData);
        setSummary(summaryData);
        setProjectSummaries(projSumData);
        setTrends(trendData);
        setAttributions(attData);
        setReports(repData);
        setError(null);
      } catch (err: any) {
        setError(err.message || 'Failed to load data from the server.');
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, []);

  if (loading) {
    return (
      <div className="loading-state">
        <div className="spinner"></div>
        <p>Loading API Data...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="error-state">
        <h2>Connection Error</h2>
        <p>{error}</p>
        <button className="badge" onClick={() => window.location.reload()} style={{ marginTop: '1rem', cursor: 'pointer', border: 'none' }}>Retry</button>
      </div>
    );
  }

  return (
    <div className="dashboard-content">
      <HeroSection />

      <KPICards summary={summary} />

      <ChartsDashboard costs={costs} projectSummaries={projectSummaries} trends={trends} />

      <AgentInsights reports={reports} onNewReport={(newReport) => setReports(prev => [newReport, ...prev])} />

      <MeetingCalendar meetings={meetings} />

      <DataTable
        title="Active Projects"
        columns={['ID', 'Name', 'Description', 'Budget']}
        data={projects}
        renderRow={(project) => (
          <tr key={project.id}>
            <td>{project.id}</td>
            <td><span className="badge">{project.name}</span></td>
            <td>{project.description}</td>
            <td className="currency">${project.budget.toLocaleString()}</td>
          </tr>
        )}
      />

      <DataTable
        title="Meeting Roster"
        columns={['ID', 'Title', 'Duration', 'Attendees']}
        data={meetings}
        renderRow={(meeting) => (
          <tr key={meeting.id}>
            <td>{meeting.id}</td>
            <td>{meeting.title}</td>
            <td>{meeting.duration_minutes} mins</td>
            <td>{meeting.attendees.length} members</td>
          </tr>
        )}
      />

      <DataTable
        title="AI Attribution Results"
        columns={['Meeting', 'Project', 'Confidence', 'Cost']}
        data={attributions}
        renderRow={(att, idx) => {
          const matchingCost = costs.find(c => c.meeting_title === att.request_title);
          const costVal = matchingCost ? matchingCost.meeting_cost : 0;
          const isLowConf = att.confidence_score < 0.7;
          const progressWidth = `${att.confidence_score * 100}%`;
          const progressColor = isLowConf ? 'var(--error)' : 'var(--success)';
          
          return (
            <tr key={`att-${idx}`} style={{ backgroundColor: isLowConf ? 'rgba(239, 68, 68, 0.05)' : undefined }}>
              <td>{att.request_title}</td>
              <td><span className="badge">{att.project_name}</span></td>
              <td style={{ minWidth: '200px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <span style={{ color: progressColor, fontWeight: 'bold' }}>{(att.confidence_score * 100).toFixed(0)}%</span>
                  <div style={{ flex: 1, height: '8px', background: 'rgba(255,255,255,0.1)', borderRadius: '4px', overflow: 'hidden' }}>
                    <div style={{ width: progressWidth, height: '100%', background: progressColor, borderRadius: '4px' }}></div>
                  </div>
                </div>
              </td>
              <td className="currency">${costVal.toLocaleString()}</td>
            </tr>
          );
        }}
      />
      
      <DataTable
        title="Meeting Cost Analysis"
        columns={['Meeting', 'Project', 'Attendees', 'Total Cost']}
        data={costs}
        renderRow={(cost, idx) => (
          <tr key={idx}>
            <td>{cost.meeting_title}</td>
            <td>
              <span 
                className="badge" 
                style={{ 
                  background: cost.project_name === 'Unassigned' ? 'rgba(239, 68, 68, 0.2)' : undefined, 
                  color: cost.project_name === 'Unassigned' ? '#fca5a5' : undefined,
                  border: cost.project_name === 'Unassigned' ? '1px solid rgba(239, 68, 68, 0.3)' : undefined
                }}
              >
                {cost.project_name}
              </span>
            </td>
            <td>{cost.attendee_count}</td>
            <td className="currency">${cost.meeting_cost.toLocaleString()}</td>
          </tr>
        )}
      />
    </div>
  );
};
