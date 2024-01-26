import os
import time
import requests
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from datetime import datetime

def scroll_full_page(driver):
    scroll_height = driver.execute_script(
        "return Math.max(document.body.scrollHeight, document.body.offsetHeight, "
        "document.documentElement.clientHeight, document.documentElement.scrollHeight, "
        "document.documentElement.offsetHeight);"
    )

    scroll_step = 500
    current_scroll = 0
    while current_scroll < scroll_height:
        driver.execute_script(f"window.scrollTo(0, {current_scroll});")
        time.sleep(0.5)
        current_scroll += scroll_step

def extract_img_urls_by_class(driver, class_name):
    img_urls = []
    elements = driver.find_elements(By.CLASS_NAME, class_name)
    for element in elements:
        img_url = element.get_attribute('src')
        if img_url and img_url.lower().endswith('.jpg'):
            img_urls.append(img_url)
    return img_urls

def extract_iframe_img_urls(driver, content):
    matches = re.findall(r'<iframe id="([^"]+)"', content)
    url_content = []

    for match in matches:
        iframe_element = driver.find_element(By.ID, match)
        driver.switch_to.frame(iframe_element)
        inner_html_content = driver.page_source
        img_urls = re.findall(r'<img src="([^"]+)"', inner_html_content)
        url_content.extend(img_urls)
        driver.switch_to.default_content()

    return url_content

def download_image(image_url, folder_path):
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        image_name = image_url.split('/')[-1]
        file_path = os.path.join(folder_path, image_name)
        with open(file_path, 'wb') as file:
            file.write(response.content)
    except Exception as e:
        print(f"Error downloading {image_url}: {e}")

def perform_cross_screen_image_compatibility_test(urls, screen_size):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Enable headless mode

    if screen_size == 'desktop':
        chrome_options.add_argument("--window-size=1920,1080")
    elif screen_size == 'tablet':
        chrome_options.add_argument("--window-size=768,1024")
    elif screen_size == 'mobile':
        chrome_options.add_argument("--window-size=375,667")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # Generate timestamp

    main_images_dir = 'images'
    if not os.path.exists(main_images_dir):
        os.makedirs(main_images_dir)

    for url in urls:
        driver = webdriver.Chrome(options=chrome_options)

        try:
            driver.get(url)
            driver.implicitly_wait(10)
            scroll_full_page(driver)

            dynamic_content = driver.page_source
            iframe_urls = extract_iframe_img_urls(driver, dynamic_content)

            img_urls = extract_img_urls_by_class(driver, "img-responsive")
            img_urls.extend(iframe_urls)  # Combine image URLs from main content and iframes

            website_name = url.split('//')[-1].split('/')[0].replace('.', '_')
            subfolder_path = os.path.join(main_images_dir, website_name, screen_size, timestamp)
            if not os.path.exists(subfolder_path):
                os.makedirs(subfolder_path)

            urls_filename = os.path.join(subfolder_path, 'url.txt')
            with open(urls_filename, 'w', encoding='utf-8') as file:
                for img_url in img_urls:
                    if img_url.startswith(('http', 'https')):
                        file.write(img_url + '\n')
                        download_image(img_url, subfolder_path)

        finally:
            driver.quit()

# User input part
user_provided_urls = input("Enter the URLs (comma-separated): ").split(',')
print("Choose screen size:\n1. Desktop\n2. Tablet\n3. Mobile")
choice = input("Enter your choice (1/2/3): ")

screen_size = 'desktop'  # Default value
if choice == '1':
    screen_size = 'desktop'
elif choice == '2':
    screen_size = 'tablet'
elif choice == '3':
    screen_size = 'mobile'

perform_cross_screen_image_compatibility_test(user_provided_urls, screen_size)
