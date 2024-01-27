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
import logging
from app.utils.find_position import *
from urllib.parse import urlparse

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
        "return Math.max(document.body.scrollHeight, document.body.offsetHeight, "
        "document.documentElement.clientHeight, document.documentElement.scrollHeight, "
        "document.documentElement.offsetHeight);"
    )
    scroll_height = driver.execute_script(js)

    # Scroll through the page to trigger lazy loading
    for y in range(0, scroll_height, 200):
        driver.execute_script(f"window.scrollTo(0, {y});")
        time.sleep(1)  # short sleep between scrolls

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
def capture_screenshots(driver, folder):
    timestamp = time.strftime("%Y%m%d%H%M%S")
    file_name = f"screenshot_{timestamp}.png"
    fullpage_screenshot(driver, folder, file_name)
    logging.info(f"Capturing screenshots for CampaignID ")
    return file_name


def get_interval_time(campainID):
    try:
        campaign = Campaigns.query.filter_by(CampaignID=campainID).first()
        if campaign:
            return campaign.IntervalTime
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

# def generate_screenshot_path(path):
#     # Extract domain from the website URL
#     parsed_url = urlparse(website_url)
#     domain = parsed_url.netloc.replace('www.', '')  # Removes 'www.' if present

#     # Format folder and file names
#     folder_name = f"screenshots/{domain} - {timestamp}"
#     file_name = f"screenshot_{timestamp}.{extension}"

#     # Combine to create the full path
#     full_path = path
#     return full_path

def capture_screenshot_by_compainid(campainID):
    # try:
    from app import create_app

    with create_app().app_context():
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
        stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True)

        # Initialize the driver here or earlier in your code

        campaign = Campaigns.query.filter_by(CampaignID=campainID).first()
        print(campaign)

        if campaign:
            website_url = Websites.query.filter_by(CampaignID=campainID).first()
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

        parsed_url = urlparse(website_url)
        domain = parsed_url.netloc.replace('www.', '').replace('.', '_')

        # Create a subfolder for each capture
        current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
        folder_name = f"{website_url.replace('https://', '').replace('/', ' ')} - {current_datetime}"
        full_folder_path = os.path.join("screenshots", folder_name)

        base_dir = os.path.dirname(os.path.abspath(__file__))
        screenshots_dir = os.path.join(base_dir, "screenshots", folder_name)

        # Open the URL
        driver.get(website_url)
        # Capture screenshots at the specified interval for the given duration
        c_sc = capture_screenshots(driver, screenshots_dir)
        # screenshot_path = generate_screenshot_path(c_sc)
        screenshot_path = os.path.join(screenshots_dir, c_sc)

        # Quit the WebDriver
        driver.quit()
            # Create a new Screenshots object and save it to the database
        screenshot = Screenshots(
            CampaignID=campainID,
            WebsiteID=website_id,
            Extension='png',
            Timestamp=current_datetime,
            FilePath=screenshot_path
        )

        db.session.add(screenshot)
        db.session.commit()
        logging.info("Screenshots captured successfully")
        return {"status": "Screenshots captured successfully"}

def image_position(campainID):
    from app import create_app

    with create_app().app_context():
        screenshots_path = get_screenshot_path(campainID)
        print(screenshots_path)
        refrence_image = get_refrence_image(campainID)
        print(refrence_image)
        if screenshots_path and refrence_image:
            position_result = find_image_position(screenshots_path,refrence_image)
            logging.info(f"Image Position Result {position_result}")
            return position_result

def schedule_screenshot_capture(campainID):
    Interval_time = get_interval_time(campainID)
    scheduler.add_job(capture_screenshot_by_compainid, 'interval', minutes=Interval_time, args=[campainID])
    scheduler.add_job(image_position,'interval',minutes = Interval_time,args=[campainID])
    return "Screenshots will be captured as scheduled"
