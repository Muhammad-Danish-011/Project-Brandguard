import requests
from bs4 import BeautifulSoup
from skimage.metrics import structural_similarity as ssim
import cv2
import numpy as np
from io import BytesIO
from PIL import Image
from urllib.parse import urljoin


def download_images_from_url(url):
    images = []
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for img in soup.find_all('img'):
            # Check if 'src' attribute exists in the 'img' tag
            if 'src' in img.attrs:
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
            else:
                image_url = urljoin(url, img['data-src'])
                try:
                    img_response = requests.get(image_url)
                    img = Image.open(BytesIO(img_response.content))
                    img = img.convert('RGB')
                    images.append(np.array(img))
                except Exception as e:
                    print(f"Failed to download {image_url}: {e}")
                # print("Skipping image without 'src' attribute.")

    except Exception as e:
        print(f"Failed to fetch content from {url}: {e}")

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


#
your_image = Image.open('321.jpg')

# Download images from the webpage

webpage_url = 'https://www.techtarget.com/searchitoperations/definition/Docker'
downloaded_images = download_images_from_url(webpage_url)

# Compare your image with each downloaded image
is_found = compare_images(your_image, downloaded_images)

print("Image found on webpage:", is_found)


