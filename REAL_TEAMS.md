# Real Teams - 2025 SAE Brasil AeroDesign Competition

## ✅ Successfully Loaded!

Your backend now contains **20 real teams** from the 2025 SAE Brasil AeroDesign - Classe Regular competition.

## Teams in the System

1. **EESC-USP Alpha** - Escola de Engenharia de São Carlos - USP (1st place - 458.54 pts)
2. **Axé Fly** - Universidade Federal da Bahia (UFBA) (2nd place - 441.40 pts)
3. **Uirá AeroDesign** - Universidade Federal de Itajubá (3rd place - 411.32 pts)
4. **Uai, sô! Fly!!!** - Universidade Federal de Minas Gerais (UFMG) (4th place - 401.72 pts)
5. **AeroFEG** - Faculdade de Engenharia de Guaratinguetá - UNESP (5th place - 336.70 pts)
6. **Keep Flying** - Escola Politécnica - USP (6th place - 323.48 pts)
7. **Montenegro** - Instituto Tecnológico de Aeronáutica (ITA) (7th place - 307.46 pts)
8. **Tucano** - Universidade Federal de Uberlândia (UFU) (8th place - 304.45 pts)
9. **Falcons AeroDesign** - Centro Universitário FACENS (9th place - 299.59 pts)
10. **CEFAST AeroDesign** - Centro Federal de Educação Tecnológica de Minas Gerais (10th place - 276.26 pts)
11. **F-Carranca** - Universidade Federal do Vale do São Francisco (UNIVASF)
12. **Kukulcán AeroDesign** - Instituto Superior de Ingeniería Mecánica - México
13. **AeroJampa** - Universidade Federal da Paraíba (UFPB)
14. **Megazord AeroDesign** - Instituto Tecnológico de Aeronáutica - São José dos Campos
15. **Harpia AeroDesign UFABC** - Universidade Federal do ABC (UFABC)
16. **Urubus AeroDesign** - Universidade Estadual de Campinas (UNICAMP)
17. **UTFalcon AeroDesign** - Universidade Tecnológica Federal do Paraná - Ponta Grossa
18. **Falcão Branco** - Centro Universitário Hermínio Ometto (FHO)
19. **FEI Regular** - Centro Universitário da FEI
20. **AeroScorpion IFSP** - Instituto Federal de São Paulo - Araraquara

## Team IDs

Teams are assigned IDs from `team001` to `team020`. You can reference them in the API or control panel using these IDs.

## Current Status

- ✅ All teams start at **Battery 1**
- ✅ No flight results yet (start fresh for your event)
- ✅ Placeholder aircraft photos (colorful placeholders with team names)
- ✅ Real university names and team names from the official competition

## Adding Flight Results

During your broadcast, you can add results via:

**Control Panel**: Click on a team to show them

**API Call**:
```bash
curl -X POST "http://localhost:8000/api/teams/team001/results" \
  -H "Content-Type: application/json" \
  -d '{
    "battery_number": 1,
    "status": "validated",
    "score": 9.2,
    "notes": "Excellent flight"
  }'
```

**Python Script**:
```python
from examples.api_usage import OverlayController

controller = OverlayController()
controller.add_flight_result(
    team_id="team001",
    battery_number=1,
    status="validated",
    score=9.2,
    notes="Excellent flight"
)
```

## Updating Current Battery

```bash
curl -X PUT "http://localhost:8000/api/teams/team001/battery?battery_number=2"
```

## Adding Aircraft Photos

To add real aircraft photos, you have two options:

### Option 1: Online Images
Update the `aircraft_photo_url` field with a URL to the team's aircraft photo:

```bash
curl -X PUT "http://localhost:8000/api/teams/team001" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "team001",
    "name": "EESC-USP Alpha",
    "university": "Escola de Engenharia de São Carlos - USP",
    "aircraft_photo_url": "https://your-server.com/photos/eesc-alpha.jpg",
    "current_battery": 1,
    "flight_results": []
  }'
```

### Option 2: Local Images
1. Create a folder: `mkdir -p aircraft_photos`
2. Add images: `aircraft_photos/team001.jpg`, etc.
3. Update backend to serve static files (already configured!)
4. Use URL: `http://localhost:8000/aircraft_photos/team001.jpg`

## Next Steps

1. **Start the server**: `python backend/main.py`
2. **Open control panel**: http://localhost:8000/control-panel/index.html
3. **Set up OBS**: Add browser source with URL: http://localhost:8000/overlay/index.html
4. **Test with teams**: Click on any team in the control panel
5. **Add real photos**: Replace placeholder URLs with actual aircraft photos
6. **During competition**: Update batteries and add flight results in real-time

## Need More Teams?

The PDF contains 57 teams total. If you need all teams loaded, let me know and I can add them all!

Current teams are the **top 20 performers** from the competition.

---

**Ready to broadcast! 🛩️📺**

