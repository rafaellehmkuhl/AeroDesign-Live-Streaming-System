# OBS Setup Guide

This guide will walk you through setting up the overlay in OBS Studio for your live broadcast.

## Prerequisites

- OBS Studio installed (download from https://obsproject.com/)
- Backend server running (`python backend/main.py`)
- A scene in OBS with your camera/video source

## Step-by-Step Setup

### 1. Start Your Backend Server

First, make sure your backend server is running:

```bash
python backend/main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 2. Open OBS Studio

Launch OBS Studio and select or create a scene for your broadcast.

### 3. Add Browser Source

In the **Sources** panel (bottom of OBS):

1. Click the **[+]** button
2. Select **"Browser"** from the list
3. Name it: `Aero Design Overlay`
4. Click **OK**

### 4. Configure Browser Source

In the **Properties** window that opens:

**URL**:
```
http://localhost:8000/overlay/index.html
```

**Width**: `1920`

**Height**: `1080`

**FPS**: `30` (default is fine)

**Custom CSS**: Leave empty

**Checkboxes** (recommended settings):
- ✅ **Shutdown source when not visible** - Saves resources
- ✅ **Refresh browser when scene becomes active** - Ensures fresh data
- ❌ **Control audio via OBS** - Not needed
- ❌ **Use custom frame rate** - Not needed

Click **OK** to save.

### 5. Position the Overlay

The overlay is designed to work at 1920x1080 resolution and shouldn't need repositioning. However, if needed:

1. Right-click the overlay source → **Transform** → **Reset Transform**
2. Make sure it covers your entire canvas
3. The overlay elements are positioned to not block important content:
   - Team info: Bottom-left corner
   - Flight results: Bottom-right corner
   - Messages: Top-center

### 6. Layer Order

In the **Sources** list, make sure your sources are ordered like this (top to bottom):

```
🔵 Aero Design Overlay    ← Top (overlay on top)
🎥 Camera/Video Source     ← Middle
🖼️  Background/Scene       ← Bottom (if any)
```

Drag sources up or down to reorder them.

### 7. Test the Overlay

Before going live:

1. Open the Control Panel: `http://localhost:8000/control-panel/index.html`
2. Click on a team to show their information
3. Watch the overlay appear in OBS preview
4. Try the show/hide buttons
5. Test custom messages

### 8. Troubleshooting

**Overlay not showing?**
- Check that the backend is running
- Right-click the browser source → **Interact** → Check browser console for errors
- Right-click the browser source → **Refresh**

**Overlay not updating?**
- The overlay polls every 500ms, give it a moment
- Refresh the browser source
- Check network connectivity to localhost:8000

**Wrong size/position?**
- Right-click → **Transform** → **Reset Transform**
- Verify Width: 1920, Height: 1080 in properties

**Performance issues?**
- Enable "Shutdown source when not visible"
- Close the browser console if open (Interact window)
- Reduce the poll interval in `overlay/index.html` if needed

### 9. Going Live

When you're ready to broadcast:

1. Start your stream/recording in OBS
2. Keep the backend server running throughout the broadcast
3. Use the control panel to manage what appears on screen
4. The overlay is transparent - only active elements show

### 10. Network Access (Optional)

To control the overlay from another device (tablet, phone):

1. Find your computer's IP address:
   - Mac: System Preferences → Network
   - Windows: `ipconfig` in command prompt
   - Linux: `ip addr` or `ifconfig`

2. Access the control panel from another device:
   ```
   http://YOUR_IP_ADDRESS:8000/control-panel/index.html
   ```

3. Make sure both devices are on the same network

## Advanced Tips

### Multiple Scenes

You can add the same browser source to multiple scenes:
- Right-click the source → **Add Existing** → Select "Aero Design Overlay"
- This reuses the same source across scenes

### Keyboard Shortcuts

Set up OBS hotkeys for quick control:
1. File → Settings → Hotkeys
2. Find your browser source
3. Assign keys for Show/Hide

### Recording Overlay Testing

To test without streaming:
1. Use OBS Studio Mode (View → Studio Mode)
2. Preview the overlay in the left panel
3. Make adjustments before going live

### Backup Plan

Always have a backup:
1. Test everything before the event
2. Have the browser URLs bookmarked
3. Know how to quickly hide the overlay (hotkey)
4. Practice showing/hiding in OBS

## Quick Reference

**Backend Start**: `python backend/main.py`

**Control Panel**: http://localhost:8000/control-panel/index.html

**Overlay URL for OBS**: http://localhost:8000/overlay/index.html

**API Docs**: http://localhost:8000/docs

**Overlay Size**: 1920x1080

**Poll Rate**: 500ms (0.5 seconds)

---

## Example Scene Setup

```
Scene: "Competition Stream"
├── 🔵 Aero Design Overlay (Browser)
├── 🎥 Competition Camera (Video Capture Device)
├── 🎤 Microphone (Audio Input Capture)
└── 🖼️  Background Image (optional)
```

---

## Need More Help?

- Check the main [README.md](README.md) for full documentation
- Test in browser first: http://localhost:8000/overlay/index.html
- Use the API examples in `examples/api_usage.py`

Happy broadcasting! 🎥✈️

