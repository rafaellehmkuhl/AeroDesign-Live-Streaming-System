"""
Aero Design Competition - Live Transmission Overlay System
Backend API for controlling overlays during live broadcasts
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import os
from pathlib import Path

app = FastAPI(title="Aero Design Overlay API")

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data Models
class FlightResult(BaseModel):
    battery_number: int
    status: str  # "validated", "invalidated", "pending", "not_flown"
    score: Optional[float] = None
    notes: Optional[str] = None

class Team(BaseModel):
    id: str
    name: str
    university: str
    aircraft_photo_url: Optional[str] = None
    current_battery: int
    flight_results: List[FlightResult] = []

class OverlayState(BaseModel):
    visible: bool = False
    current_team_id: Optional[str] = None
    show_team_info: bool = True
    show_flight_results: bool = True
    show_current_battery: bool = True
    custom_message: Optional[str] = None

# In-memory storage (in production, use a real database)
teams_db: Dict[str, Team] = {}
overlay_state = OverlayState()

# Mock data for testing
def initialize_mock_data():
    """Initialize mock teams and data for testing"""
    global teams_db

    mock_teams = [
        Team(
            id="team001",
            name="AeroTech Racing",
            university="Universidade de São Paulo",
            aircraft_photo_url="https://via.placeholder.com/300x200/0066cc/ffffff?text=AeroTech",
            current_battery=3,
            flight_results=[
                FlightResult(battery_number=1, status="validated", score=8.5, notes="Excellent flight"),
                FlightResult(battery_number=2, status="validated", score=9.2, notes="Perfect landing"),
                FlightResult(battery_number=3, status="pending", score=None, notes="Currently flying"),
            ]
        ),
        Team(
            id="team002",
            name="Sky Pioneers",
            university="Instituto Tecnológico de Aeronáutica",
            aircraft_photo_url="https://via.placeholder.com/300x200/cc0000/ffffff?text=Sky+Pioneers",
            current_battery=2,
            flight_results=[
                FlightResult(battery_number=1, status="invalidated", score=None, notes="Crashed on takeoff"),
                FlightResult(battery_number=2, status="validated", score=7.8, notes="Good recovery"),
            ]
        ),
        Team(
            id="team003",
            name="Falcon Engineering",
            university="Universidade Federal de Minas Gerais",
            aircraft_photo_url="https://via.placeholder.com/300x200/00cc66/ffffff?text=Falcon",
            current_battery=4,
            flight_results=[
                FlightResult(battery_number=1, status="validated", score=8.0, notes="Solid performance"),
                FlightResult(battery_number=2, status="validated", score=8.3, notes="Improving"),
                FlightResult(battery_number=3, status="validated", score=9.0, notes="Excellent"),
                FlightResult(battery_number=4, status="pending", score=None, notes="On track now"),
            ]
        ),
    ]

    for team in mock_teams:
        teams_db[team.id] = team

# Initialize mock data on startup
initialize_mock_data()

# API Endpoints

@app.get("/")
async def root():
    return {
        "message": "Aero Design Overlay API",
        "version": "0.1.0",
        "endpoints": {
            "overlay_state": "/api/overlay/state",
            "teams": "/api/teams",
            "control_panel": "/control-panel/index.html",
            "overlay_view": "/overlay/index.html"
        }
    }

# Overlay State Endpoints
@app.get("/api/overlay/state")
async def get_overlay_state():
    """Get current overlay state (polled by OBS browser source)"""
    result = {
        "visible": overlay_state.visible,
        "show_team_info": overlay_state.show_team_info,
        "show_flight_results": overlay_state.show_flight_results,
        "show_current_battery": overlay_state.show_current_battery,
        "custom_message": overlay_state.custom_message,
        "team": None
    }

    if overlay_state.current_team_id:
        team = teams_db.get(overlay_state.current_team_id)
        if team:
            result["team"] = team.dict()

    return result

@app.put("/api/overlay/state")
async def update_overlay_state(state: OverlayState):
    """Update overlay state (called by control panel)"""
    global overlay_state
    overlay_state = state
    return {"status": "success", "state": overlay_state}

@app.post("/api/overlay/show")
async def show_overlay(team_id: Optional[str] = None):
    """Show overlay for a specific team"""
    overlay_state.visible = True
    if team_id:
        if team_id not in teams_db:
            raise HTTPException(status_code=404, detail="Team not found")
        overlay_state.current_team_id = team_id
    return {"status": "success", "visible": True, "team_id": team_id}

@app.post("/api/overlay/hide")
async def hide_overlay():
    """Hide overlay"""
    overlay_state.visible = False
    return {"status": "success", "visible": False}

@app.post("/api/overlay/toggle")
async def toggle_overlay():
    """Toggle overlay visibility"""
    overlay_state.visible = not overlay_state.visible
    return {"status": "success", "visible": overlay_state.visible}

# Team Management Endpoints
@app.get("/api/teams")
async def get_teams():
    """Get all teams"""
    return list(teams_db.values())

@app.get("/api/teams/{team_id}")
async def get_team(team_id: str):
    """Get specific team"""
    if team_id not in teams_db:
        raise HTTPException(status_code=404, detail="Team not found")
    return teams_db[team_id]

@app.post("/api/teams")
async def create_team(team: Team):
    """Create new team"""
    if team.id in teams_db:
        raise HTTPException(status_code=400, detail="Team already exists")
    teams_db[team.id] = team
    return {"status": "success", "team": team}

@app.put("/api/teams/{team_id}")
async def update_team(team_id: str, team: Team):
    """Update team"""
    if team_id not in teams_db:
        raise HTTPException(status_code=404, detail="Team not found")
    teams_db[team_id] = team
    return {"status": "success", "team": team}

@app.delete("/api/teams/{team_id}")
async def delete_team(team_id: str):
    """Delete team"""
    if team_id not in teams_db:
        raise HTTPException(status_code=404, detail="Team not found")
    del teams_db[team_id]
    return {"status": "success", "message": f"Team {team_id} deleted"}

# Flight Results Endpoints
@app.post("/api/teams/{team_id}/results")
async def add_flight_result(team_id: str, result: FlightResult):
    """Add flight result for a team"""
    if team_id not in teams_db:
        raise HTTPException(status_code=404, detail="Team not found")

    team = teams_db[team_id]
    team.flight_results.append(result)
    return {"status": "success", "team": team}

@app.put("/api/teams/{team_id}/battery")
async def update_current_battery(team_id: str, battery_number: int):
    """Update team's current battery"""
    if team_id not in teams_db:
        raise HTTPException(status_code=404, detail="Team not found")

    teams_db[team_id].current_battery = battery_number
    return {"status": "success", "team": teams_db[team_id]}

# Serve static files
overlay_dir = Path(__file__).parent.parent / "overlay"
control_panel_dir = Path(__file__).parent.parent / "control-panel"

if overlay_dir.exists():
    app.mount("/overlay", StaticFiles(directory=str(overlay_dir)), name="overlay")

if control_panel_dir.exists():
    app.mount("/control-panel", StaticFiles(directory=str(control_panel_dir)), name="control-panel")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

