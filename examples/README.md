# API Usage Examples

This directory contains example scripts demonstrating how to use the overlay system programmatically.

## Scripts

### `api_usage.py`

A Python script showing how to control the overlay from your own code. Useful if you want to integrate the overlay with your competition management system.

**Run the example flow:**
```bash
python examples/api_usage.py
```

**Run in interactive mode:**
```bash
python examples/api_usage.py --interactive
```

## Integration Ideas

You can integrate this overlay system with:

1. **Competition Scoring System**: Automatically update overlays when judges enter scores
2. **Timer System**: Show countdowns and timing information
3. **External Controller**: Use a tablet or phone app to control overlays
4. **Automated Scripts**: Create scripts for common overlay sequences

## Example Integration

```python
from examples.api_usage import OverlayController

controller = OverlayController()

# When a team starts their flight
controller.show_team("team001")

# When they complete the flight
controller.add_flight_result(
    team_id="team001",
    battery_number=3,
    status="validated",
    score=8.7,
    notes="Good flight"
)

# When moving to next team
controller.show_team("team002")
```

