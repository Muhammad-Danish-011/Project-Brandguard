from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from selenium_stealth import stealth
import os
from datetime import datetime

def fullpage_screenshot(driver, folder, file):
    """Capture a full-page screenshot using JavaScript"""
    js = (
        "return Math.max( document.body.scrollHeight, document.body.offsetHeight, "
        "document.documentElement.clientHeight, document.documentElement.scrollHeight, "
        "document.documentElement.offsetHeight);"
    )
    scroll_height = driver.execute_script(js)

    # Set window size to capture the entire page
    driver.set_window_size(1920, scroll_height)

    # Scroll horizontally to the right
    driver.execute_script("window.scrollTo(5000, 0);")

    driver.refresh()

    time.sleep(3)

    # Create subfolder if it doesn't exist
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Capture screenshot in the subfolder
    file_path = os.path.join(folder, file)
    driver.save_screenshot(file_path)

# Function to capture screenshots at intervals
def capture_screenshots(driver, folder, interval_seconds, duration_minutes):
    start_time = time.time()
    end_time = start_time + (duration_minutes * 60)

    while time.time() < end_time:
        timestamp = time.strftime("%Y%m%d%H%M%S")
        file_name = f"screenshot_{timestamp}.png"
        fullpage_screenshot(driver, folder, file_name)
        print(f"Screenshot captured: {file_name}")

        time.sleep(interval_seconds)

# Chrome options
options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_argument("--headless")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

chrome_driver_path = 'chromedriver_linux64/chromedriver'

service = Service(chrome_driver_path)

# Initialize WebDriver
driver = webdriver.Chrome(options=options, service=service)

# Apply stealth settings
stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True)

# URL to capture
url = "https://test.kokaneducation.com/a-comprehensive-guide-to-web-scraping-with-selenium-and-scrapy/"
web_name = "Kokan"

# Create subfolder dynamically with website name and current date and time
current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
folder_name = f"{web_name} - {current_datetime}"

# Full path to the subfolder
full_folder_path = os.path.join("screenshots", folder_name)

# Open the URL
driver.get(url)

# Capture screenshots every 10 seconds for 1 minute (default)
capture_screenshots(driver, full_folder_path, interval_seconds=10, duration_minutes=1)

# Quit the WebDriver
driver.quit()