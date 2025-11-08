#!/usr/bin/env python3
"""
Example script demonstrating how to control the overlay programmatically
This could be integrated with your competition scoring system
"""

import requests
import time
from typing import Optional

API_BASE = "http://localhost:8000/api"


class OverlayController:
    """
    Simple controller class for the overlay system
    """

    def __init__(self, api_base: str = API_BASE):
        self.api_base = api_base

    def show_team(self, team_id: str) -> bool:
        """Show overlay with specific team"""
        try:
            response = requests.post(f"{self.api_base}/overlay/show?team_id={team_id}")
            return response.status_code == 200
        except Exception as e:
            print(f"Error showing team: {e}")
            return False

    def hide_overlay(self) -> bool:
        """Hide the overlay"""
        try:
            response = requests.post(f"{self.api_base}/overlay/hide")
            return response.status_code == 200
        except Exception as e:
            print(f"Error hiding overlay: {e}")
            return False

    def add_flight_result(
        self,
        team_id: str,
        battery_number: int,
        status: str,
        score: Optional[float] = None,
        notes: Optional[str] = None
    ) -> bool:
        """
        Add a flight result for a team

        Args:
            team_id: Team identifier
            battery_number: Battery/round number
            status: "validated", "invalidated", "pending", or "not_flown"
            score: Optional flight score
            notes: Optional notes about the flight
        """
        try:
            data = {
                "battery_number": battery_number,
                "status": status,
                "score": score,
                "notes": notes
            }
            response = requests.post(
                f"{self.api_base}/teams/{team_id}/results",
                json=data
            )
            return response.status_code == 200
        except Exception as e:
            print(f"Error adding flight result: {e}")
            return False

    def update_current_battery(self, team_id: str, battery_number: int) -> bool:
        """Update which battery a team is currently on"""
        try:
            response = requests.put(
                f"{self.api_base}/teams/{team_id}/battery?battery_number={battery_number}"
            )
            return response.status_code == 200
        except Exception as e:
            print(f"Error updating battery: {e}")
            return False

    def set_custom_message(self, message: Optional[str]) -> bool:
        """Set a custom message to display"""
        try:
            # Get current state
            response = requests.get(f"{self.api_base}/overlay/state")
            state = response.json()

            # Update message
            state["custom_message"] = message

            # Send updated state
            response = requests.put(f"{self.api_base}/overlay/state", json=state)
            return response.status_code == 200
        except Exception as e:
            print(f"Error setting message: {e}")
            return False

    def get_teams(self) -> list:
        """Get list of all teams"""
        try:
            response = requests.get(f"{self.api_base}/teams")
            return response.json()
        except Exception as e:
            print(f"Error getting teams: {e}")
            return []


def example_competition_flow():
    """
    Example showing a typical competition workflow
    """
    controller = OverlayController()

    print("🛩️  Aero Design Overlay Controller - Example Flow\n")

    # Get teams
    teams = controller.get_teams()
    print(f"📋 Loaded {len(teams)} teams")
    for team in teams:
        print(f"   - {team['name']} ({team['id']})")

    print("\n" + "=" * 50)

    if not teams:
        print("❌ No teams found!")
        return

    # Example: First team is about to fly
    team = teams[0]
    print(f"\n✈️  {team['name']} is preparing for flight...")
    print("   Showing team on overlay...")
    controller.show_team(team['id'])
    time.sleep(3)

    # Show a message
    print("\n📢 Displaying custom message...")
    controller.set_custom_message("Próximo voo: Preparando decolagem!")
    time.sleep(3)

    # Clear message
    print("   Clearing message...")
    controller.set_custom_message(None)
    time.sleep(2)

    # Flight completed
    print(f"\n✅ Flight completed! Recording result...")
    battery = team['current_battery']
    controller.add_flight_result(
        team_id=team['id'],
        battery_number=battery,
        status="validated",
        score=9.2,
        notes="Excellent landing, smooth flight"
    )
    time.sleep(3)

    # Move to next battery
    next_battery = battery + 1
    print(f"\n🔄 Moving to battery {next_battery}...")
    controller.update_current_battery(team['id'], next_battery)
    time.sleep(2)

    # Next team
    if len(teams) > 1:
        next_team = teams[1]
        print(f"\n👥 Switching to next team: {next_team['name']}...")
        controller.show_team(next_team['id'])
        time.sleep(3)

    # Hide overlay
    print("\n🔚 End of demonstration, hiding overlay...")
    controller.hide_overlay()

    print("\n✅ Example flow completed!")
    print("\n💡 Tip: You can integrate this controller with your scoring system")
    print("   to automatically update the overlay as events happen!")


def interactive_mode():
    """
    Interactive mode for manual testing
    """
    controller = OverlayController()

    print("🛩️  Aero Design Overlay Controller - Interactive Mode\n")
    print("Commands:")
    print("  list              - List all teams")
    print("  show <team_id>    - Show team on overlay")
    print("  hide              - Hide overlay")
    print("  result <team_id> <battery> <status> <score> - Add flight result")
    print("  message <text>    - Set custom message")
    print("  clear             - Clear custom message")
    print("  quit              - Exit")
    print()

    while True:
        try:
            cmd = input(">>> ").strip().split()

            if not cmd:
                continue

            if cmd[0] == "quit":
                break

            elif cmd[0] == "list":
                teams = controller.get_teams()
                for team in teams:
                    print(f"  {team['id']}: {team['name']} (Battery {team['current_battery']})")

            elif cmd[0] == "show" and len(cmd) > 1:
                team_id = cmd[1]
                if controller.show_team(team_id):
                    print(f"✅ Showing {team_id}")
                else:
                    print("❌ Failed")

            elif cmd[0] == "hide":
                if controller.hide_overlay():
                    print("✅ Overlay hidden")
                else:
                    print("❌ Failed")

            elif cmd[0] == "result" and len(cmd) >= 4:
                team_id = cmd[1]
                battery = int(cmd[2])
                status = cmd[3]
                score = float(cmd[4]) if len(cmd) > 4 else None

                if controller.add_flight_result(team_id, battery, status, score):
                    print("✅ Result added")
                else:
                    print("❌ Failed")

            elif cmd[0] == "message" and len(cmd) > 1:
                message = " ".join(cmd[1:])
                if controller.set_custom_message(message):
                    print("✅ Message set")
                else:
                    print("❌ Failed")

            elif cmd[0] == "clear":
                if controller.set_custom_message(None):
                    print("✅ Message cleared")
                else:
                    print("❌ Failed")

            else:
                print("❌ Unknown command or missing arguments")

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ Error: {e}")

    print("\n👋 Goodbye!")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive_mode()
    else:
        example_competition_flow()

