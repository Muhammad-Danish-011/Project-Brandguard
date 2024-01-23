from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from selenium_stealth import stealth
import os
from datetime import datetime
from app.models.models import *
from webdriver_manager.chrome import ChromeDriverManager
from flask import jsonify

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

# chrome_driver_path = ChromeDriverManager().install()
    # chrome_driver_path='./chromedriver_linux64/chromedriver'
    # service = Service(chrome_driver_path)

    # Initialize WebDriver
    driver = webdriver.Chrome(ChromeDriverManager().install())

    # Apply stealth settings
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True)
    driver.get(url)
    # URL to capture
url = "https://test.kokaneducation.com/a-comprehensive-guide-to-web-scraping-with-selenium-and-scrapy/"
web_name = "Kokan"

# Create subfolder dynamically with website name and current date and time
current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
folder_name = f"{web_name} - {current_datetime}"

# Full path to the subfolder
full_folder_path = os.path.join("screenshots", folder_name)

# Open the URL
# driver.get(url)

# # Capture screenshots every 10 seconds for 1 minute (default)
# capture_screenshots(driver, full_folder_path, interval_seconds=10, duration_minutes=1)

# # Quit the WebDriver
# driver.quit()

# # Replace this with your data retrieval logic
# # @bp.route('/campaigns/<compainid>', methods=['GET'])
# def get_campaign_details(compainid):
#     campaign = Campaigns.query.filter_by(id=compainid).first()
#     if campaign:
#         websites = Websites.query.filter_by(CampaignID=campaign.id).all()
#         website_urls = [website.WebsiteURL for website in websites]
#         return jsonify(IntervalTime=campaign.IntervalTime,WebsiteURLs=website_urls)
#         # return jsonify(CampaignName=campaign.CampaignName, StartDate=campaign.StartDate.strftime('%Y-%m-%d %H:%M:%S'),
#         #                EndDate=campaign.EndDate.strftime('%Y-%m-%d %H:%M:%S'), IntervalTime=campaign.IntervalTime,
#         #                Status=campaign.Status, WebsiteURLs=website_urls)
#     else:
#         return jsonify(message='Campaign not found'), 404

def get_interval_time(compainID):
    campaign = Campaigns.query.filter_by(id=compainID).first()
    print(campaign)
    if campaign is not None:
        IntervalTime = campaign.IntervalTime
        return IntervalTime


def capture_screenshot_by_compainid(compainID):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_argument("--headless")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

    # chrome_driver_path = ChromeDriverManager().install()
        # chrome_driver_path='/home/muhammadmoizkhan/selenium_webdriver/chromedriver'
        # service = Service(chrome_driver_path)

        # Initialize WebDriver
        driver = webdriver.Chrome(ChromeDriverManager().install())

        # Initialize the driver here or earlier in your code

        campaign = Campaigns.query.filter_by(id=compainID).first()

        if campaign:
            website_url = Websites.query.filter_by(CampaignID=campaign.id).first()
            if website_url:
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

        # Quit the WebDriver
        driver.quit()

        return {"status": "Screenshots captured successfully"}
    except Exception as e:
        return {"error": str(e)}
