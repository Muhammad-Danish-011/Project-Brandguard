from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from selenium_stealth import stealth
import os
from webdriver_manager.chrome import ChromeDriverManager
import threading
from apscheduler.schedulers.background import BackgroundScheduler
import cv2
import numpy as np

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

def print_cronjob_data():
    with app.app_context():
        cronjob_data = Cronjob.query.all()
        intervals = [record.interval for record in cronjob_data]
        return intervals


def update_database_with_ad_info(has_ad):
    ad_record = AdRecord(has_ad=has_ad)
    db.session.add(ad_record)
    db.session.commit()

def check_for_ad(driver):
    try:
        ad_element = driver.find_element_by_class_name('react-swipeable-view-container')
        return ad_element is not None
    except:
        return False

def fullpage_screenshot(driver, folder, file):
    js = (
        "return Math.max( document.body.scrollHeight, document.body.offsetHeight, "
        "document.documentElement.clientHeight, document.documentElement.scrollHeight, "
        "document.documentElement.offsetHeight);"
    )
    scroll_height = driver.execute_script(js)

    driver.set_window_size(1920, scroll_height)
    driver.execute_script("window.scrollTo(5000, 0);")
    driver.refresh()

    time.sleep(3)

    if not os.path.exists(folder):
        os.makedirs(folder)

    file_path = os.path.join(folder, file)
    driver.save_screenshot(file_path)

def find_image_position(screenshot_path, reference_image_path):
        # Read the screenshot and reference image
    screenshot = cv2.imread(screenshot_path)
    reference_image = cv2.imread(reference_image_path)

    # Convert images to grayscale
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    reference_image_gray = cv2.cvtColor(reference_image, cv2.COLOR_BGR2GRAY)

    # Use template matching to find the location of the reference image
    result = cv2.matchTemplate(screenshot_gray, reference_image_gray, cv2.TM_CCOEFF_NORMED)
    _, _, _, max_loc = cv2.minMaxLoc(result)

    # Determine the position of the reference image
    height, width = reference_image_gray.shape
    mid_x, mid_y = max_loc[0] + width // 2, max_loc[1] + height // 2

    # Initialize positions based on relative location
    position_names = {
        'top': False,
        'bottom': False,
        'left': False,
        'right': False,
        'mid': False
    }

    # Update positions based on relative location
    screen_width, screen_height = screenshot.shape[1], screenshot.shape[0]
    position_names['top'] = mid_y < screen_height / 3
    position_names['bottom'] = mid_y > 2 * screen_height / 3
    position_names['left'] = mid_x < screen_width / 3
    position_names['right'] = mid_x > 2 * screen_width / 3
    position_names['mid'] = not any([position_names['top'], position_names['bottom'], position_names['left'], position_names['right']])

    return position_names

# Example usage
screenshot_path = '/home/aqsatauheed/Desktop/T_Duration (copy)/screenshots/OLX - 20240118110112/screenshot_20240118110112.png'
reference_image_path = '/home/aqsatauheed/Desktop/T_Duration (copy)/img_comp/424970966-800x600.jpeg'
# screenshot_path = '/home/shahzaibkhan/work/brandguard/webdriver_mvp_xloop/screenshots/Kokan - 20240116200720/screenshot_20240116200819.png'
# reference_image_path = '/home/shahzaibkhan/work/brandguard/img_comp/ad_banner_template.png'
# reference_image_path = '/home/shahzaibkhan/work/brandguard/img_comp/lwl-ad-300X600.jpg'

position = find_image_position(screenshot_path, reference_image_path)
print("Reference image position:", position)

def capture_screenshots_and_position_image(driver, folder, interval_seconds, duration_minutes):
    start_time = time.time()
    end_time = start_time + (duration_minutes * 60)

    while time.time() < end_time:
        timestamp = time.strftime("%Y%m%d%H%M%S")
        file_name = f"screenshot_{timestamp}.png"
        fullpage_screenshot(driver, folder, file_name)
        print(f"Screenshot captured: {file_name}")

        # Image positioning logic
        screenshot_path = os.path.join(folder, file_name)
        reference_image_path = '/home/aqsatauheed/Desktop/T_Duration (copy)/img_comp/424970966-800x600.jpeg'
        position = find_image_position(screenshot_path, reference_image_path)
        print("Reference image position:", position)

        time.sleep(interval_seconds)

def start_capture():
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument("--headless")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    chrome_driver_path = ChromeDriverManager().install()
    service = Service(chrome_driver_path)

    driver = webdriver.Chrome(options=options, service=service)

    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True)

    url = "https://www.olx.com.pk/"

    web_name = "OLX"
    current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
    folder_name = f"{web_name} - {current_datetime}"
    full_folder_path = os.path.join("screenshots", folder_name)

    driver.get(url)

    # Start a new thread for capturing screenshots and positioning the image
    capture_thread = threading.Thread(
        target=capture_screenshots_and_position_image,
        args=(driver, full_folder_path, 10, 1)
    )
    capture_thread.start()

    capture_thread.join()  # Wait for the thread to finish

    has_ad = check_for_ad(driver)
    update_database_with_ad_info(has_ad)

    driver.quit()

@app.route('/')
def index():
    return 'Welcome to the Ad Capture App'

@app.route('/start_capture', methods=['POST'])
def start_capture_endpoint():
    start_capture()
    return jsonify({'message': 'Ad capture completed.'})

@app.route('/stop_capture', methods=['POST'])
def stop_capture():
    return jsonify({'message': 'Ad capture stopped.'})

def scheduled_job():
    with app.app_context():
        db.create_all()       
        start_capture()


# Setup scheduler
scheduler = BackgroundScheduler()

intervals = print_cronjob_data()
print(intervals)  # Make sure intervals is a list of integers

# Assuming you want the first element of the list as minutes
minutes = intervals[0]

scheduler.add_job(scheduled_job, 'interval', minutes=minutes)  # Set initial interval, it will be updated from the database
scheduler.start()

if __name__ == '__main__':
    app.run(debug=True)
