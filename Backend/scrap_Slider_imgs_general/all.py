import re
import requests
import os
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def close_popup(driver):
    try:
        close_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.close")))
        close_button.click()
        print("Pop-up closed.")
    except (NoSuchElementException, TimeoutException):
        print("No pop-up found or unable to close.")

def get_slider_images(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("window-size=1920x1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36")

    service = Service('/usr/local/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get(url)
    time.sleep(5)

    close_popup(driver)

    image_urls = set()

    if 'daraz.pk' in url:
        slider_keywords = ['slider', 'carousel', 'slideshow', 'gallery', 'magicslider']
        exclude_substring = '/tps/'
        slider_regex = re.compile('|'.join(slider_keywords), re.IGNORECASE)

        images = driver.find_elements(By.TAG_NAME, 'img')
        for img in images:
            src = img.get_attribute('src')
            if src and src.startswith('http') and exclude_substring not in src:
                ancestors = driver.execute_script(
                    "return (function(el) { var ancestors = []; while (el.parentElement) { ancestors.push(el.parentElement); el = el.parentElement; } return ancestors; })(arguments[0])", 
                    img
                )
                for ancestor in ancestors:
                    class_name = ancestor.get_attribute('class')
                    if class_name and slider_regex.search(class_name):
                        image_urls.add(src)
                        break

    elif 'naheed.pk' in url:
        images = driver.find_elements(By.TAG_NAME, 'img')
        for img in images:
            src = img.get_attribute('src')
            if src and "/magicslider" in src:
                image_urls.add(src)

    elif 'foodpanda.pk' in url:
        images = driver.find_elements(By.XPATH, "//img[contains(@class, 'groceries-image') and contains(@data-testid, 'campaign-banners-swiper')]")
        for img in images:
            src = img.get_attribute('src')
            if src and src.startswith('http'):
                image_urls.add(src)

    else:
        images = driver.find_elements(By.TAG_NAME, 'img')
        for img in images:
            src = img.get_attribute('src')
            if src and src.startswith('http'):
                image_urls.add(src)

    driver.quit()
    return list(image_urls)

def download_images_from_file(file_name, base_folder_name, sub_folder_name):
    main_folder_path = os.path.join(base_folder_name, sub_folder_name)
    if not os.path.exists(main_folder_path):
        os.makedirs(main_folder_path)

    with open(file_name, 'r') as file:
        for url in file:
            try:
                response = requests.get(url.strip())
                if response.status_code == 200:
                    image_name = url.split('/')[-1].strip()
                    file_path = os.path.join(main_folder_path, image_name)
                    with open(file_path, 'wb') as img_file:
                        img_file.write(response.content)
            except Exception as e:
                print(f"Error downloading {url}: {e}")

def get_folder_name_from_url(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    if domain.startswith('www.'):
        domain = domain[4:]
    folder_name = domain.split('.')[0].capitalize()
    return folder_name

# Main execution
url = 'https://www.daraz.pk/'  # Replace with the actual URL
slider_images = get_slider_images(url)

# Determine the folder name based on the URL
sub_folder_name = get_folder_name_from_url(url)

# Base folder for all images
base_folder_name = 'Images'

# Save URLs to file
output_filename = f'slider_images_{sub_folder_name.lower()}.txt'
with open(output_filename, 'w') as file:
    for image_url in slider_images:
        file.write(image_url + '\n')

# Download images to the specified sub-folder inside the base folder
download_images_from_file(output_filename, base_folder_name, sub_folder_name)
