import os
import re
import time
from datetime import datetime
from urllib.parse import urlparse

import cv2
import requests
from app.models.models import *
from app.utils.find_position import *
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium_stealth import stealth
from webdriver_manager.chrome import ChromeDriverManager


def get_root_domain(url):
    # Extract the main part of the URL (domain) using urlparse
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    current_datetime = datetime.now().strftime("%Y-%m-%d---%H-%M-%S")
    folder_name = f"{url.replace('https://', '').replace('/', '')}---{current_datetime}"
    return folder_name


def get_script_directory():
    # Get the directory of the current script
    return os.path.dirname(os.path.abspath(__file__))


def get_image_files(folder_name):
    # Get the path to the 'utils' directory
    script_directory = get_script_directory()

    # Construct the path to the 'download_images' folder inside the 'utils' directory
    download_images_path = os.path.join(script_directory, folder_name)

    # Check if the directory exists before listing files
    if not os.path.exists(download_images_path):
        print(f"Directory does not exist: {download_images_path}")
        return []

    # List image files in the directory
    image_files = [f for f in os.listdir(download_images_path) if f.lower(
    ).endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    return [os.path.join(download_images_path, f) for f in image_files]


def calculate_similarity_percentage(main_image, other_image):

    # Check if either main_image or other_image is None
    if main_image is None or other_image is None:
        # print("Error: One of the images is None.")
        return 0.0  # Return 0 similarity in case of an error

    # Feature-based matching using ORB
    orb = cv2.ORB_create()
    keypoints1, descriptors1 = orb.detectAndCompute(main_image, None)
    keypoints2, descriptors2 = orb.detectAndCompute(other_image, None)

    # Check if descriptors1 or descriptors2 is None
    if descriptors1 is None or descriptors2 is None:
        print("Error: One of the image descriptors is None.")
        return 0.0  # Return 0 similarity in case of an error

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(descriptors1, descriptors2)

    # Calculate similarity percentage based on the number of matches
    similarity_percentage = len(
        matches) / max(len(keypoints1), len(keypoints2)) * 100

    return similarity_percentage


def get_slider_images(url):

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

    # Navigate to the URL
    driver.get(url)
    time.sleep(5)  # Adjust the sleep time if necessary
    close_popup(driver)
    image_urls = set()

    if 'daraz.pk' in url:
        # Daraz specific logic
        slider_keywords = ['slider', 'carousel',
                           'slideshow', 'gallery', 'magicslider']
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
        # Naheed specific logic
        images = driver.find_elements(By.TAG_NAME, 'img')

        for img in images:
            src = img.get_attribute('src')
            if src and "/magicslider" in src:
                image_urls.add(src)

    elif 'cozmetica.pk' in url:
        images = driver.find_elements(By.TAG_NAME, 'img')
        for img in images:
            src = img.get_attribute('src')
            if src and src.startswith('http') and 'shopify' in src:
                # print(src)
                image_urls.add(src)

    elif 'foodpanda.pk' in url:
        images = driver.find_elements(
            By.XPATH, "//img[contains(@class, 'groceries-image') and contains(@data-testid, 'campaign-banners-swiper')]")
        for img in images:
            src = img.get_attribute('src')
            if src and src.startswith('http'):
                image_urls.add(src)

    else:
        # General logic for other URLs
        images = driver.find_elements(By.TAG_NAME, 'img')

        for img in images:
            src = img.get_attribute('src')
            if src and src.startswith('http'):
                image_urls.add(src)

    driver.quit()
    return list(image_urls)


def scrape_images_from_url(url):

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


def download_images_from_list(url_list, folder_path):
    for image_url in url_list:
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
        close_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.close")))
        close_button.click()
        print("Pop-up closed.")
    except (NoSuchElementException, TimeoutException):
        print("No pop-up found or unable to close.")


def analyze_images(url, main_image_path, campaignID):
    # Get the root domain from the URL for folder naming
    if "www." not in url:
        # Split the URL at the double slash "//" and insert "www." after it
        parts = url.split("//")
        url = parts[0] + "//www." + parts[1]

    file_name = get_root_domain(url)

    # Get the path to the 'utils' directory
    script_directory = get_script_directory()

    # Construct the path to the 'download_images' folder inside the 'utils' directory
    main_download_folder = os.path.join(script_directory, 'download_images')
    os.makedirs(main_download_folder, exist_ok=True)

    # Create a unique subfolder for each analysis to avoid file name conflicts
    download_folder = os.path.join(
        main_download_folder, f'{file_name}')
    os.makedirs(download_folder, exist_ok=True)

    # print(f'Shahzaib Khan Prints {download_folder}')

    slider_images = get_slider_images(url)

    other_images = scrape_images_from_url(url)

   # List to store image URLs
    image_url_list = []

    for image_url in slider_images:
        image_url_list.append(image_url)

    for image_url in other_images:
        image_url_list.append(image_url)

    cleaned_urls = [url.split('?')[0] for url in image_url_list]

    # print(cleaned_urls)

    download_images_from_list(cleaned_urls, download_folder)

    main_image_path = main_image_path
    main_image = cv2.imread(main_image_path)

    other_images_path = download_folder

    other_images_folder = other_images_path
    other_image_files = get_image_files(other_images_folder)

    similarity_scores = []
    image_names = []

    for other_image_file in other_image_files:
        other_image = cv2.imread(other_image_file)
        total_similarity = calculate_similarity_percentage(
            main_image, other_image)
        similarity_scores.append(total_similarity)
        image_names.append(os.path.basename(other_image_file))

    for i, (ssim_score, image_name) in enumerate(zip(similarity_scores, image_names)):
        match_status = "Match" if ssim_score > 0.8 else "Not Match"

    threshold_score = 80.0
    is_score_above_threshold = any(
        score > threshold_score for score in similarity_scores)
    visibility = 'yes' if is_score_above_threshold else 'no'

    new_Scrape_Image_Status = Scrape_Image_Status(
        CampaignID=campaignID,
        Found_Status=visibility
    )
    db.session.add(new_Scrape_Image_Status)
    db.session.commit()


def image_scraping(campaignID):
    from app.factory import create_app

    with create_app().app_context():

        campaign = Campaigns.query.filter_by(CampaignID=campaignID).first()
        print(campaign)

        if campaign:
            website_url = Websites.query.filter_by(
                CampaignID=campaignID).first()
            if website_url:
                website_url = website_url.WebsiteURL
            else:
                print("No Website URL found.")

        refrence_image = get_refrence_image(campaignID)

        analyze_images(website_url, refrence_image, campaignID)
