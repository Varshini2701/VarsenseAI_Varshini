# Project Name

VarsenseAI

---

## Attendee Details

**Name:** Varshini
**GitHub Username:** Varshini2701
**LinkedIn Profile:** [Your LinkedIn profile link]
**GitHub Project Repository:** https://github.com/Varshini2701/VarsenseAI_Varshini.git

---

## Problem Statement Selected

HR Cost Intelligence Engine

---

## Project Description

VarsenseAI is an intelligent full-stack dashboard application built with React and FastAPI to provide actionable, AI-driven financial insights. 

**What is the project about?**
It is an HR Cost Intelligence Engine that tracks the "hidden" financial costs of corporate meetings and automatically attributes those costs to specific projects using AI.

**Who is it for?**
It is designed for executives, project managers, and finance teams who want better visibility into operational spending and resource allocation.

**What problem does it solve?**
Countless hours are spent in meetings without being explicitly linked to project budgets. This app solves the problem of untracked HR costs by dynamically calculating the exact financial cost of every meeting (based on attendees' hourly rates and meeting duration). 

**How does it help the user?**
It uses Google Gemini AI to analyze meeting titles and descriptions to intelligently categorize them by project. It also features an autonomous AI Agent that scans all dashboard data to highlight "Cost Anomalies" (e.g., a project burning too much budget on meetings), delivering concise executive insights.

---

## Approach

* **Understanding the Problem:** I realized that to accurately track hidden HR costs, the system needed both precise calculation logic (duration × employee rates) and intelligent categorization, as meeting data is often unstructured.
* **User Flow & Features:** I designed a centralized dashboard flow where a user can immediately see high-level KPIs (Total HR Cost, Average Meeting Cost), view monthly trends via Recharts, and see exactly when expensive meetings occurred using React Big Calendar.
* **AI Integration:** Instead of manual data entry, I integrated the Google Gemini API in two distinct ways:
  1. **Attribution Engine:** To process unstructured meeting descriptions and confidently assign them to active projects.
  2. **Executive Agent:** To autonomously read the structured cost data and write a punchy markdown report identifying financial anomalies.
* **What makes it different:** The seamless combination of a fast RESTful API (FastAPI), a highly interactive frontend (Vite/React), and dual-layer AI integration makes the platform feel like a proactive financial advisor rather than just a passive tracking tool.

---

## Tech Stack and Tools Used

**Frontend:** React, TypeScript, Vite, Recharts, React Big Calendar, React Markdown
**Backend:** Python, FastAPI, Uvicorn, Pydantic
**Database:** Local JSON (Mock Data)
**AI Tools/API:** Google Gemini API (google-generativeai)
**Cloud/Deployment:** [Add cloud platform if deployed, e.g., Vercel, Render]
**Other Tools:**https://github.com/Varshini2701/varsense-insight-deck.git)

---

## Key Features

1. Interactive Frontend Dashboard with KPI cards and Recharts
2. Meeting Calendar view
3. AI Agent Insights powered by Gemini
4. FastAPI REST backend for fast data retrieval

---

## What is Working?

* Frontend UI rendering successfully (Dashboard, Charts, Calendar)
* Backend API endpoints serving data
* AI integration fetching insights

---

## What is Still in Progress?

* Replacing mock JSON data with a live, persistent database (e.g., PostgreSQL/MongoDB)
* Implementing User Authentication and Role-Based Access Control (RBAC)
* Expanding the AI Agent capabilities to include more predictive analytics and conversational chat
* Adding more granular data filtering options on the frontend Dashboard
* Setting up CI/CD pipelines for automated testing and deployment

---

## Screenshots or Demo

**Deployed Link:** https://preview--varsense-insight-deck.lovable.app/
**Demo Video Link:**(https://drive.google.com/file/d/1etxKVcFvbXbsqNJmoUFuPC2InZSajSOG/view?usp=drive_link)
**Screenshots:** [Add Links or Images]

---

## Challenges Faced

1. **AI Prompt Engineering:** Structuring the prompts for the Gemini API to consistently return reliable, structured responses suitable for a dashboard.
2. **CORS and API Integration:** Managing Cross-Origin Resource Sharing (CORS) between the Vite frontend development server and the FastAPI backend.
3. **Frontend State & Visuals:** Seamlessly integrating Recharts and the React Big Calendar while managing complex state to keep the dashboard responsive and interactive.
4. **Environment Security:** Handling environment variables properly to ensure API keys (like the Google Gemini key) were kept secure and not accidentally pushed to version control.

---

## Learnings

* Gained hands-on experience integrating Large Language Models (LLMs) into a full-stack application using the Google Gemini API.
* Deepened understanding of building scalable RESTful APIs with Python and FastAPI.
* Improved frontend skills in React and TypeScript, specifically in working with data visualization libraries like Recharts and integrating third-party components like React Big Calendar.
* Learned best practices for securing environment variables and managing Git repository rules.

---

## Future Improvements

* **Real-time Updates:** Implement WebSockets in the FastAPI backend so that the React dashboard updates in real-time as data changes.
* **Third-Party Integrations:** Connect the system directly to external enterprise tools (e.g., Slack, Google Workspace, or actual HR systems) rather than relying on internal mock data.
* **Conversational AI Interface:** Add a chatbot interface where users can ask ad-hoc questions about their data in plain English and have the Gemini model generate on-the-fly SQL queries or chart visualizations.
* **Docker & Automated Deployment:** Containerize the frontend and backend using Docker and set up a fully automated CI/CD pipeline for cloud deployment.
* **OAuth Authentication:** Implement social and enterprise login (like Google or GitHub SSO).

---

## Final Note

This project was a fantastic opportunity to dive deep into the integration of modern frontend architectures with powerful AI models. I'm incredibly proud of how quickly VarsenseAI went from concept to a working full-stack prototype. A huge thank you to the mentors and the community for their support and guidance throughout the Buildathon!
