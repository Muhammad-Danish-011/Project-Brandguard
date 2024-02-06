import logging
import os
import time
import traceback
from datetime import datetime
from urllib.parse import urlparse
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from app.extensions import scheduler
from app.models.models import *
from app.utils.find_position import *
from app.utils.img_scraper import *
from flask import jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium_stealth import stealth
from webdriver_manager.chrome import ChromeDriverManager

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
    
    current_url = driver.current_url
    if current_url == 'https://www.naheed.pk/':
        # Wait for 10 seconds before starting to scroll
        # time.sleep(30)
    
       
        # Scroll to the bottom of the page to load all content
        js_scroll_to_bottom = "window.scrollTo(0, document.body.scrollHeight);"
        driver.execute_script(js_scroll_to_bottom)
        time.sleep(10)  # Wait for lazy-loading content to load (adjust as needed)

        # Calculate the total scroll height of the page
        js_get_scroll_height = (
            "return Math.max(document.body.scrollHeight, document.body.offsetHeight, "
            "document.documentElement.clientHeight, document.documentElement.scrollHeight, "
            "document.documentElement.offsetHeight);"
        )
        scroll_height = driver.execute_script(js_get_scroll_height)
        print(scroll_height)

        # Set window size to capture the entire page
        driver.set_window_size(1920, scroll_height)

        # Wait for an element with a specific XPath to become clickable
        try:
            WebDriverWait(driver, 50).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='maincontent']/div[2]/div/div[2]/div[9]/div[7]"))
            )

            # Scroll back to the top of the page
            driver.execute_script("window.scrollTo(0, 0)")
            time.sleep(2)  # Optional: Wait for any animations to finish

             # Create subfolder if it doesn't exist
            if not os.path.exists(folder):
                os.makedirs(folder)
            
            # Capture screenshot in the subfolder
            file_path = os.path.join(folder, file)
            driver.save_screenshot(file_path)
            
            print(f"Screenshot saved to {file_path}")

        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            driver.quit()
    elif current_url == 'https://cozmetica.pk/':
        js_get_scroll_height = (
            "return Math.max(document.body.scrollHeight, document.body.offsetHeight, "
            "document.documentElement.clientHeight, document.documentElement.scrollHeight, "
            "document.documentElement.offsetHeight);"
        )
        scroll_height = driver.execute_script(js_get_scroll_height)
        print(scroll_height)

        # Set window size to capture the entire page
        driver.set_window_size(920, scroll_height)

        # Wait for an element with a specific XPath to become clickable
   
        try:

            # Scroll down in smaller steps to capture the entire page
            scroll_step = 800 # Adjust the step size as needed
            current_scroll = 0
            
            while current_scroll < scroll_height:
                logging.info(current_scroll)
                actions = ActionChains(driver)
                actions.send_keys(Keys.PAGE_DOWN)
                actions.perform()
                current_scroll += scroll_step
                time.sleep(10)  # Adjust the sleep time as needed
            
           
            WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='shopify-section-sections--16399863414945__footer-1']/footer/div/div/div/div[3]/div/h2"))
                 
            )
            
             # # Scroll back to the top of the page
            driver.execute_script("window.scrollTo(0,0)")
            time.sleep(5)  # Optional: Wait for any animations to finish

             # Create subfolder if it doesn't exist
            if not os.path.exists(folder):
                os.makedirs(folder)
            
            # Capture screenshot in the subfolder
            file_path = os.path.join(folder, file)
            driver.save_screenshot(file_path)
            
            print(f"Screenshot saved to {file_path}")

        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            driver.quit()

    else:
        js = (
            "return Math.max(document.body.scrollHeight, document.body.offsetHeight, "
            "document.documentElement.clientHeight, document.documentElement.scrollHeight, "
            "document.documentElement.offsetHeight);"
        )
        scroll_height = driver.execute_script(js)
        # print(scroll_height)
        time.sleep(10)

        # Scroll through the page to trigger lazy loading
        for y in range(0, scroll_height, 100):
            driver.execute_script(f"window.scrollTo(0, {y});")
            time.sleep(2)

        # Set window size to capture the entire page
        driver.set_window_size(1920, scroll_height)

        # Scroll the page using the scroll_full_page function
        # scroll_full_page(driver)
        driver.execute_script("window.scrollTo(5000, 0);")

        # driver.refresh()

        time.sleep(80)

        # Create subfolder if it doesn't exist
        if not os.path.exists(folder):
            os.makedirs(folder)

        # Capture screenshot in the subfolder
        file_path = os.path.join(folder, file)
        driver.save_screenshot(file_path)
        driver.quit()

    

	    
	    
        

# Function to capture screenshots at intervals


def capture_screenshots(driver, folder):
    timestamp = time.strftime("%Y%m%d%H%M%S")
    file_name = f"screenshot_{timestamp}.png"
    fullpage_screenshot(driver, folder, file_name)
    logging.info(f"Capturing screenshots for CampaignID ")
    return file_name


def get_interval_time(campaignID):
    try:
        campaign = Campaigns.query.filter_by(CampaignID=campaignID).first()
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
            website_url = Websites.query.filter_by(
                CampaignID=campaign_id).first()
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


def capture_screenshot_by_campaignid(campaignID):
    # try:
    from app.factory import create_app

    with create_app().app_context():
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_argument("--headless")
        options.add_experimental_option(
            "excludeSwitches", ["enable-automation"])
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

        campaign = Campaigns.query.filter_by(CampaignID=campaignID).first()
        print(campaign)

        if campaign:
            website_url = Websites.query.filter_by(
                CampaignID=campaignID).first()
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

        base_dir = os.path.dirname(os.path.abspath(__file__))
        screenshots_dir = os.path.join(base_dir, "screenshots", folder_name)

        # Open the URL
        driver.get(website_url)
        # Capture screenshots at the specified interval for the given duration
        c_sc = capture_screenshots(driver, screenshots_dir)

        screenshot_path = os.path.join(screenshots_dir, c_sc)

        # Quit the WebDriver
        driver.quit()
        # Create a new Screenshots object and save it to the database
        screenshot = Screenshots(
            CampaignID=campaignID,
            WebsiteID=website_id,
            Extension='png',
            Timestamp=current_datetime,
            FilePath=screenshot_path
        )

        db.session.add(screenshot)
        db.session.commit()
        logging.info("Screenshots captured successfully")

        position_result = image_position(campaignID)
        logging.info(f"Image Position Result {position_result}")
        return {"status": "Screenshots captured successfully"}


def image_position(campaignID):
    screenshots_path = get_screenshot_path(campaignID)
    print(screenshots_path)
    refrence_image = get_refrence_image(campaignID)
    print(refrence_image)
    if screenshots_path and refrence_image:
        position_result = find_image_position(
            screenshots_path, refrence_image, campaignID)
        return position_result


def schedule_screenshot_capture(campaignID, Interval_time):
    # Interval_time = get_interval_time(campaignID)
    print(f'Campaign ID is {campaignID} and its interval is {Interval_time}')
    scheduler.add_job(capture_screenshot_by_campaignid,
                      'interval', minutes=Interval_time, args=[campaignID])
    scheduler.add_job(image_scraping, 'interval',
                      minutes=Interval_time, args=[campaignID])

    return "Screenshots will be captured as scheduled"


def schedule_active_campaigns(app):
    with app.app_context():
        active_campaigns = Campaigns.query.filter_by(Status='active').all()
        for campaign in active_campaigns:
            schedule_screenshot_capture(
                campaign.CampaignID, campaign.IntervalTime)
