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
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def get_root_domain(url):
    # Extract the main part of the URL (domain) using urlparse
    parsed_url = urlparse(url)
    domain = parsed_url.netloc

    # Extract specific part (e.g., daraz) based on your requirement
    parts = domain.split('.')
    if len(parts) >= 2:
        return parts[1]  # Return the second-to-last part of the domain
    else:
        return domain


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

# def get_image_files(folder_path):

#     image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
#     return [os.path.join(folder_path, f) for f in image_files]


def calculate_similarity_percentage(main_image, other_image):
    # Feature-based matching using ORB
    orb = cv2.ORB_create()
    keypoints1, descriptors1 = orb.detectAndCompute(main_image, None)
    keypoints2, descriptors2 = orb.detectAndCompute(other_image, None)

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(descriptors1, descriptors2)

    # Calculate similarity percentage based on the number of matches
    similarity_percentage = len(
        matches) / max(len(keypoints1), len(keypoints2)) * 100

    return similarity_percentage


def get_slider_images(url):
    # Create Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    # This line makes Chrome run in headless mode
    chrome_options.add_argument("--headless")

    # Initialize a webdriver (e.g., Chrome)
    # driver = webdriver.Chrome(options=chrome_options)

    chrome_driver_path = ChromeDriverManager().install()
    # chrome_driver_path='./chromedriver'
    service = Service(chrome_driver_path)

    # Initialize WebDriver
    driver = webdriver.Chrome(options=chrome_options, service=service)

    # Navigate to the URL
    driver.get(url)
    time.sleep(5)  # Adjust the sleep time if necessary

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

    else:
        # General logic for other URLs
        images = driver.find_elements(By.TAG_NAME, 'img')

        for img in images:
            src = img.get_attribute('src')
            if src and src.startswith('http'):
                image_urls.add(src)

    driver.quit()
    return list(image_urls)


def download_images_from_list(url_list, output_folder):
    try:
        # Create the output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)

        for url in url_list:
            try:
                response = requests.get(url.strip())

                if response.status_code == 200:
                    # Get the image filename from the URL
                    image_name = os.path.join(
                        output_folder, os.path.basename(url.strip()))

                    # Save the image to the specified folder
                    with open(image_name, 'wb') as img_file:
                        img_file.write(response.content)
                        print(f"Image downloaded: {image_name}")
                else:
                    print(
                        f"Failed to download image from {url.strip()}. Status code: {response.status_code}")

            except Exception as e:
                print(f"Error downloading {url.strip()}: {e}")

    except Exception as e:
        print(f"Error creating folder {output_folder}: {e}")


def analyze_images(url, main_image_path, campaignID):
    # Get the root domain from the URL for folder naming
    file_name = get_root_domain(url)

    # Get the path to the 'utils' directory
    script_directory = get_script_directory()

    # Construct the path to the 'download_images' folder inside the 'utils' directory
    main_download_folder = os.path.join(script_directory, 'download_images')
    os.makedirs(main_download_folder, exist_ok=True)

    # Create a unique subfolder for each analysis to avoid file name conflicts
    download_folder = os.path.join(
        main_download_folder, f'{file_name}_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
    os.makedirs(download_folder, exist_ok=True)

    # print(f'Shahzaib Khan Prints {download_folder}')

    slider_images = get_slider_images(url)

   # List to store image URLs
    image_url_list = []

    for image_url in slider_images:
        image_url_list.append(image_url)

    # Print or use image_url_list as needed
    # print("Image URLs:", image_url_list)

    # main_download_folder = 'download_images'
    # os.makedirs(main_download_folder, exist_ok=True)

    # download_folder = os.path.join(main_download_folder, f'{file_name}_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
    # os.makedirs(download_folder, exist_ok=True)

    # base_dir = os.path.dirname(os.path.abspath(__file__))
    # screenshots_dir = os.path.join(base_dir, download_folder)

    download_images_from_list(image_url_list, download_folder)

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
        # print(f"Similarity Score with Image '{image_name}': {ssim_score:.5f} - {match_status}")

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

    # print(f"Shahzaib Prints Visibility Score: {visibility}")

    # plt.figure(figsize=(10, 5))
    # colors = ['green' if score > 80.0 else 'red' for score in similarity_scores]
    # plt.bar(image_names, similarity_scores, color=colors)
    # plt.xlabel('Other Images')
    # plt.ylabel('Similarity Score')
    # plt.title('Similarity Scores with Match/Not Match Status')
    # plt.xticks(rotation=45, ha='right')

    # for i, (ssim_score, color) in enumerate(zip(similarity_scores, colors)):
    #     plt.text(i, ssim_score, f"{ssim_score:.5f}\n{'Match' if ssim_score > 0.8 else 'Not Match'}",
    #              ha='center', va='bottom', color='black', fontsize=8)

    # plt.show()


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

        # main_image_path = r"/home/shahzaibkhan/work/Project-Brandguard/Backend/brandguard_app/reference_images/50e3cb98-f34a-48b5-99aa-37e4e3dd413b.jpg"

        # url = 'https://www.daraz.pk/'
        analyze_images(website_url, refrence_image, campaignID)
