#!/usr/bin/env python3
"""
Script to update team aircraft photos to use local images
"""

import json
from pathlib import Path

# Get paths
backend_dir = Path(__file__).parent / "backend"
photos_dir = Path(__file__).parent / "overlay" / "assets" / "plane-photos"
json_path = backend_dir / "mock_data.json"

# Load the JSON
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Update each team's photo URL
for team in data['teams']:
    team_id = team['id']

    # Check for team-specific photos (try different extensions)
    photo_found = False
    for ext in ['.jpg', '.jpeg', '.png', '.gif']:
        photo_path = photos_dir / f"{team_id}{ext}"
        if photo_path.exists():
            team['aircraft_photo_url'] = f"assets/plane-photos/{team_id}{ext}"
            photo_found = True
            print(f"✓ {team['name']}: Found photo {team_id}{ext}")
            break

    if not photo_found:
        # Use default photo
        team['aircraft_photo_url'] = "assets/plane-photos/default.jpg"
        print(f"○ {team['name']}: Using default photo")

# Save updated JSON
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"\n✅ Updated {len(data['teams'])} teams in {json_path}")
print(f"📁 Photos directory: {photos_dir}")

