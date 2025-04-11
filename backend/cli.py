import questionary
from modules.setup import setup_vlc
from modules.settings import settings_menu
from modules.env import update_Api_keys

settings_menu()
setup_vlc()

searchQueries = questionary.text(
    "Enter your search queries in the format: query1,query2,query3:"
).ask()

hashtags = questionary.text(
    "Enter the hashtags  in the format: hashtag1,hashtag2,hashtag3:"
).ask()

import main
# max_results = questionary.text(
#     "Please enter the maximum number of results you want (choose a number):"
# ).ask()

main.main(searchQueries.split(","), hashtags.split(","), 25)    
