#!/bin/bash

# Cool It Launcher Script
# Safely launch the fan control application

set -euo pipefail  # Enable strict error handling

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_SCRIPT="${SCRIPT_DIR}/coolit.py"

# Validate that the Python script exists
if [[ ! -f "$APP_SCRIPT" ]]; then
    echo "Error: coolit.py not found in $SCRIPT_DIR" >&2
    exit 1
fi

# Validate that Python3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 not found. Please install Python 3." >&2
    exit 1
fi

# Set up display environment
export DISPLAY="${DISPLAY:-:0}"
export XAUTHORITY="${XAUTHORITY:-$HOME/.Xauthority}"

# Log the launch attempt
echo "[$(date)] Launching Cool It fan control application"
echo "Script location: $APP_SCRIPT"
echo "Running as user: $(whoami)"

# Try to run with existing sudo session, fallback to password prompt
if sudo -n python3 "$APP_SCRIPT" 2>/dev/null; then
    echo "Application launched successfully with existing sudo session"
else
    echo "Requesting sudo privileges for hardware access..."
    exec sudo python3 "$APP_SCRIPT"
fi
