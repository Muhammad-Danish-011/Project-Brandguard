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

def capture_screenshots(driver, folder, interval_seconds, duration_minutes):
    start_time = time.time()
    end_time = start_time + (duration_minutes * 60)

    while time.time() < end_time:
        timestamp = time.strftime("%Y%m%d%H%M%S")
        file_name = f"screenshot_{timestamp}.png"
        fullpage_screenshot(driver, folder, file_name)
        print(f"Screenshot captured: {file_name}")

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

    capture_screenshots(driver, full_folder_path, interval_seconds=10, duration_minutes=1)

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
