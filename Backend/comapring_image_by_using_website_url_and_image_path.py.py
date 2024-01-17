import requests
from bs4 import BeautifulSoup
from skimage.metrics import structural_similarity as ssim
import cv2
import numpy as np
from io import BytesIO
from PIL import Image
from requests.exceptions import ConnectionError, HTTPError
import time

from urllib.parse import urljoin


def download_images(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    images = []

    for img in soup.find_all('img'):
        # Construct the absolute URL
        image_url = urljoin(url, img['src'])
        print(image_url)
        
        try:
            img_response = requests.get(image_url)
            img = Image.open(BytesIO(img_response.content))
            img = img.convert('RGB')
            images.append(np.array(img))
        except Exception as e:
            print(f"Failed to download {image_url}: {e}")

    return images

def compare_images(base_image, images, size=(100, 100)):
    base_image_resized = cv2.resize(np.array(base_image), size, interpolation=cv2.INTER_AREA)
    base_image_gray = cv2.cvtColor(base_image_resized, cv2.COLOR_RGB2GRAY)
    

    # for img in images:
    for img in images:
        if not isinstance(img, np.ndarray) or img.size == 0:
            print("An image is empty or invalid. Skipping this image.")
            continue

        img_resized = cv2.resize(img, size, interpolation=cv2.INTER_AREA)
        img_gray = cv2.cvtColor(img_resized, cv2.COLOR_RGB2GRAY)
        s = ssim(base_image_gray, img_gray)
        threshold = 0.8
        if s > threshold:  # Define a suitable threshold
            return True
    return False



# Load your image
your_image = Image.open('overlay.jpg')

# Download images from the webpage

webpage_url = 'https://docs.opencv.org/4.x/d0/d86/tutorial_py_image_arithmetics.html'
downloaded_images = download_images(webpage_url)

# Compare your image with each downloaded image
is_found = compare_images(your_image, downloaded_images)

print("Image found on webpage:", is_found)



