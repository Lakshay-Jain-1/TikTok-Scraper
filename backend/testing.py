import questionary

def main():
    print("Settings Page")

    # Main Settings Menu
    settings_options = [
        "Max View Count – Disabled",
        "Max Follower Count – Enabled",
        "Exit Settings"
    ]

    while True:
        selected_setting = questionary.select(
            "Select a setting to configure:",
            choices=settings_options
        ).ask()

        if selected_setting == "Exit Settings":
            print("Exiting Settings...")
            break

        elif selected_setting == "Max View Count – Disabled":
            configure_setting("Max View Count")
        
        elif selected_setting == "Max Follower Count – Enabled":
            configure_follower_count()

def configure_setting(setting_name):
    """Toggle basic enable/disable settings."""
    status = questionary.select(
        f"Do you want to enable or disable {setting_name}?",
        choices=["Enable", "Disable", "Back"]
    ).ask()

    if status in ["Enable", "Disable"]:
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
        print(f"Follower count configuration set to {status.lower()}.")
    else:
        print("Returning to previous menu...")

def set_follower_count(count_type):
    count = questionary.text(f"Enter the {count_type} follower count (must be a number):").ask()

    if count.isdigit():
        print(f"The {count_type} follower count has been set to {count}.")
    else:
        print("Invalid input. Please enter a valid number.")

if __name__ == "__main__":
    main()
