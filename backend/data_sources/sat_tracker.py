"""
Interface to sat-tracker-cli for satellite tracking and pass predictions.
"""

import subprocess
import json


def get_iss_location() -> str:
    """Call sat-tracker-cli to get current ISS location and return a user-friendly summary."""
    try:
        result = subprocess.run(
            ["python", "/Users/shivmishra/sat_tracker_cli/main.py", "hst", "--json"],
            text=True,
            capture_output=True,
        )
        if not result.stdout:
            # If no output, show stderr or a helpful message
            return f"sat-tracker-cli did not return data. Error/output: {result.stderr.strip()}"
        try:
            data = json.loads(result.stdout)
        except Exception:
            # Output is not JSON, likely a prompt or error
            return f"sat-tracker-cli did not return JSON. Output: {result.stdout.strip() or result.stderr.strip()}"
        sat = data.get("satellite", {})
        pos = sat.get("position", {})
        vis = data.get("visibility", {})
        summary = (
            f"🛰️ {sat.get('name', 'Unknown')}\n"
            f"Position: {pos.get('latitude', '?'):.2f}°N, {pos.get('longitude', '?'):.2f}°E, {pos.get('altitude_km', '?'):.1f} km altitude\n"
            f"Velocity: {pos.get('velocity_kms', '?')} km/s\n"
            f"Time: {data.get('timestamp', '?')} UTC\n"
            f"Visibility: Elevation {vis.get('elevation_degrees', '?')}°, Azimuth {vis.get('azimuth_degrees', '?')}°, Range {vis.get('range_km', '?')} km\n"
            f"{'✅ Visible above horizon' if vis.get('is_visible') else '❌ Not currently visible'}"
        )
        return summary
    except Exception as e:
        return f"Error calling sat-tracker-cli: {e}"
