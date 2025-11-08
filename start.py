#!/usr/bin/env python3
"""
Quick start script for the Aero Design Overlay System
Starts the backend server
"""

import subprocess
import sys
import webbrowser
import time
from pathlib import Path

def main():
    print("🛩️  Starting Aero Design Overlay System...")
    print("=" * 50)

    # Get the backend directory
    backend_dir = Path(__file__).parent / "backend"

    print("\n📡 Starting backend server...")
    print("   Server will be available at: http://localhost:8000")
    print("   Control Panel: http://localhost:8000/control-panel/index.html")
    print("   Overlay: http://localhost:8000/overlay/index.html")
    print("\n   Press Ctrl+C to stop the server")
    print("=" * 50)

    # Wait a bit for user to read
    time.sleep(2)

    # Open control panel in browser after a delay
    def open_browser():
        time.sleep(3)  # Wait for server to start
        webbrowser.open("http://localhost:8000/control-panel/index.html")

    import threading
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()

    # Start the server
    try:
        subprocess.run(
            [sys.executable, "backend/main.py"],
            cwd=Path(__file__).parent
        )
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down server...")
        print("Goodbye!")

if __name__ == "__main__":
    main()

