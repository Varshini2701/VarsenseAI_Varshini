import React from 'react';
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell,
  LineChart, Line, CartesianGrid
} from 'recharts';
import type { MeetingCost, ProjectCostSummary, MonthlyTrend } from '../services/api';

interface ChartsDashboardProps {
  costs: MeetingCost[];
  projectSummaries: ProjectCostSummary[];
  trends: MonthlyTrend[];
}

// Sleek SaaS colors
const COLORS = ['#3b82f6', '#8b5cf6', '#10b981', '#f59e0b', '#ec4899', '#06b6d4'];

export const ChartsDashboard: React.FC<ChartsDashboardProps> = ({ costs, projectSummaries, trends }) => {
  
  const topMeetings = [...costs].sort((a, b) => b.meeting_cost - a.meeting_cost).slice(0, 5);

  return (
    <div className="charts-grid">
      
      {/* 1. Cost By Project Chart (Pie) */}
      <div className="chart-card">
        <h3 className="chart-title">Cost By Project</h3>
        <div className="chart-container">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={projectSummaries}
                dataKey="total_cost"
                nameKey="project_name"
                cx="50%"
                cy="50%"
                innerRadius={60}
                paddingAngle={5}
                label={({ name, percent }) => `${name} ${(percent || 0) * 100}%`}
                outerRadius={100}
                fill="#8884d8"
                labelLine={false}
                stroke="none"
              >
                {projectSummaries.map((_, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} style={{ outline: 'none' }} />
                ))}
              </Pie>
              <Tooltip cursor={{ fill: 'rgba(255,255,255,0.05)' }} />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* 2. Meeting Cost Distribution (Bar) */}
      <div className="chart-card">
        <h3 className="chart-title">Top Expensive Meetings</h3>
        <div className="chart-container">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={topMeetings} layout="vertical" margin={{ left: 10, right: 30 }}>
              <defs>
                <linearGradient id="barGradient" x1="0" y1="0" x2="1" y2="0">
                  <stop offset="0%" stopColor="#3b82f6" />
                  <stop offset="100%" stopColor="#8b5cf6" />
                </linearGradient>
              </defs>
              <XAxis type="number" hide />
              <YAxis 
                type="category" 
                dataKey="meeting_title" 
                axisLine={false} 
                tickLine={false} 
                tick={{fill: '#a1a1aa', fontSize: 13}} 
                width={150} 
              />
              <Tooltip cursor={{ fill: 'rgba(255,255,255,0.02)' }} />
              <Bar dataKey="meeting_cost" fill="url(#barGradient)" radius={[0, 6, 6, 0]} barSize={24} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* 3. Monthly Cost Trend Chart (Line) */}
      <div className="chart-card" style={{ gridColumn: '1 / -1' }}>
        <h3 className="chart-title">Monthly Cost Trend</h3>
        <div className="chart-container">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={trends} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
              <defs>
                <linearGradient id="lineGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#8b5cf6" stopOpacity={0.3}/>
                  <stop offset="95%" stopColor="#8b5cf6" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="rgba(255,255,255,0.04)" />
              <XAxis 
                dataKey="month" 
                axisLine={false} 
                tickLine={false} 
                tick={{fill: '#a1a1aa', fontSize: 13}} 
                dy={10} 
              />
              <YAxis 
                axisLine={false} 
                tickLine={false} 
                tick={{fill: '#a1a1aa', fontSize: 13}} 
                tickFormatter={(value) => `$${value/1000}k`}
              />
              <Tooltip cursor={{ stroke: 'rgba(255,255,255,0.1)', strokeWidth: 1, strokeDasharray: '4 4' }} />
              <Line 
                type="monotone" 
                dataKey="total_cost" 
                stroke="#8b5cf6" 
                strokeWidth={3} 
                dot={{ r: 4, fill: '#8b5cf6', strokeWidth: 0 }} 
                activeDot={{ r: 6, fill: '#fff', stroke: '#8b5cf6', strokeWidth: 2 }} 
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

    </div>
  );
};
