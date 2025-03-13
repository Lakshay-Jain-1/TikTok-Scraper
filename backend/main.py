from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import urllib.parse
import time
import random

def brave_tor_scraper(query):
    options = Options()
    options.binary_location = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
    options.add_argument("--incognito")
    options.add_argument("--tor")
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    # Anti-detection settings
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        driver.get(f"https://www.tiktok.com/search?q={urllib.parse.quote(query)}")
        
        # Wait for video containers to load
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href*="/video/"]'))
        )
        
        # Scroll and collect links
        video_urls = set()
        scroll_attempts = 3
        
        for _ in range(scroll_attempts):
            # Find all video anchor tags
            video_links = driver.find_elements(
                By.CSS_SELECTOR, 
                'a.css-1mdo0pl-AVideoContainer[href*="/video/"]'
            )
            
            # Extract href attributes
            for link in video_links:
                try:
                    url = link.get_attribute('href')
                    if url and '/video/' in url:
                        video_urls.add(url)
                except Exception as e:
                    continue
                    
            # Natural scrolling behavior
            driver.execute_script("window.scrollBy(0, window.innerHeight * 1.2)")
            time.sleep(random.uniform(1.5, 3.5))  # Random delay between scrolls
            
        return list(video_urls)
    
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return []
    finally:
        driver.quit()

if __name__ == "__main__":
    results = brave_tor_scraper("Student Loans Income Driven Repayment Plans Are Now Over! | Why Your Credit Score Crashed")
    print(f"\nFound {len(results)} video URLs:")
    for idx, url in enumerate(results, 1):
        print(f"{idx}. {url}")