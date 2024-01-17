
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from selenium_stealth import stealth
import os
from webdriver_manager.chrome import ChromeDriverManager
import schedule

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Aq$a123@localhost:5432/postgres'
db = SQLAlchemy(app)

class AdRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    has_ad = db.Column(db.Boolean, default=False)

class Cronjob(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    interval = db.Column(db.Integer)  

def get_interval_from_db():
    # Assuming you have a model for the cronjob table
    cronjob_record = Cronjob.query.first()  # Assuming you have a model named Cronjob

    if cronjob_record:
        return cronjob_record.interval

def update_database_with_ad_info(has_ad):
    ad_record = AdRecord(has_ad=has_ad)
    db.session.add(ad_record)
    db.session.commit()

def check_for_ad(driver):
    try:
        # Check for the existence of an element with a specific class
        ad_element = driver.find_element_by_class_name('react-swipeable-view-container')
        return ad_element is not None
    except:
        # If the element is not found, consider it as no ad
        return False

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

@app.route('/')
def index():
    return 'Welcome to the Ad Capture App'

@app.route('/start_capture', methods=['POST'])
def start_capture():
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument("--headless")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    # Use ChromeDriverManager to automatically download and manage ChromeDriver
    chrome_driver_path = ChromeDriverManager().install()

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
    url = "https://www.olx.com.pk/"

    # Capture screenshots every 10 seconds for 1 minute (default)
    try:
        # Create subfolder dynamically with website name and current date and time
        web_name = "OLX"
        current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
        folder_name = f"{web_name} - {current_datetime}"

        # Full path to the subfolder
        full_folder_path = os.path.join("screenshots", folder_name)

        # Open the URL
        driver.get(url)

        # Capture screenshots
        capture_screenshots(driver, full_folder_path, interval_seconds=10, duration_minutes=1)

        # Update database with ad information after capturing screenshots
        has_ad = check_for_ad(driver)
        update_database_with_ad_info(has_ad)

        return jsonify({'message': 'Ad capture completed.'})

    finally:
        # Quit the WebDriver in a finally block to ensure it happens even if an exception occurs
        driver.quit()

@app.route('/stop_capture', methods=['POST'])
def stop_capture():
    # Stop the ad capture process
    return jsonify({'message': 'Ad capture stopped.'})

@app.route('/hello', methods=['POST'])
def hello():
    print('Hello')

def job():
    with app.app_context():
        # Create the database tables within the Flask app context
        db.create_all()

    # Retrieve interval from the database
    interval = get_interval_from_db()

    # Trigger the /start_capture endpoint
    with app.test_request_context('/start_capture', method='POST'):
        start_capture()

    # Schedule the job with the retrieved interval
    schedule.every(interval).minutes.do(job)

# Schedule the job to run every hour
# schedule.every().minute.do(job)
        
# schedule.every(3).minutes.do(job)


if __name__ == '__main__':
    # Create the database tables within the Flask app context
    # with app.app_context():
    #     db.create_all()

    # Run the scheduler in a loop
    while True:
        schedule.run_pending()
        time.sleep(1)  # Sleep for 1 second to avoid high CPU usage

    app.run(debug=True)
