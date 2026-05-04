#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

cleanup() {
    echo "Stopping containers..."
    docker compose down -v
}
trap cleanup EXIT

echo "Starting Home Assistant + Mosquitto..."
docker compose down -v 2>/dev/null || true
docker compose up -d

echo "Setting up E2E venv..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    .venv/bin/pip install -q -r requirements.txt
fi

echo "Waiting for Home Assistant to be ready..."
for i in $(seq 1 90); do
    if curl -sf http://localhost:8123/api/onboarding > /dev/null 2>&1; then
        echo "Home Assistant is ready (took ~$((i * 2))s)"
        break
    fi
    if [ "$i" -eq 90 ]; then
        echo "ERROR: Home Assistant failed to start"
        docker compose logs homeassistant
        exit 1
    fi
    sleep 2
done

echo "Running E2E tests..."
.venv/bin/python -m pytest test_e2e.py -v --tb=short
