# Quick Start Guide 🚀

Get your overlay system running in 3 minutes!

## Step 1: Install Dependencies

```bash
uv sync
```

## Step 2: Start the Server

```bash
python backend/main.py
```

Or use the quick start script:

```bash
python start.py
```

## Step 3: Access the Interface

The control panel will automatically open in your browser at:
- **Control Panel**: http://localhost:8000/control-panel/index.html
- **Overlay (for OBS)**: http://localhost:8000/overlay/index.html
- **API Docs**: http://localhost:8000/docs

## Step 4: Configure OBS

1. Open OBS Studio
2. Add a **Browser Source**:
   - URL: `http://localhost:8000/overlay/index.html`
   - Width: `1920`
   - Height: `1080`
3. Position it above your camera source

## Step 5: Control the Overlay

1. Open the Control Panel in your browser
2. Click on a team to show their info
3. Use the Quick Controls to show/hide the overlay
4. Customize settings and messages

That's it! You're ready to broadcast! 🎉

---

## What's Next?

- Read the full [README.md](README.md) for detailed documentation
- Check [examples/api_usage.py](examples/api_usage.py) for programmatic control
- Customize the overlay appearance in `overlay/index.html`
- Add your own teams via the API

## Need Help?

- Check the API documentation at http://localhost:8000/docs
- Read the troubleshooting section in README.md
- Test the overlay in your browser before adding to OBS

---

## Quick Tips

✅ Test the overlay in your browser first before adding to OBS
✅ Keep the backend server running while broadcasting
✅ Use the control panel from any device on the same network
✅ The overlay auto-refreshes every 500ms - no need to reload OBS

🎥 Happy broadcasting!

