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

# Real competition data - 2025 SAE Brasil AeroDesign - Classe Regular
def initialize_mock_data():
    """Initialize real teams from 2025 competition"""
    global teams_db

    real_teams = [
        Team(
            id="team001",
            name="EESC-USP Alpha",
            university="Escola de Engenharia de São Carlos - USP",
            aircraft_photo_url="https://via.placeholder.com/300x200/0066cc/ffffff?text=EESC-USP+Alpha",
            current_battery=1,
            flight_results=[]
        ),
        Team(
            id="team002",
            name="Axé Fly",
            university="Universidade Federal da Bahia (UFBA)",
            aircraft_photo_url="https://via.placeholder.com/300x200/FF9900/ffffff?text=Axe+Fly",
            current_battery=1,
            flight_results=[]
        ),
        Team(
            id="team003",
            name="Uirá AeroDesign",
            university="Universidade Federal de Itajubá",
            aircraft_photo_url="https://via.placeholder.com/300x200/00cc66/ffffff?text=Uira",
            current_battery=1,
            flight_results=[]
        ),
        Team(
            id="team004",
            name="Uai, sô! Fly!!!",
            university="Universidade Federal de Minas Gerais (UFMG)",
            aircraft_photo_url="https://via.placeholder.com/300x200/cc0000/ffffff?text=Uai+So+Fly",
            current_battery=1,
            flight_results=[]
        ),
        Team(
            id="team005",
            name="AeroFEG",
            university="Faculdade de Engenharia de Guaratinguetá - UNESP",
            aircraft_photo_url="https://via.placeholder.com/300x200/9933ff/ffffff?text=AeroFEG",
            current_battery=1,
            flight_results=[]
        ),
        Team(
            id="team006",
            name="Keep Flying",
            university="Escola Politécnica - USP",
            aircraft_photo_url="https://via.placeholder.com/300x200/0099cc/ffffff?text=Keep+Flying",
            current_battery=1,
            flight_results=[]
        ),
        Team(
            id="team007",
            name="Montenegro",
            university="Instituto Tecnológico de Aeronáutica (ITA)",
            aircraft_photo_url="https://via.placeholder.com/300x200/003366/ffffff?text=Montenegro",
            current_battery=1,
            flight_results=[]
        ),
        Team(
            id="team008",
            name="Tucano",
            university="Universidade Federal de Uberlândia (UFU)",
            aircraft_photo_url="https://via.placeholder.com/300x200/ffcc00/ffffff?text=Tucano",
            current_battery=1,
            flight_results=[]
        ),
        Team(
            id="team009",
            name="Falcons AeroDesign",
            university="Centro Universitário FACENS",
            aircraft_photo_url="https://via.placeholder.com/300x200/990000/ffffff?text=Falcons",
            current_battery=1,
            flight_results=[]
        ),
        Team(
            id="team010",
            name="CEFAST AeroDesign",
            university="Centro Federal de Educação Tecnológica de Minas Gerais",
            aircraft_photo_url="https://via.placeholder.com/300x200/006633/ffffff?text=CEFAST",
            current_battery=1,
            flight_results=[]
        ),
        Team(
            id="team011",
            name="F-Carranca",
            university="Universidade Federal do Vale do São Francisco (UNIVASF)",
            aircraft_photo_url="https://via.placeholder.com/300x200/ff6600/ffffff?text=F-Carranca",
            current_battery=1,
            flight_results=[]
        ),
        Team(
            id="team012",
            name="Kukulcán AeroDesign",
            university="Instituto Superior de Ingeniería Mecánica - México",
            aircraft_photo_url="https://via.placeholder.com/300x200/cc6600/ffffff?text=Kukulcan",
            current_battery=1,
            flight_results=[]
        ),
        Team(
            id="team013",
            name="AeroJampa",
            university="Universidade Federal da Paraíba (UFPB)",
            aircraft_photo_url="https://via.placeholder.com/300x200/3366cc/ffffff?text=AeroJampa",
            current_battery=1,
            flight_results=[]
        ),
        Team(
            id="team014",
            name="Megazord AeroDesign",
            university="Instituto Tecnológico de Aeronáutica - São José dos Campos",
            aircraft_photo_url="https://via.placeholder.com/300x200/ff0066/ffffff?text=Megazord",
            current_battery=1,
            flight_results=[]
        ),
        Team(
            id="team015",
            name="Harpia AeroDesign UFABC",
            university="Universidade Federal do ABC (UFABC)",
            aircraft_photo_url="https://via.placeholder.com/300x200/336699/ffffff?text=Harpia",
            current_battery=1,
            flight_results=[]
        ),
        Team(
            id="team016",
            name="Urubus AeroDesign",
            university="Universidade Estadual de Campinas (UNICAMP)",
            aircraft_photo_url="https://via.placeholder.com/300x200/000000/ffffff?text=Urubus",
            current_battery=1,
            flight_results=[]
        ),
        Team(
            id="team017",
            name="UTFalcon AeroDesign",
            university="Universidade Tecnológica Federal do Paraná - Ponta Grossa",
            aircraft_photo_url="https://via.placeholder.com/300x200/666666/ffffff?text=UTFalcon",
            current_battery=1,
            flight_results=[]
        ),
        Team(
            id="team018",
            name="Falcão Branco",
            university="Centro Universitário Hermínio Ometto (FHO)",
            aircraft_photo_url="https://via.placeholder.com/300x200/cccccc/333333?text=Falcao+Branco",
            current_battery=1,
            flight_results=[]
        ),
        Team(
            id="team019",
            name="FEI Regular",
            university="Centro Universitário da FEI",
            aircraft_photo_url="https://via.placeholder.com/300x200/0033cc/ffffff?text=FEI",
            current_battery=1,
            flight_results=[]
        ),
        Team(
            id="team020",
            name="AeroScorpion IFSP",
            university="Instituto Federal de São Paulo - Araraquara",
            aircraft_photo_url="https://via.placeholder.com/300x200/993300/ffffff?text=AeroScorpion",
            current_battery=1,
            flight_results=[]
        ),
    ]

    for team in real_teams:
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

