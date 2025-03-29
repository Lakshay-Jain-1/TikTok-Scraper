# import questionary
# import json
# from pathlib import Path

# # File to store settings
# SETTINGS_FILE = "app_settings.json"

# def load_global_settings() -> dict:
#     """Load settings from a JSON file."""
#     try:
#         if Path(SETTINGS_FILE).exists():
#             with open(SETTINGS_FILE, "r") as f:
#                 return json.load(f)
#     except Exception as e:
#         print(f"Error loading settings: {e}")
#     return {}

# def save_global_settings(settings: dict):
#     """Save settings to a JSON file."""
#     try:
#         with open(SETTINGS_FILE, "w") as f:
#             json.dump(settings, f, indent=2)
#     except Exception as e:
#         print(f"Error saving settings: {e}")

# GLOBAL_SETTINGS = load_global_settings()

# def parse_number(value: str) -> int:
#     """Convert k/M suffixes to integers with error handling."""
#     value = value.strip().lower().replace(',', '')
#     if not value:
#         raise ValueError("Empty input")
    
#     multipliers = {'k': 1000, 'm': 1_000_000}
#     if value[-1] in multipliers:
#         return int(float(value[:-1]) * multipliers[value[-1]])
#     return int(value)

# def format_number(n: int) -> str:
#     """Convert integer to a string with k/M suffix if applicable."""
#     if n >= 1_000_000:
#         quotient = n // 1_000_000
#         remainder = n % 1_000_000
#         if remainder == 0:
#             return f"{quotient}M"
#         else:
#             return f"{n / 1_000_000:.1f}M".replace(".0M", "M")
#     elif n >= 1000:
#         quotient = n // 1000
#         remainder = n % 1000
#         if remainder == 0:
#             return f"{quotient}k"
#         else:
#             return f"{n / 1000:.1f}k".replace(".0k", "k")
#     else:
#         return str(n)

# def get_limits(limit_type: str, current_min: int = 0, current_max: int = 0):
#     """Get validated limits with current global values as defaults."""
#     while True:
#         try:
#             min_default = format_number(current_min) if current_min != 0 else "0"
#             max_default = format_number(current_max) if current_max != 0 else min_default

#             min_val = questionary.text(
#                 f"Minimum {limit_type}s (e.g., 10k, 1M):",
#                 validate=lambda val: val and any(c.isdigit() for c in val),
#                 default=min_default
#             ).ask()
            
#             max_val = questionary.text(
#                 f"Maximum {limit_type}s (e.g., 10k, 1M):",
#                 validate=lambda val: val and any(c.isdigit() for c in val),
#                 default=max_default
#             ).ask()

#             parsed_min = parse_number(min_val)
#             parsed_max = parse_number(max_val)

#             if parsed_min > parsed_max:
#                 raise ValueError("Maximum cannot be less than minimum.")

#             return {
#                 f"min_{limit_type}": parsed_min,
#                 f"max_{limit_type}": parsed_max
#             }
#         except (ValueError, IndexError) as e:
#             print(f"Invalid input: {e}")

# def settings_menu():
#     """Settings menu that uses global settings as defaults."""
#     temp_settings = GLOBAL_SETTINGS.copy()  # Work on a temporary copy
    
#     while True:
#         action = questionary.select(
#             "Settings Page:",
#             choices=[
#                 {"name": f"View Limits ({format_number(temp_settings.get('min_view', 0))}-{format_number(temp_settings.get('max_view', 0))})", "value": "views"},
#                 {"name": f"Follower Limits ({format_number(temp_settings.get('min_follower', 0))}-{format_number(temp_settings.get('max_follower', 0))})", "value": "followers"},
#                 {"name": "Save and Exit", "value": "save"},
#                 {"name": "Exit Without Saving", "value": "exit"},
#             ]
#         ).ask()

#         if action == "views":
#             new_limits = get_limits(
#                 "view",
#                 temp_settings.get("min_view", 0),
#                 temp_settings.get("max_view", 0)
#             )
#             temp_settings.update(new_limits)
#         elif action == "followers":
#             new_limits = get_limits(
#                 "follower",
#                 temp_settings.get("min_follower", 0),
#                 temp_settings.get("max_follower", 0)
#             )
#             temp_settings.update(new_limits)
#         elif action == "save":
#             return temp_settings
#         elif action == "exit":
#             return None

# if __name__ == "__main__":
#     # Load existing settings at startup
#     GLOBAL_SETTINGS.update(load_global_settings())
    
#     # Run settings menu
#     new_settings = settings_menu()
    
#     if new_settings is not None:
#         GLOBAL_SETTINGS.update(new_settings)
#         save_global_settings(GLOBAL_SETTINGS)
#         print("\nSaved Settings:")
#         print(f"Views: {format_number(GLOBAL_SETTINGS.get('min_view', 0))}-{format_number(GLOBAL_SETTINGS.get('max_view', 0))}")
#         print(f"Followers: {format_number(GLOBAL_SETTINGS.get('min_follower', 0))}-{format_number(GLOBAL_SETTINGS.get('max_follower', 0))}")
#     else:
#         print("\nExited without saving changes")





# import requests
# import json

# GEMINI_API_KEY = 'AIzaSyBaANl7m1QamNyJZZHUUKbulV-y45z6ohk'

# def refine_query_and_hashtags(query, hashtags, use_gemini):
#     if not use_gemini.lower() == "yes":
#         return query, hashtags  # Return input if not using Gemini AI
    
#     headers = {
#         'Content-Type': 'application/json',
#     }
#     data = {
#         "contents": [{
#             "parts": [{"text": f"Refine the following search query and hashtags for better SEO, user engagement, and trending relevance. Only provide the refined query and hashtags without additional explanation.\nQuery: {query}\nHashtags: {hashtags}"}]
#         }]
#     }
#     url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    
#     response = requests.post(url, headers=headers, data=json.dumps(data))
    
#     if response.status_code == 200:
#         response_data = response.json()
#         refined_response = response_data["candidates"][0]["content"]["parts"][0]["text"]

#         # Extract refined query and hashtags
#         refined_query = query
#         refined_hashtags = hashtags
        
#         if "Query:" in refined_response and "Hashtags:" in refined_response:
#             parts = refined_response.split("Hashtags:")
#             refined_query = parts[0].split("Query:")[1].strip()
#             refined_hashtags = parts[1].strip()

#         # Clean the refined query and hashtags
#         refined_query = refined_query.strip().replace("**", "").strip()  # Remove any unwanted symbols from query

#         if isinstance(refined_hashtags, str):
#             refined_hashtags_list = [hashtag.strip("#").strip() for hashtag in refined_hashtags.split()]

#             # Remove unwanted symbols like '[' or ']' from hashtags
#             refined_hashtags_list = [hashtag.replace('[','').replace(']','').replace('**','') for hashtag in refined_hashtags_list]
#         else:
#             refined_hashtags_list = [hashtag.strip("#").strip() for hashtag in refined_hashtags]

#         return refined_query.strip(), refined_hashtags_list
#     else:
#         return f"API Error: Status Code {response.status_code} - {response.text}"

# # User input for query and Gemini AI usage
# query = input("Enter your search query: ")
# hashtags_input = input("Enter your search hashtags (comma separated): ")
# hashtags = hashtags_input.split(", ")

# use_gemini = input("Do you want to use Gemini AI for refining the query and hashtags? (yes/no): ")

# # Get the refined query and hashtags
# refined_query, refined_hashtags = refine_query_and_hashtags(query, hashtags, use_gemini)

# # Output final results
# print("\nRefined Query:")
# print(refined_query)
# print("\nOptimized Hashtags:")
# print(refined_hashtags)




import requests
import json

GEMINI_API_KEY = 'AIzaSyBaANl7m1QamNyJZZHUUKbulV-y45z6ohk'

def refine_query_and_hashtags(query, hashtags, use_gemini):
    if not use_gemini.lower() == "yes":
        return query, hashtags  # Return input if not using Gemini AI
    
    headers = {
        'Content-Type': 'application/json',
    }
    data = {
        "contents": [{
            "parts": [{"text": f"Refine the following search query and hashtags for better SEO, user engagement, and trending relevance. Only provide the refined query and hashtags without additional explanation.\nQuery: {query}\nHashtags: {hashtags}"}]
        }]
    }
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        response_data = response.json()
        refined_response = response_data["candidates"][0]["content"]["parts"][0]["text"]

        # Extract refined query and hashtags
        refined_query = query
        refined_hashtags = hashtags
        
        if "Query:" in refined_response and "Hashtags:" in refined_response:
            parts = refined_response.split("Hashtags:")
            refined_query = parts[0].split("Query:")[1].strip()
            refined_hashtags = parts[1].strip()

        # Clean the refined query and hashtags
        refined_query = refined_query.strip().replace("**", "").strip()  # Remove any unwanted symbols from query

        if isinstance(refined_hashtags, str):
            refined_hashtags_list = [hashtag.strip("#").strip() for hashtag in refined_hashtags.split()]

            # Remove unwanted symbols like '[' or ']' from hashtags
            refined_hashtags_list = [hashtag.replace('[','').replace(']','').replace("'", "").replace(",", "") for hashtag in refined_hashtags_list]
        else:
            refined_hashtags_list = [hashtag.strip("#").strip() for hashtag in refined_hashtags]

        return refined_query.strip(), refined_hashtags_list
    else:
        return f"API Error: Status Code {response.status_code} - {response.text}"

# User input for query and Gemini AI usage
query = input("Enter your search query: ")
hashtags_input = input("Enter your search hashtags (comma separated): ")
hashtags = hashtags_input.split(", ")

use_gemini = input("Do you want to use Gemini AI for refining the query and hashtags? (yes/no): ")

# Get the refined query and hashtags
refined_query, refined_hashtags = refine_query_and_hashtags(query, hashtags, use_gemini)

# Output final results
print("\nRefined Query:")
print(refined_query)
print("\nOptimized Hashtags:")
print(refined_hashtags)
