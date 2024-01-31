import os
import time
import requests
import re
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

        os.makedirs(folder_path, exist_ok=True)

        file_path = os.path.join(folder_path, image_name)
        with open(file_path, 'wb') as file:
            file.write(response.content)
    except Exception as e:
        print(f"Error downloading {image_url}: {e}")

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

def scrape_images_from_url(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36")
    driver = webdriver.Chrome(options=chrome_options)
    try:
        driver.get(url)
        driver.implicitly_wait(10)
        scroll_full_page(driver)
        page_source = driver.page_source
        all_image_urls = extract_img_urls_by_class(driver, "img-responsive")
        all_image_urls.extend(extract_iframe_img_urls(driver, page_source))
        return all_image_urls
    finally:
        driver.quit()

def get_folder_name_from_url(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    if domain.startswith('www.'):
        domain = domain[4:]
    folder_name = domain.split('.')[0].capitalize()
    return folder_name

def main():
    url = input("Enter the URL for image extraction: ")
    slider_images = get_slider_images(url)
    print(f"Found {len(slider_images)} slider images.")
    additional_images = scrape_images_from_url(url)
    print(f"Found {len(additional_images)} additional images.")
    all_images = list(set(slider_images + additional_images))
    print(f"Total unique images found: {len(all_images)}")
    sub_folder_name = get_folder_name_from_url(url)
    base_folder_name = 'Images'
    if not os.path.exists(base_folder_name):
        os.makedirs(base_folder_name)
    for image_url in all_images:
        download_image(image_url, os.path.join(base_folder_name, sub_folder_name))

if __name__ == "__main__":
    main()
