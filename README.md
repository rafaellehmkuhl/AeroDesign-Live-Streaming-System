# Aero Design - Live Transmission Overlay System

A complete live broadcast overlay system designed for aero design competitions, allowing you to display dynamic information over your video stream in OBS.

## 🎯 Features

- **Real-time Overlays**: Display team information, aircraft photos, and flight results
- **Web-based Control Panel**: Easy-to-use interface to control what appears on stream
- **OBS Integration**: Works seamlessly with OBS Browser Sources
- **Mock API**: Pre-loaded with sample data for testing
- **Customizable**: Show/hide different elements, add custom messages
- **Responsive Design**: Professional-looking overlays with smooth animations

## 📋 What Gets Displayed

The overlay can show:
- **Team Information**: Team name, university, aircraft photo
- **Current Battery**: Which round (battery) the team is currently flying
- **Flight Results**: Results from previous batteries with validation status and scores
- **Custom Messages**: Display important announcements or messages

## 🏗️ Architecture

```
┌─────────────────┐
│  Control Panel  │ ← You control the overlay here
│  (Web Browser)  │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  Python Backend │ ← FastAPI server with REST API
│   (Port 8000)   │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  Overlay Page   │ ← Add this as Browser Source in OBS
│  (Polls API)    │
└─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- UV package manager (or pip)
- OBS Studio (for broadcasting)
- A modern web browser

### Installation

1. **Clone or navigate to the repository:**

```bash
cd /Users/rafael/Documents/git/aero-tv-transmission-overlayer
```

2. **Install dependencies using UV:**

```bash
uv sync
```

Or if you prefer pip:

```bash
pip install -e .
```

### Running the Application

1. **Start the backend server:**

```bash
python backend/main.py
```

Or with uvicorn directly:

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

The server will start on `http://localhost:8000`

2. **Open the Control Panel:**

Open your web browser and go to:
```
http://localhost:8000/control-panel/index.html
```

3. **Test the overlay in browser:**

Before adding to OBS, test it in your browser:
```
http://localhost:8000/overlay/index.html
```

## 🎥 Setting Up in OBS

1. **Open OBS Studio**

2. **Add a Browser Source:**
   - Click the `+` button in the Sources panel
   - Select "Browser"
   - Name it "Aero Design Overlay"

3. **Configure the Browser Source:**
   - **URL**: `http://localhost:8000/overlay/index.html`
   - **Width**: `1920`
   - **Height**: `1080`
   - ✅ Check "Shutdown source when not visible"
   - ✅ Check "Refresh browser when scene becomes active"

4. **Position the overlay:**
   - The overlay is designed for 1920x1080 (Full HD)
   - It should cover your entire video canvas
   - Elements are positioned to not obstruct the center of the video

5. **Layer it over your camera:**
   - Make sure the Browser Source is above your camera/video source in the layers

## 🎮 Using the Control Panel

### Quick Controls

- **Show Overlay**: Make the overlay visible on stream
- **Hide Overlay**: Hide all overlay elements
- **Toggle Overlay**: Switch visibility on/off

### Selecting a Team

Click on any team card to:
- Select that team
- Automatically show their information on the overlay
- Display their current battery and flight results

### Overlay Settings

- **Show Team Info**: Toggle the team information card
- **Show Flight Results**: Toggle the flight results panel
- **Show Current Battery**: Toggle the current battery badge
- **Custom Message**: Add a custom message that appears at the top

Click "Apply Settings" after making changes.

## 📡 API Endpoints

The backend provides a REST API that you can use programmatically:

### Overlay Control

- `GET /api/overlay/state` - Get current overlay state (polled by OBS)
- `PUT /api/overlay/state` - Update overlay state
- `POST /api/overlay/show?team_id=<id>` - Show overlay for specific team
- `POST /api/overlay/hide` - Hide overlay
- `POST /api/overlay/toggle` - Toggle overlay visibility

### Team Management

- `GET /api/teams` - Get all teams
- `GET /api/teams/{team_id}` - Get specific team
- `POST /api/teams` - Create new team
- `PUT /api/teams/{team_id}` - Update team
- `DELETE /api/teams/{team_id}` - Delete team

### Flight Results

- `POST /api/teams/{team_id}/results` - Add flight result
- `PUT /api/teams/{team_id}/battery` - Update current battery

### Example API Usage

```bash
# Show overlay with team
curl -X POST "http://localhost:8000/api/overlay/show?team_id=team001"

# Hide overlay
curl -X POST "http://localhost:8000/api/overlay/hide"

# Get all teams
curl "http://localhost:8000/api/teams"

# Add flight result
curl -X POST "http://localhost:8000/api/teams/team001/results" \
  -H "Content-Type: application/json" \
  -d '{"battery_number": 4, "status": "validated", "score": 9.5, "notes": "Excellent performance"}'
```

## 🧪 Mock Data

The system comes pre-loaded with three mock teams:
- **AeroTech Racing** - Universidade de São Paulo
- **Sky Pioneers** - Instituto Tecnológico de Aeronáutica
- **Falcon Engineering** - Universidade Federal de Minas Gerais

Each team has sample flight results you can use for testing.

## 🎨 Customization

### Changing Colors

Edit `overlay/index.html` and modify the CSS:
- Team card gradient: `.team-info-card` background
- Flight results: `.flight-results` background
- Status colors: `.validated`, `.invalidated`, `.pending` border-left-color

### Changing Layout

The overlay is positioned using absolute positioning:
- Team info: Bottom-left (40px from edges)
- Flight results: Bottom-right (40px from edges)
- Custom message: Top-center (40px from top)

Adjust these values in the CSS to reposition elements.

### Adding Your Logo

Add your logo to the overlay by modifying `overlay/index.html`:

```html
<div class="logo">
  <img src="your-logo-url.png" alt="Logo">
</div>
```

## 🔧 Configuration

### Changing the Poll Interval

In `overlay/index.html`, modify the `POLL_INTERVAL` constant:

```javascript
const POLL_INTERVAL = 500; // milliseconds (default: 500ms)
```

Lower values = more responsive, higher CPU usage
Higher values = less responsive, lower CPU usage

### Changing the Port

In `backend/main.py`, modify the port in the `if __name__ == "__main__":` block:

```python
uvicorn.run(app, host="0.0.0.0", port=8000)  # Change 8000 to your port
```

## 📁 Project Structure

```
aero-tv-transmission-overlayer/
├── backend/
│   └── main.py              # FastAPI backend server
├── overlay/
│   └── index.html           # OBS browser source overlay
├── control-panel/
│   └── index.html           # Control panel interface
├── pyproject.toml           # Python dependencies (UV)
├── .gitignore
└── README.md
```

## 🐛 Troubleshooting

### Overlay not updating in OBS

1. Make sure the backend is running
2. Check the OBS browser source URL is correct
3. Right-click the browser source → Interact → Open browser console (F12) to check for errors
4. Try refreshing the browser source (right-click → Refresh)

### CORS Errors

The backend has CORS enabled for all origins in development. If you need to restrict it, modify the `CORSMiddleware` configuration in `backend/main.py`.

### Port Already in Use

If port 8000 is already in use:
1. Change the port in `backend/main.py`
2. Update the API_URL in `overlay/index.html`
3. Update the API_BASE in `control-panel/index.html`

### Teams Not Loading

Check that the backend initialized correctly:
```bash
curl http://localhost:8000/api/teams
```

Should return the three mock teams.

## 🚀 Production Deployment

For production use:

1. **Use a real database** instead of in-memory storage
2. **Add authentication** to the control panel
3. **Use HTTPS** for secure connections
4. **Configure CORS** properly for your domain
5. **Add error logging** and monitoring
6. **Upload aircraft photos** to a CDN or server

## 📝 Notes

- The system uses in-memory storage, so data resets when the server restarts
- Aircraft photos use placeholder images by default
- The overlay is designed for 1920x1080 resolution
- All text is in Portuguese (BR) but can be easily translated

## 🤝 Contributing

Feel free to customize and extend this system for your competition needs!

## 📄 License

This project is open source and available for use in your competitions.

## 🎓 Credits

Built for the Aero Design competition with ❤️

---

**Need help?** Check the API documentation at `http://localhost:8000/docs` (FastAPI automatic docs)

