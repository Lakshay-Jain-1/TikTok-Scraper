import questionary
import os

choice=questionary.text(
        "Do you want to edit out your api keys: (y or n)"
    ).ask()

choice=choice.lower().strip()

def update_Api_keys():
    apiKeys = questionary.text(
        "Enter your api keys eg:- apify_api_FKgR1TkkRsa6RlVgqCDxWxcwrPa4PY0wyQeP,1830b5b59bmsh9a4dc5077af3396p155ba7jsn200b149d6b93 "
    ).ask()

    apiKeys=apiKeys.strip()
    apiKeys=apiKeys.split(",")

    backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    env_file_path = os.path.join(backend_dir, ".env")


    with open(env_file_path, "w") as f:
        f.write("")

    for i in apiKeys:
        if "apify_api" in i:
            with open(env_file_path, "a") as f:
                f.write(f'TIKTOK_SCRAPPER_API_TOKEN="{i.strip()}"\n')
                f.write(f'CONSTRAINTS_API_KEY="{i.strip()}"\n')
        else:
            with open(env_file_path, "a") as f:
                f.write(f'DOWNLOAD_TIKTOK_API_TOKEN="{i.strip()}"\n')
                f.write(f'GOOGLE_API_KEY="AIzaSyAa1DVXYCB-HVSVW2VIY07QKh1yzANayxk"\n')

if choice=="y":
    update_Api_keys()    
