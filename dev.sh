#!/bin/bash
# Development helper script

echo "🛩️  Aero Design Overlay - Development Tools"
echo ""

show_help() {
    echo "Usage: ./dev.sh [command]"
    echo ""
    echo "Commands:"
    echo "  start       - Start the backend server"
    echo "  test        - Run test/example script"
    echo "  interactive - Run interactive API controller"
    echo "  install     - Install dependencies"
    echo "  clean       - Clean cache and temp files"
    echo "  help        - Show this help message"
    echo ""
}

case "$1" in
    start)
        echo "Starting backend server with auto-reload..."
        uv run uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload --reload-include '*.html' --reload-include '*.json' --reload-include '*.css' --reload-include '*.js'
        ;;
    test)
        echo "Running example script..."
        python examples/api_usage.py
        ;;
    interactive)
        echo "Starting interactive mode..."
        python examples/api_usage.py --interactive
        ;;
    install)
        echo "Installing dependencies..."
        uv sync
        ;;
    clean)
        echo "Cleaning cache and temp files..."
        find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
        find . -type f -name "*.pyc" -delete 2>/dev/null || true
        find . -type f -name "*.pyo" -delete 2>/dev/null || true
        find . -type f -name "*.log" -delete 2>/dev/null || true
        echo "✅ Cleaned!"
        ;;
    help|*)
        show_help
        ;;
esac

