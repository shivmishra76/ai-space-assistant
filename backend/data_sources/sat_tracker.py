"""
Interface to sat-tracker-cli for satellite tracking and pass predictions.
"""

import subprocess
import json
import re


def get_satellite_location(sat_name: str, selection: int = None) -> str:
    """Call sat-tracker-cli for any satellite and return a user-friendly summary. If multiple matches, prompt for selection."""
    try:
        args = ["python", "/Users/shivmishra/sat_tracker_cli/main.py", sat_name, "--json"]
        if selection is not None:
            args.append(str(selection))
        result = subprocess.run(
            args,
            text=True,
            capture_output=True,
        )
        if not result.stdout:
            return f"sat-tracker-cli did not return data. Error/output: {result.stderr.strip()}"
        try:
            data = json.loads(result.stdout)
        except Exception:
            # Try to detect multiple matches in the output
            matches = re.findall(r"\d+\.\s+([\w\s\-\(\)]+)", result.stdout)
            if matches:
                numbered = "\n".join(f"{i+1}. {name.strip()}" for i, name in enumerate(matches))
                return (
                    "Multiple satellites found. Please select one by typing its number and re-ask your question.\n" +
                    numbered
                )
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


def get_satellite_location_json(*args):
    """Call sat-tracker-cli for any satellite and return the raw JSON dict, or error/ambiguous message."""
    try:
        cli_args = ["python", "/Users/shivmishra/sat_tracker_cli/main.py"] + list(args)
        print(cli_args)
        result = subprocess.run(
            cli_args,
            text=True,
            capture_output=True,
        )
        if not result.stdout:
            return f"sat-tracker-cli did not return data. Error/output: {result.stderr.strip()}"
        try:
            data = json.loads(result.stdout)
            return data
        except Exception:
            # Try to detect multiple matches in the output
            matches = re.findall(r"\d+\.\s+([\w\s\-\(\)]+)", result.stdout)
            if matches:
                numbered = "\n".join(f"{i+1}. {name.strip()}" for i, name in enumerate(matches))
                return (
                    "Multiple satellites found. Please select one by typing its number and re-ask your question.\n" +
                    numbered
                )
            return f"sat-tracker-cli did not return JSON. Output: {result.stdout.strip() or result.stderr.strip()}"
    except Exception as e:
        return f"Error calling sat-tracker-cli: {e}"
