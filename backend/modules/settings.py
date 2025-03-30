import questionary
import json
from pathlib import Path
import os

Settings_File = f"{os.getcwd()}/modules/app_settings.json"
def load_global_settings() -> dict:
    """Load settings from a JSON file."""
    try:
       with open(Settings_File, 'r') as file:
        data = json.load(file)
        return data

    except Exception as e:
        print(f"Error loading settings: {e}")
    return {}

def save_global_settings(settings: dict):
    """Save settings to a JSON file."""

    try:
        with open(Settings_File, "w") as f:
            json.dump(settings, f, indent=2)
    except Exception as e:
        print(f"Error saving settings: {e}")

GLOBAL_SETTINGS = load_global_settings()

def parse_number(value: str) -> int:
    """Convert k/M suffixes to integers with error handling."""
    value = value.strip().lower().replace(',', '')
    if not value:
        raise ValueError("Empty input")
    
    multipliers = {'k': 1000, 'm': 1_000_000}
    if value[-1] in multipliers:
        return int(float(value[:-1]) * multipliers[value[-1]])
    return int(value)

def format_number(n: int) -> str:
    """Convert integer to a string with k/M suffix if applicable."""
    if n >= 1_000_000:
        quotient = n // 1_000_000
        remainder = n % 1_000_000
        if remainder == 0:
            return f"{quotient}M"
        else:
            return f"{n / 1_000_000:.1f}M".replace(".0M", "M")
    elif n >= 1000:
        quotient = n // 1000
        remainder = n % 1000
        if remainder == 0:
            return f"{quotient}k"
        else:
            return f"{n / 1000:.1f}k".replace(".0k", "k")
    else:
        return str(n)

def get_limits(limit_type: str, current_min: int = 0, current_max: int = 0):
    """Get validated limits with current global values as defaults."""
    while True:
        try:
            min_default = format_number(current_min) if current_min != 0 else "0"
            max_default = format_number(current_max) if current_max != 0 else min_default

            min_val = questionary.text(
                f"Minimum {limit_type}s (e.g., 10k, 1M):",
                validate=lambda val: val and any(c.isdigit() for c in val),
                default=min_default
            ).ask()
            
            max_val = questionary.text(
                f"Maximum {limit_type}s (e.g., 10k, 1M):",
                validate=lambda val: val and any(c.isdigit() for c in val),
                default=max_default
            ).ask()

            parsed_min = parse_number(min_val)
            parsed_max = parse_number(max_val)

            if parsed_min > parsed_max:
                raise ValueError("Maximum cannot be less than minimum.")

            return {
                f"min_{limit_type}": parsed_min,
                f"max_{limit_type}": parsed_max
            }
        except (ValueError, IndexError) as e:
            print(f"Invalid input: {e}")

def settings_menu():
    """Settings menu that uses global settings as defaults."""
    temp_settings = GLOBAL_SETTINGS.copy()  
    
    while True:
        action = questionary.select(
            "Settings Page:",
            choices=[
                {"name": f"View Limits", "value": "views"},
                {"name": f"Follower Limits", "value": "followers"},
                {"name": "Save and Exit", "value": "save"},
                {"name": "Exit Without Saving", "value": "exit"},
            ]
        ).ask()

        if action == "views":
            new_limits = get_limits(
                "view",
                temp_settings.get("min_view", 0),
                temp_settings.get("max_view", 0)
            )
            temp_settings.update(new_limits)
        elif action == "followers":
            new_limits = get_limits(
                "follower",
                temp_settings.get("min_follower", 0),
                temp_settings.get("max_follower", 0)
            )
            temp_settings.update(new_limits)
        elif action == "save":
            save_global_settings(temp_settings)
            return temp_settings
        elif action == "exit":
            return None
