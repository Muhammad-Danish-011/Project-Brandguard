import re
import requests
import os
from selenium import webdriver
from urllib.parse import urlparse
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

from tkinter import Tk, filedialog
from PIL import Image
from io import BytesIO
import cv2
from skimage.metrics import structural_similarity as ssim
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime



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

def select_image():
    root = Tk()
    root.withdraw()  # Hide the main window

    file_path = filedialog.askopenfilename(
        title="Select an image file",
        filetypes=[("Image files", ("*.png", "*.jpg", "*.jpeg", "*.gif"))]
    )

    return file_path

def get_image_size(file_path):
    try:
        image = Image.open(file_path)
        width, height = image.size
        return width, height
    except Exception as e:
        print(f"Error: {e}")
        return None

def select_folder():
    root = Tk()
    root.withdraw()  # Hide the main window

    folder_path = filedialog.askdirectory(title="Select a folder containing images")

    return folder_path

def get_image_files(folder_path):
    
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    return [os.path.join(folder_path, f) for f in image_files]

def calculate_similarity_percentage(main_image, other_image):
    # Feature-based matching using ORB
    orb = cv2.ORB_create()
    keypoints1, descriptors1 = orb.detectAndCompute(main_image, None)
    keypoints2, descriptors2 = orb.detectAndCompute(other_image, None)

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(descriptors1, descriptors2)

    # Calculate similarity percentage based on the number of matches
    similarity_percentage = len(matches) / max(len(keypoints1), len(keypoints2)) * 100

    return similarity_percentage

def get_slider_images(url):
        # Create Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--headless")  # This line makes Chrome run in headless mode

    # Initialize a webdriver (e.g., Chrome)
    driver = webdriver.Chrome(options=chrome_options)

    # Navigate to the URL
    driver.get(url)
    time.sleep(5)  # Adjust the sleep time if necessary

    image_urls = set()
    
    if 'daraz.pk' in url:
        # Daraz specific logic
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
        # Naheed specific logic
        images = driver.find_elements(By.TAG_NAME, 'img')

        for img in images:
            src = img.get_attribute('src')
            if src and "/magicslider" in src:
                image_urls.add(src)


    ##########################################################################################
    elif 'cozmetica.pk' in url:
        # Naheed specific logic
        images = driver.find_elements(By.TAG_NAME, 'img')

        for img in images:
            src = img.get_attribute('src')
            if src and "/magicslider" in src:
                image_urls.add(src)
    #######################################################################################################3

    else:
        # General logic for other URLs
        images = driver.find_elements(By.TAG_NAME, 'img')

        for img in images:
            src = img.get_attribute('src')
            if src and src.startswith('http'):
                image_urls.add(src)

    driver.quit()
    return list(image_urls)

def download_images_from_file(file_name, output_folder):
    try:
        # Create the output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)

        with open(file_name, 'r') as file:
            for url in file:
                try:
                    response = requests.get(url.strip())

                    if response.status_code == 200:
                        # Get the image filename from the URL
                        image_name = os.path.join(output_folder, os.path.basename(url.strip()))

                        # Save the image to the specified folder
                        with open(image_name, 'wb') as img_file:
                            img_file.write(response.content)
                            print(f"Image downloaded: {image_name}")
                    else:
                        print(f"Failed to download image from {url.strip()}. Status code: {response.status_code}")

                except Exception as e:
                    print(f"Error downloading {url.strip()}: {e}")

    except Exception as e:
        print(f"Error creating folder {output_folder}: {e}")

# Main execution
url = 'https://www.cozmetica.pk/'  
# Get the main part of the URL (domain)
file_name = get_root_domain(url)
slider_images = get_slider_images(url)

# Save URLs to file
main_scrap_folder ='url_scrap'
os.makedirs(main_scrap_folder, exist_ok=True)

scrap_filename = os.path.join(main_scrap_folder,f'image_url_{file_name}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt')
with open(scrap_filename, 'w') as file:
    for image_url in slider_images:
        file.write(image_url + '\n')

main_download_folder = 'download_images'
os.makedirs(main_download_folder, exist_ok=True)

# Create a subfolder with the current date and time for downloading images
download_folder = os.path.join(main_download_folder, f'{file_name}_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
os.makedirs(download_folder, exist_ok=True)


#download image
download_images_from_file(scrap_filename, download_folder)

# Select the main image
main_image_path = select_image()
main_image = cv2.imread(main_image_path)

# Select the folder containing other images
# other_images_folder = select_folder()
other_images_folder = select_folder()
other_image_files = get_image_files(other_images_folder)

# Calculate SSIM scores
similarity_scores = []
image_names = []

for other_image_file in other_image_files:
    other_image = cv2.imread(other_image_file)
    total_similarity = calculate_similarity_percentage(main_image, other_image)
    similarity_scores.append(total_similarity)
    image_names.append(os.path.basename(other_image_file))

# Display the SSIM scores and match/not match status
for i, (ssim_score, image_name) in enumerate(zip(similarity_scores, image_names)):
    match_status = "Match" if ssim_score > 0.8 else "Not Match"
    print(f"Similarity Score with Image '{image_name}': {ssim_score:.5f} - {match_status}")

# Plot the SSIM scores with match/not match status
plt.figure(figsize=(10, 5))
colors = ['green' if score > 80.0 else 'red' for score in similarity_scores]
plt.bar(image_names, similarity_scores, color=colors)
plt.xlabel('Other Images')
plt.ylabel('Similarity Score')
plt.title('Similarity Scores with Match/Not Match Status')
plt.xticks(rotation=45, ha='right')

# Display match/not match status on the bars
for i, (ssim_score, color) in enumerate(zip(similarity_scores, colors)):
    plt.text(i, ssim_score, f"{ssim_score:.5f}\n{'Match' if ssim_score > 0.8 else 'Not Match'}",
             ha='center', va='bottom', color='black', fontsize=8)

plt.show()
