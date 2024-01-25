from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from selenium_stealth import stealth
import os
from datetime import datetime
from app.models.models import *
from webdriver_manager.chrome import ChromeDriverManager
from flask import jsonify
import traceback 
from app.extensions import scheduler
import atexit
import logging


# Configure logging (usually done in your Flask app initialization)
logging.basicConfig(
    level=logging.INFO,  # Set the logging level (e.g., INFO, DEBUG)
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('app.log'),  # Log to a file
        logging.StreamHandler()  # Log to the console
    ]
)

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
        logging.info(f"Capturing screenshots for CampaignID ")
        # print(f"Screenshot captured: {file_name}")

        time.sleep(interval_seconds)

# Chrome options
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument("--headless")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

# chrome_driver_path = ChromeDriverManager().install()
    chrome_driver_path=ChromeDriverManager().install()
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

def get_interval_time(compainID):
    try:
        campaign = Campaigns.query.filter_by(CampaignID=compainID).first()
        if campaign:
            return {"IntervalTime": campaign.IntervalTime}
        else:
            return {"error": "Campaign not found"}, 404
    except Exception as e:
        traceback.print_exc()  # Log the exception traceback
        return {"error": str(e)}, 500
    



def get_website(campaign_id):
    try:
        campaign = Campaigns.query.filter_by(CampaignID=campaign_id).first()
        print(campaign)
        if campaign:
            website_url = Websites.query.filter_by(CampaignID=campaign_id).first()
            if website_url:
                response_data = {"website": website_url.WebsiteURL}
                return (response_data)
            else:
                return ({"error": "Website URL not found"}), 404
        else:
            return jsonify({"error": "Campaign not found"}), 404
    except Exception as e:
        traceback.print_exc()  # Log the exception traceback
        return jsonify({"error": str(e)}), 500
def generate_screenshot_path(website_url, campaign_id, timestamp, extension):
    return f"{str(campaign_id).zfill(3)}_{str(timestamp).zfill(3)}_{timestamp}.{extension}"

def capture_screenshot_by_compainid(CompainID):
    try:
        
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_argument("--headless")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        chrome_driver_path = ChromeDriverManager().install()
        # chrome_driver_path='./chromedriver'
        service = Service(chrome_driver_path)

        # Initialize WebDriver
        driver = webdriver.Chrome(options=options, service=service)

        # Initialize the driver here or earlier in your code
       
        campaign = Campaigns.query.filter_by(CampaignID=CompainID).first()
        print(campaign)

        if campaign:
            website_url = Websites.query.filter_by(CampaignID=CompainID).first()
            if website_url:
                website_id = website_url.WebsiteID
                website_url = website_url.WebsiteURL
                interval_time = campaign.IntervalTime
            else:
                driver.quit()  # Quit the driver before returning an error response
                return {"error": "Website URL not found for this campaign"}, 404
        else:
            driver.quit()  # Quit the driver before returning an error response
            return {"error": "Campaign not found"}, 404

        # Create a subfolder for each capture
        current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
        folder_name = f"{website_url.replace('https://', '').replace('/', '-')} - {current_datetime}"
        full_folder_path = os.path.join("screenshots", folder_name)

        # Open the URL
        driver.get(website_url)

        # Capture screenshots at the specified interval for the given duration
        capture_screenshots(driver, full_folder_path, interval_seconds=interval_time, duration_minutes=1)
        screenshot_path = generate_screenshot_path(website_url, CompainID, current_datetime, 'png')

        # Quit the WebDriver
        driver.quit()
          # Create a new Screenshots object and save it to the database
        screenshot = Screenshots(
            CampaignID=CompainID,
            WebsiteID=website_id,  # Replace with the actual WebsiteID
            Extension='png',  # Replace with the actual extension
            Timestamp=current_datetime,
            FilePath=screenshot_path
        )

        db.session.add(screenshot)
        db.session.commit()
        logging.info("Screenshots captured successfully")
        return {"status": "Screenshots captured successfully"}

        
    except Exception as e:
        return {"error": str(e)}


def schedule_screenshot_capture(CompainID):
    scheduler.add_job(capture_screenshot_by_compainid, 'interval', minutes=3, args=[CompainID])
    return "Screenshots will be captured as scheduled"
