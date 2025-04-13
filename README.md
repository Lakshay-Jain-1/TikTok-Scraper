# Tik Tok Scraper

## Directory Structure

A CLI-based TikTok video automation pipeline with modular components for refining queries, 
scraping video URLs, downloading, and merging videos — built for extensibility and manual testing.

```
├── README.md                      # Root project overview  
├── backend  
│   ├── cli.py                    # CLI entry point for the application  
│   ├── main.py                   # Main controller orchestrating the pipeline phases  
│   ├── modules                   # Core logic and utilities  
│   │   ├── app_settings.json     # JSON config for app settings  
│   │   ├── constraints.py        # Filters out videos based on metadata rules  
│   │   ├── downloader.py         # Downloads TikTok videos; supports manual testing  
│   │   ├── env.py                # Environment variable configuration  
│   │   ├── merge.py              # Merges multiple downloaded videos  
│   │   ├── output.json           # Output data or example structure  
│   │   ├── query_hashtag_refiner.py  # Refines queries and hashtags using Gemini AI  
│   │   ├── scraper.py            # Extracts TikTok video URLs from given inputs  
│   │   ├── settings.py           # General app settings  
│   │   └── setup.py              # Initial setup logic  
│   └── requirements.txt          # Python dependencies    
├── run.bat                       # Batch script to run the CLI (experimental)
```

---

## Phases of the Project

The TikTok video automation pipeline is broken down into the following key phases:

### Phase 0: Refining Search Queries (Optional)

- Uses Gemini AI to enhance and fine-tune user-provided search queries and hashtags.
- Triggered based on user input (`y/n`) at runtime.
- Function: `refine_query_and_hashtags()` from `query_hashtag_refiner.py`.

### Phase 1: Scraping TikTok Video URLs

- Calls `extractVideoUrls()` from `scraper.py` to fetch relevant video URLs using search queries and hashtags.
- The returned video metadata is filtered using rules defined in `constraints.py`.

### Phase 2: Downloading Videos

- Downloads TikTok videos using `batch_download()` from `downloader.py`.
- Supports manual testing of downloads.
- Uses `count_videos_in_downloads()` to report how many videos were successfully downloaded.

### Phase 3: Merging Videos (Optional)

- After download, users are prompted whether to merge the videos in the Downloads folder.
- If accepted, `merging()` from `merge.py` combines the downloaded files.

---

## How to Run This Project

```bash
git clone https://github.com/Lakshay-Jain-1/TikTok-Scraper.git
cd .\TikTok-Scraper\
cd backend 
pip install -r requirements.txt
python cli.py
```
