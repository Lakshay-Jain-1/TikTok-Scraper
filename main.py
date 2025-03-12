from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_tiktok_videos(query):
    search_url = f"https://www.tiktok.com/search?q={query.replace(' ', '+')}"
    
    # Setup Chrome options
    chrome_options = Options()
    # Uncomment this line to run in headless mode (disable for debugging)
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Set a user-agent to bypass bot detection
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    # Start WebDriver
    service = Service()  # Auto-detect ChromeDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        driver.get(search_url)

        # Wait for video links to load
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//a[contains(@href, "/video/")]'))
        )

        # Extract video URLs
        video_elements = driver.find_elements(By.XPATH, '//a[contains(@href, "/video/")]')
        video_urls = [elem.get_attribute("href") for elem in video_elements if elem.get_attribute("href")]

        return list(set(video_urls))  # Remove duplicates

    finally:
        driver.quit()

# Example usage
query = "AI technology"
video_urls = scrape_tiktok_videos(query)
print(video_urls)
