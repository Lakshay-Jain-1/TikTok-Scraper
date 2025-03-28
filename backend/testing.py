import questionary

# Initial setting states
settings_status = {
    "Max View Count": "Disabled",
    "Max Follower Count": "Enabled"
}

def main():
    print("Settings Page")

    while True:
        # Dynamically update the menu with current settings
        settings_options = [
            f"Max View Count – {settings_status['Max View Count']}",
            f"Max Follower Count – {settings_status['Max Follower Count']}",
            "Exit Settings"
        ]

        selected_setting = questionary.select(
            "Select a setting to configure:",
            choices=settings_options
        ).ask()

        if selected_setting == "Exit Settings":
            print("Exiting Settings...")
            break

        elif "Max View Count" in selected_setting:
            configure_setting("Max View Count")
        
        elif "Max Follower Count" in selected_setting:
            configure_follower_count()


def configure_setting(setting_name):
    """Toggle basic enable/disable settings."""
    status = questionary.select(
        f"Do you want to enable or disable {setting_name}?",
        choices=["Enable", "Disable", "Back"]
    ).ask()

    if status in ["Enable", "Disable"]:
        settings_status[setting_name] = status
        print(f"{setting_name} has been set to {status.lower()}.")
    else:
        print("Returning to main menu...")


def configure_follower_count():
    """Additional configuration options for Follower Count."""
    sub_option = questionary.select(
        "Configure Follower Count Settings:",
        choices=[
            "Enable/Disable Configuration",
            "Set Max Follower Count",
            "Set Minimum Follower Count",
            "Back"
        ]
    ).ask()

    if sub_option == "Enable/Disable Configuration":
        toggle_follower_count()
    elif sub_option == "Set Max Follower Count":
        set_follower_count("maximum")
    elif sub_option == "Set Minimum Follower Count":
        set_follower_count("minimum")
    else:
        print("Returning to main menu...")


def toggle_follower_count():
    status = questionary.select(
        "Do you want to enable or disable follower count?",
        choices=["Enable", "Disable", "Back"]
    ).ask()

    if status in ["Enable", "Disable"]:
        settings_status["Max Follower Count"] = status
        print(f"Follower count configuration set to {status.lower()}.")
    else:
        print("Returning to previous menu...")


def set_follower_count(count_type):
    count = questionary.text(f"Enter the {count_type} follower count (e.g., '2 million', '500k'):")
    parsed_count = parse_number(count.ask())

    if parsed_count is not None:
        print(f"The {count_type} follower count has been set to {parsed_count}.")
    else:
        print("Invalid input. Please enter a valid number.")


def parse_number(text):
    """Parse numbers with words like 'million' or 'k' into actual integers."""
    text = text.lower().replace(",", "").strip()
    if "million" in text:
        return int(float(text.replace("million", "").strip()) * 1_000_000)
    elif "k" in text:
        return int(float(text.replace("k", "").strip()) * 1_000)
    elif text.isdigit():
        return int(text)
    else:
        return None


if __name__ == "__main__":
    main()
