# VarSense AI_Varshini

This is the monorepo for the VarSense AI_Varshini full-stack application.

## Project Structure

- `frontend/`: React + TypeScript frontend created with Vite.
- `backend/`: FastAPI backend.
- `docs/`: Project documentation.

## Setup Instructions

### Prerequisites
- Node.js (v18+ recommended)
- Python (v3.9+ recommended)

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the FastAPI development server:
   ```bash
   uvicorn main:app --reload
   ```

The FastAPI backend will be accessible at http://127.0.0.1:8000.
The React frontend will be accessible at the port outputted by Vite (typically http://localhost:5173).
