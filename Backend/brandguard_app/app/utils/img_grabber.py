from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from selenium_stealth import stealth
import os
from datetime import datetime
from webdriver_manager.chrome import ChromeDriverManager
from app.models.models import Websites

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

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument("--headless")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    # Use ChromeDriverManager().install() to get the path
    chromedriver_path = ChromeDriverManager().install()
    # Use the obtained path directly with webdriver.Chrome()

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)


    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True)

    return driver

def get_website_urls():
    websites = Websites.query.all()
    urls = [website.WebsiteURL for website in websites]
    return urls

def run_img_grabber(url):
    driver = setup_driver()

    web_name = "OLX"

    current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
    folder_name = f"{web_name} - {current_datetime}"
    full_folder_path = os.path.join("screenshots", folder_name)

    driver.get(url)
    capture_screenshots(driver, full_folder_path, interval_seconds=10, duration_minutes=1)
    driver.quit()
