import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

def get_slider_images(url):
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("window-size=1920x1080")  # Set window size to 1920x1080
    # Adding a desktop user-agent
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36")

    service = Service('/usr/local/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Open the URL
    driver.get(url)
    time.sleep(5)  # Adjust the sleep time if necessary

    # Regex pattern for common slider elements
    slider_regex = re.compile(r"slider|carousel|slideshow|gallery", re.IGNORECASE)

    # Find all elements in the page
    elements = driver.find_elements(By.XPATH, "//*")

    image_urls = set()

    # Check each element for a matching class
    for element in elements:
        class_name = element.get_attribute('class')
        if class_name and slider_regex.search(class_name):
            images = element.find_elements(By.TAG_NAME, 'img')
            for img in images:
                src = img.get_attribute('src')
                if src and src.startswith('http'):  # Ensure it's a valid URL
                    image_urls.add(src)

    driver.quit()
    return list(image_urls)

# Usage
url = 'https://www.naheed.pk/'  # Replace with the actual URL
slider_images = get_slider_images(url)

# Save to file
with open('slider_images.txt', 'w') as file:
    for image_url in slider_images:
        file.write(image_url + '\n')