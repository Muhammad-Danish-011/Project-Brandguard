from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
from selenium_stealth import stealth
from PIL import Image
from io import BytesIO
from selenium.common.exceptions import TimeoutException
import os

web_screenshot_list = []
def fullpage_screenshot(driver, file, timeout=63, scroll_pause_time=13):
    """Capture a full-page screenshot using JavaScript"""
    start_time = time.time()

    js = (
        "return Math.max( document.body.scrollHeight, document.body.offsetHeight, "
        "document.documentElement.clientHeight, document.documentElement.scrollHeight, "
        "document.documentElement.offsetHeight);"
    )

    scroll_height = driver.execute_script(js)
    driver.set_window_size(driver.get_window_size()['width'], scroll_height)

    screenshot_parts = []
    last_height = 0

    while time.time() - start_time < timeout:
        last_height = scroll_height
        driver.execute_script(f"window.scrollTo(0, {last_height});")
        time.sleep(scroll_pause_time)
        scroll_height = driver.execute_script(js)

        if scroll_height == last_height:
            break

    if time.time() - start_time >= timeout:
        raise TimeoutException("Timeout while capturing full-page screenshot.")

    y_offset = 0
    for _ in range(scroll_height // driver.get_window_size()['height']):
        driver.execute_script(f"window.scrollTo(0, {y_offset});")
        time.sleep(scroll_pause_time)
        screenshot = driver.get_screenshot_as_png()
        screenshot_parts.append(Image.open(BytesIO(screenshot)))
        y_offset += driver.get_window_size()['height']

    full_page_image = Image.new('RGB', (driver.get_window_size()['width'], scroll_height))
    y_offset = 0
   
    for part in screenshot_parts:
        web_screenshot_list.append(part)
        full_page_image.paste(part, (0, y_offset))
        y_offset += part.size[1]

    full_page_image.save(file)
    file_path = os.path.join('screenshots', file_name)

"/home/muhammadmoizkhan/selenium_webdriver"
options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_argument("--headless")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

chrome_driver_path = '/home/muhammadmoizkhan/selenium_webdriver/chromedriver'
service = Service(chrome_driver_path)

# Initialize WebDriver
# driver = webdriver.Chrome(options=options, service=service)

driver = webdriver.Chrome(options=options, service=service)
# # URL to capture
url = "https://www.daraz.com.pk/#"

# # Open the URL
driver.get(url)

# # Set the start time
start_time = time.time()
# # Capture screenshots every 10 seconds for 60 seconds
interval = 10
duration = 60
file_names = []
while time.time() - start_time <= duration:
    # Calculate the start time for capturing the screenshot
    capture_start_time = time.time()
    # Set the desired window width (modify as needed)
    desired_width = 1920
    driver.set_window_size(desired_width, driver.get_window_size()['height'])
    
    # Capture full-page screenshot
    # fullpage_screenshot(driver, f"full_page_screenshot_{(time.time())}.png")
        
    # Generate the file name with a timestamp
    file_name = f"full_page_screenshot_{int(time.time())}.png"
    #this is the way to store the file in folder
    file_path = os.path.join('screenshots', file_name)
    # Capture full-page screenshot
    
    fullpage_screenshot(driver, file_path)
    
    # Append the file name to the list
    file_names.append(file_name)
    
    
    # Calculate time taken for capturing the screenshot
    capture_duration = time.time() - capture_start_time
    
    # Calculate the time to sleep to maintain 10-second intervals
    time_to_sleep = max(0, interval - capture_duration)
    
    # Wait for the next interval
    time.sleep(time_to_sleep)
print(file_names)
print(web_screenshot_list)
# while time.time() - start_time <= duration:
# #     # Capture full-page screenshot
#     fullpage_screenshot(driver, f"full_page_screenshot_{int(time.time())}.png")
    
# #     # Wait for the next interval
#     time.sleep(interval)
# def fullpage_screenshot(driver, file):
#     """Capture a full-page screenshot using JavaScript"""
#     js = (
#         "return Math.max( document.body.scrollHeight, document.body.offsetHeight, "
#         "document.documentElement.clientHeight, document.documentElement.scrollHeight, "
#         "document.documentElement.offsetHeight);"
#     )
#     scroll_height = driver.execute_script(js)

#     # Set window size to capture the entire page
#     driver.set_window_size(driver.get_window_size()['width'], scroll_height)

#     # Capture screenshot
#     driver.save_screenshot(file)

# # Start time
# start_time = time.time()

# # Chrome options
# options = webdriver.ChromeOptions()
# options.add_argument("start-maximized")
# options.add_argument("--headless")
# options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_experimental_option('useAutomationExtension', False)

# chrome_driver_path = '/home/muhammadmoizkhan/selenium_webdriver/chromedriver'

# service = Service(chrome_driver_path)

# # Initialize WebDriver
# driver = webdriver.Chrome(options=options, service=service)

# # Apply stealth settings
# stealth(driver,
#         languages=["en-US", "en"],
#         vendor="Google Inc.",
#         platform="Win32",
#         webgl_vendor="Intel Inc.",
#         renderer="Intel Iris OpenGL Engine",
#         fix_hairline=True)

# # URL to capture
# url = "https://www.daraz.pk/#"

# # Open the URL
# driver.get(url)
# interval = 10
# duration = 60

# while time.time() - start_time <= duration:
#     # Capture full-page screenshot
#     fullpage_screenshot(driver, f"full_page_screenshot_{int(time.time())}.png")
    
#     # Wait for the next interval
#     time.sleep(interval)

# # Capture full-page screenshot
# fullpage_screenshot(driver, "full_page_screenshot.png")

# # Calculate elapsed time
# elapsed = "%s seconds" % (time.time() - start_time)

# # Print elapsed time
# print("Done in " + elapsed)

# # Quit the WebDriver
# driver.quit()


# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium_stealth import stealth
# import time

# def fullpage_screenshot(driver, file):
#     """Capture a full-page screenshot using JavaScript"""
#     js = (
#         "return Math.max( document.body.scrollHeight, document.body.offsetHeight, "
#         "document.documentElement.clientHeight, document.documentElement.scrollHeight, "
#         "document.documentElement.offsetHeight);"
#     )
#     scroll_height = driver.execute_script(js)

#     # Set window size to capture the entire page
#     driver.set_window_size(driver.get_window_size()['width'], scroll_height)

#     # Capture screenshot
#     driver.save_screenshot(file)
#     print(f"full_page_screenshot_{int(time.time())}.png")

# # Chrome options
# options = webdriver.ChromeOptions()
# options.add_argument("start-maximized")
# options.add_argument("--headless")
# options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_experimental_option('useAutomationExtension', False)

# chrome_driver_path = '/home/muhammadmoizkhan/selenium_webdriver/chromedriver'

# service = Service(chrome_driver_path)

# # Initialize WebDriver
# driver = webdriver.Chrome(options=options, service=service)

# # Apply stealth settings
# stealth(driver,
#         languages=["en-US", "en"],
#         vendor="Google Inc.",
#         platform="Win32",
#         webgl_vendor="Intel Inc.",
#         renderer="Intel Iris OpenGL Engine",
#         fix_hairline=True)

# # URL to capture
# url = "https://www.daraz.pk/#"

# # Open the URL
# driver.get(url)

# # Set the start time
# start_time = time.time()

# # Capture screenshots every 10 seconds for 60 seconds
# interval = 10
# duration = 60

# while time.time() - start_time <= duration:
#     # Capture full-page screenshot
#     fullpage_screenshot(driver, f"full_page_screenshot_{int(time.time())}.png")
    
#     # Wait for the next interval
#     time.sleep(interval)

# # Quit the WebDriver
# driver.quit()

