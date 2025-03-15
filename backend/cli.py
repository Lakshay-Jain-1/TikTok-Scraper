import questionary
import main


searchQueries = questionary.text(
    "Please enter your search query (you may enter multiple keywords separated by commas):"
).ask()

hashtags = questionary.text(
    "Please enter the hashtags you would like to use (separate multiple hashtags with commas):"
).ask()

max_results = questionary.text(
    "Please enter the maximum number of results you want (choose a number up to 10):"
).ask()

main.main(searchQueries.split(","), hashtags.split(","), int(max_results))