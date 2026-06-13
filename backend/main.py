import os
import json
from pathlib import Path
from typing import List
from datetime import datetime
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import google.generativeai as genai  # type: ignore

load_dotenv()

app = FastAPI(
    title="VarSense AI API",
    description="API for accessing VarSense AI mock data including employees, projects, and meetings.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define Pydantic Models for Response Schemas
class Employee(BaseModel):
    id: int = Field(..., description="Unique identifier for the employee")
    name: str = Field(..., description="Full name of the employee")
    designation: str = Field(..., description="Job title or role")
    hourly_rate: float = Field(..., description="Hourly billing rate")

class Project(BaseModel):
    id: int = Field(..., description="Unique identifier for the project")
    name: str = Field(..., description="Name of the project")
    description: str = Field(..., description="Brief summary of the project goals")
    budget: float = Field(..., description="Allocated budget for the project")

class Meeting(BaseModel):
    id: int = Field(..., description="Unique identifier for the meeting")
    title: str = Field(..., description="Subject of the meeting")
    description: str = Field(..., description="What the meeting is about")
    duration_minutes: int = Field(..., description="Length of the meeting in minutes")
    attendees: List[int] = Field(..., description="List of Employee IDs attending")
    date: str = Field(..., description="ISO datetime of the meeting")

class MeetingCost(BaseModel):
    meeting_id: int = Field(..., description="Unique identifier for the meeting")
    meeting_title: str = Field(..., description="Subject of the meeting")
    project_name: str = Field(..., description="Attributed project name")
    duration_minutes: int = Field(..., description="Duration of the meeting in minutes")
    attendee_count: int = Field(..., description="Number of attendees")
    meeting_cost: float = Field(..., description="Calculated total cost of the meeting")

class ProjectCostSummary(BaseModel):
    project_name: str = Field(..., description="Name of the project")
    total_cost: float = Field(..., description="Aggregated cost of all meetings for this project")

class DashboardSummary(BaseModel):
    total_projects: int = Field(..., description="Total number of projects")
    total_meetings: int = Field(..., description="Total number of meetings")
    total_hr_cost: float = Field(..., description="Total HR cost across all meetings")
    average_meeting_cost: float = Field(..., description="Average cost per meeting")

class MostExpensiveEntity(BaseModel):
    name: str = Field(..., description="Name of the entity (project or meeting)")
    cost: float = Field(..., description="Cost of the entity")

class LowestConfidenceAttribution(BaseModel):
    meeting_title: str = Field(..., description="The title of the meeting")
    confidence_score: float = Field(..., description="The lowest confidence score observed")

class DashboardInsights(BaseModel):
    most_expensive_project: MostExpensiveEntity
    most_expensive_meeting: MostExpensiveEntity
    lowest_confidence_attribution: LowestConfidenceAttribution
    total_unattributed_meetings: int = Field(..., description="Meetings not attributed to any active project")

class MonthlyTrend(BaseModel):
    month: str = Field(..., description="Month in YYYY-MM format")
    total_cost: float = Field(..., description="Total meeting cost for the month")

class AttributionRequest(BaseModel):
    title: str = Field(..., description="The title of the meeting")
    description: str = Field(..., description="The description of the meeting")

class AttributionResponse(BaseModel):
    project_name: str = Field(..., description="The attributed project name")
    confidence_score: float = Field(..., description="Confidence score between 0.0 and 1.0")

class MeetingAttributionResult(BaseModel):
    meeting_id: int = Field(..., description="The ID of the meeting")
    title: str = Field(..., description="The title of the meeting")
    project_name: str = Field(..., description="The attributed project name")
    confidence_score: float = Field(..., description="Confidence score between 0.0 and 1.0")

class AgentReport(BaseModel):
    id: str = Field(..., description="Unique ID for the report")
    timestamp: str = Field(..., description="ISO timestamp of when the report was generated")
    content: str = Field(..., description="Markdown content of the anomaly report")

# In-memory storage for attribution results
attribution_results = []
agent_reports = []

def _get_gemini_attribution(title: str, description: str) -> AttributionResponse:
    prompt = f"""
    You are an AI Project Attribution module.
    Match the following meeting to one of these projects: Phoenix, Atlas, Mercury, Nova, Orion.
    If it doesn't clearly match, pick the most relevant one or "Unknown".
    
    Meeting Title: {title}
    Meeting Description: {description}
    
    Return ONLY a raw JSON object (without markdown code blocks) with exactly two keys:
    "project_name": The string name of the selected project.
    "confidence_score": A float between 0.0 and 1.0 representing your confidence.
    """
    model = genai.GenerativeModel('gemini-1.5-flash', generation_config={"response_mime_type": "application/json"})
    response = model.generate_content(prompt)
    result = json.loads(response.text)
    
    return AttributionResponse(
        project_name=result.get("project_name", "Unknown"),
        confidence_score=float(result.get("confidence_score", 0.0))
    )

# Helper function to load data from JSON files
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "mock_data"

def load_json_data(filename: str):
    file_path = DATA_DIR / filename
    if not file_path.exists():
        return []
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

# Load data into memory
employees_data = load_json_data("employees.json")
projects_data = load_json_data("projects.json")
meetings_data = load_json_data("meetings.json")

# Create a dictionary for O(1) employee lookups
employee_dict = {emp["id"]: emp for emp in employees_data}

@app.get("/", tags=["Root"])
def read_root():
    """
    Root endpoint returning a welcome message.
    """
    return {"message": "Welcome to VarSense AI API! Visit /docs for Swagger documentation."}

@app.get("/api/employees", response_model=List[Employee], tags=["Employees"])
def get_employees():
    """
    Retrieve a list of all employees.
    """
    return employees_data

@app.get("/api/projects", response_model=List[Project], tags=["Projects"])
def get_projects():
    """
    Retrieve a list of all projects.
    """
    return projects_data

@app.get("/api/meetings", response_model=List[Meeting], tags=["Meetings"])
def get_meetings():
    """
    Retrieve a list of all meetings.
    """
    return meetings_data

def _get_project_for_meeting(title: str) -> str:
    # Retrieve the most recent attribution for a given meeting title
    for att in reversed(attribution_results):
        if att.get("request_title") == title:
            return att["project_name"]
    return "Unassigned"

@app.get("/api/costs", response_model=List[MeetingCost], tags=["Costs"])
def get_meeting_costs():
    """
    Calculate and retrieve the cost for all meetings including their AI attributed project.
    """
    costs = []
    for meeting in meetings_data:
        duration_hours = meeting["duration_minutes"] / 60.0
        total_hourly_rate = sum(employee_dict.get(aid, {}).get("hourly_rate", 0) for aid in meeting["attendees"])
        meeting_cost = duration_hours * total_hourly_rate
        
        costs.append(MeetingCost(
            meeting_id=meeting["id"],
            meeting_title=meeting["title"],
            project_name=_get_project_for_meeting(meeting["title"]),
            duration_minutes=meeting["duration_minutes"],
            attendee_count=len(meeting["attendees"]),
            meeting_cost=round(meeting_cost, 2)
        ))
    return costs

@app.get("/api/costs/project-summary", response_model=List[ProjectCostSummary], tags=["Costs"])
def get_project_cost_summary():
    """
    Aggregate the meeting HR costs by project based on AI attribution.
    """
    summary = {}
    for meeting in meetings_data:
        proj_name = _get_project_for_meeting(meeting["title"])
        duration_hours = meeting["duration_minutes"] / 60.0
        total_hourly_rate = sum(employee_dict.get(aid, {}).get("hourly_rate", 0) for aid in meeting["attendees"])
        cost = duration_hours * total_hourly_rate
        
        summary[proj_name] = summary.get(proj_name, 0.0) + cost
        
    return [ProjectCostSummary(project_name=k, total_cost=round(v, 2)) for k, v in summary.items()]

@app.post("/api/attribution", response_model=AttributionResponse, tags=["AI Attribution"])
def attribute_project(req: AttributionRequest):
    """
    Use Gemini AI to attribute a meeting to one of the active projects: Phoenix, Atlas, Mercury, Nova, Orion.
    Returns the predicted project name and a confidence score.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY environment variable is not set. Please provide it to use the AI features.")
        
    genai.configure(api_key=api_key)
    
    try:
        att_res = _get_gemini_attribution(req.title, req.description)
        
        # Store in memory
        attribution_results.append({
            "request_title": req.title,
            "request_description": req.description,
            "project_name": att_res.project_name,
            "confidence_score": att_res.confidence_score
        })
        
        return att_res
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process AI attribution: {str(e)}")

@app.post("/api/attribution/run-all", response_model=List[MeetingAttributionResult], tags=["AI Attribution"])
def run_all_attributions():
    """
    Process all existing meetings through the Gemini AI attribution engine.
    Assigns a project and confidence score to each, and stores the results in memory.
    Note: This will execute sequentially and may take some time depending on API latency.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY environment variable is not set.")
    genai.configure(api_key=api_key)
    
    results = []
    for meeting in meetings_data:
        try:
            att_res = _get_gemini_attribution(meeting["title"], meeting["description"])
            results.append(MeetingAttributionResult(
                meeting_id=meeting["id"],
                title=meeting["title"],
                project_name=att_res.project_name,
                confidence_score=att_res.confidence_score
            ))
            
            # Store in memory
            attribution_results.append({
                "request_title": meeting["title"],
                "request_description": meeting["description"],
                "project_name": att_res.project_name,
                "confidence_score": att_res.confidence_score
            })
        except Exception as e:
            # Fallback on failure to prevent entire batch from crashing
            results.append(MeetingAttributionResult(
                meeting_id=meeting["id"],
                title=meeting["title"],
                project_name="Error",
                confidence_score=0.0
            ))
            
    return results

@app.get("/api/attribution", tags=["AI Attribution"])
def get_attributions():
    """
    Retrieve all past attribution results stored in memory.
    """
    return attribution_results

@app.get("/api/dashboard/summary", response_model=DashboardSummary, tags=["Dashboard"])
def get_dashboard_summary():
    """
    Get a high-level summary of the KPI analytics.
    """
    total_proj = len(projects_data)
    total_meet = len(meetings_data)
    
    # Calculate costs
    all_costs = get_meeting_costs()
    total_cost = sum(m.meeting_cost for m in all_costs)
    avg_cost = total_cost / total_meet if total_meet > 0 else 0.0
    
    return DashboardSummary(
        total_projects=total_proj,
        total_meetings=total_meet,
        total_hr_cost=round(total_cost, 2),
        average_meeting_cost=round(avg_cost, 2)
    )

@app.get("/api/dashboard/insights", response_model=DashboardInsights, tags=["Dashboard"])
def get_dashboard_insights():
    """
    Generate deep insights and highlights from the combined data.
    """
    all_costs = get_meeting_costs()
    proj_summaries = get_project_cost_summary()
    
    # Most expensive meeting
    most_exp_meet = max(all_costs, key=lambda x: x.meeting_cost, default=None)
    meet_entity = MostExpensiveEntity(name="None", cost=0.0)
    if most_exp_meet:
        meet_entity = MostExpensiveEntity(name=most_exp_meet.meeting_title, cost=most_exp_meet.meeting_cost)
        
    # Most expensive project
    most_exp_proj = max(proj_summaries, key=lambda x: x.total_cost, default=None)
    proj_entity = MostExpensiveEntity(name="None", cost=0.0)
    if most_exp_proj:
        proj_entity = MostExpensiveEntity(name=most_exp_proj.project_name, cost=most_exp_proj.total_cost)
        
    # Lowest confidence attribution
    low_conf_att = LowestConfidenceAttribution(meeting_title="None", confidence_score=0.0)
    if attribution_results:
        min_att = min(attribution_results, key=lambda x: x["confidence_score"])
        low_conf_att = LowestConfidenceAttribution(meeting_title=min_att["request_title"], confidence_score=min_att["confidence_score"])
        
    # Unattributed meetings
    unattributed_count = sum(1 for m in all_costs if m.project_name == "Unassigned")
    
    return DashboardInsights(
        most_expensive_project=proj_entity,
        most_expensive_meeting=meet_entity,
        lowest_confidence_attribution=low_conf_att,
        total_unattributed_meetings=unattributed_count
    )

@app.get("/api/dashboard/trend", response_model=List[MonthlyTrend], tags=["Dashboard"])
def get_dashboard_trend():
    """
    Aggregate costs by month to generate a cost trend chart.
    """
    trend = {}
    for meeting in meetings_data:
        date_str = meeting.get("date", "2026-01-01T00:00:00Z")
        month = date_str[:7] # Extract YYYY-MM
        duration_hours = meeting["duration_minutes"] / 60.0
        total_hourly_rate = sum(employee_dict.get(aid, {}).get("hourly_rate", 0) for aid in meeting["attendees"])
        cost = duration_hours * total_hourly_rate
        
        trend[month] = trend.get(month, 0.0) + cost
        
    # Sort chronologically
    sorted_trend = [{"month": k, "total_cost": round(v, 2)} for k, v in sorted(trend.items())]
    return sorted_trend

@app.post("/api/agent/run", response_model=AgentReport, tags=["Agent"])
def run_agent_analysis():
    """
    Run the autonomous agent to analyze current dashboard costs and find anomalies.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY environment variable is not set.")
    genai.configure(api_key=api_key)

    summary = get_dashboard_summary()
    insights = get_dashboard_insights()
    proj_summary = get_project_cost_summary()
    top_meetings = sorted(get_meeting_costs(), key=lambda x: x.meeting_cost, reverse=True)[:5]
    
    context = {
        "summary": summary.model_dump(),
        "insights": insights.model_dump(),
        "top_expensive_projects": [p.model_dump() for p in proj_summary],
        "top_expensive_meetings": [m.model_dump() for m in top_meetings]
    }
    
    prompt = f"""
    You are an expert Executive Financial Analyst AI.
    Analyze the following corporate meeting HR cost data and write a short, punchy executive summary (max 3 paragraphs).
    Identify any major "Cost Anomalies" - e.g., a specific project burning too much budget on meetings, or a single meeting that was disproportionately expensive.
    Format your response in Markdown. Use bolding for emphasis. Be direct and analytical.
    
    Data:
    {json.dumps(context, indent=2)}
    """
    
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt)
        
        report = AgentReport(
            id=f"rep_{len(agent_reports)+1}",
            timestamp=datetime.utcnow().isoformat() + "Z",
            content=response.text
        )
        agent_reports.insert(0, report.model_dump()) # Prepend so newest is first
        
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate agent report: {str(e)}")

@app.get("/api/agent/reports", response_model=List[AgentReport], tags=["Agent"])
def get_agent_reports():
    """
    Retrieve all past agent reports.
    """
    return agent_reports
