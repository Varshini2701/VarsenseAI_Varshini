export interface Project {
  id: number;
  name: string;
  description: string;
  budget: number;
}

export interface Meeting {
  id: number;
  title: string;
  description: string;
  duration_minutes: number;
  attendees: number[];
  date: string;
}

export interface MeetingCost {
  meeting_id: number;
  meeting_title: string;
  project_name: string;
  duration_minutes: number;
  attendee_count: number;
  meeting_cost: number;
}

export interface DashboardSummary {
  total_projects: number;
  total_meetings: number;
  total_hr_cost: number;
  average_meeting_cost: number;
}

export interface ProjectCostSummary {
  project_name: string;
  total_cost: number;
}

export interface MonthlyTrend {
  month: string;
  total_cost: number;
}

export interface AttributionResult {
  request_title: string;
  project_name: string;
  confidence_score: number;
}

export interface AgentReport {
  id: string;
  timestamp: string;
  content: string;
}

const API_BASE_URL = 'http://127.0.0.1:8000/api';

export const fetchProjects = async (): Promise<Project[]> => {
  const response = await fetch(`${API_BASE_URL}/projects`);
  if (!response.ok) throw new Error("Failed to fetch projects");
  return response.json();
};

export const fetchMeetings = async (): Promise<Meeting[]> => {
  const response = await fetch(`${API_BASE_URL}/meetings`);
  if (!response.ok) throw new Error("Failed to fetch meetings");
  return response.json();
};

export const fetchCosts = async (): Promise<MeetingCost[]> => {
  const response = await fetch(`${API_BASE_URL}/costs`);
  if (!response.ok) throw new Error("Failed to fetch costs");
  return response.json();
};

export const fetchDashboardSummary = async (): Promise<DashboardSummary> => {
  const response = await fetch(`${API_BASE_URL}/dashboard/summary`);
  if (!response.ok) throw new Error("Failed to fetch dashboard summary");
  return response.json();
};

export const fetchProjectSummary = async (): Promise<ProjectCostSummary[]> => {
  const response = await fetch(`${API_BASE_URL}/costs/project-summary`);
  if (!response.ok) throw new Error("Failed to fetch project summary");
  return response.json();
};

export const fetchTrend = async (): Promise<MonthlyTrend[]> => {
  const response = await fetch(`${API_BASE_URL}/dashboard/trend`);
  if (!response.ok) throw new Error("Failed to fetch trend");
  return response.json();
};

export const fetchAttributions = async (): Promise<AttributionResult[]> => {
  const response = await fetch(`${API_BASE_URL}/attribution`);
  if (!response.ok) throw new Error("Failed to fetch attributions");
  return response.json();
};

export const fetchAgentReports = async (): Promise<AgentReport[]> => {
  const response = await fetch(`${API_BASE_URL}/agent/reports`);
  if (!response.ok) throw new Error("Failed to fetch agent reports");
  return response.json();
};

export const runAgentAnalysis = async (): Promise<AgentReport> => {
  const response = await fetch(`${API_BASE_URL}/agent/run`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' }
  });
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || "Failed to run agent analysis");
  }
  return response.json();
};
