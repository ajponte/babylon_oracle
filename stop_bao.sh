#!/usr/bin/env bash
set -euo pipefail

# --- Configuration ---
BAO_LOG_FILE="./bao.log"

# --- Functions ---

stop_server() {
  # Find the Bao server process
  local PID
  PID=$(pgrep -f "bao server" || true)

  if [[ -z "$PID" ]]; then
    echo "No Bao server process found."
    return
  fi

  echo "Stopping Bao server (PID $PID)..."
  kill "$PID"

  # Wait for clean shutdown
  for i in {1..10}; do
    if ! pgrep -f "bao server" > /dev/null; then
      echo "Bao server stopped cleanly."
      return
    fi
    sleep 0.5
  done

  echo "Force killing Bao server..."
  pkill -9 -f "bao server" || true
  echo "Bao server terminated."

  # Optionally show last few log lines for debugging
  if [[ -f "$BAO_LOG_FILE" ]]; then
    echo
    echo "--- Last 10 lines of $BAO_LOG_FILE ---"
    tail -n 10 "$BAO_LOG_FILE" || true
  fi
}

# --- Main Flow ---
stop_server
