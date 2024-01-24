import requestsimport requests
from bs4 import BeautifulSoup
from skimage.metrics import structural_similarity as ssim
import cv2
import numpy as np
from io import BytesIO
from PIL import Image
from urllib.parse import urljoin

def download_image(image_url):
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        img = img.convert('RGB')
        return np.array(img)
    except Exception as e:
        print(f"Failed to download {image_url}: {e}")
        return None

def download_images(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    images = []
    for img_tag in soup.find_all('img'):
        if 'src' in img_tag.attrs :
            image_url = urljoin(url, img_tag['src'])
            img = download_image(image_url)
            if img is not None:
                images.append(img)

        elif 'data-src' in img_tag.attrs:
            image_url = urljoin(url, img_tag['data-src'])
            img = download_image(image_url)
            if img is not None:
                images.append(img)

    # print(images)
    return images

def compare_images(base_image, images, target_size=(300, 300)):
    base_image_resized = cv2.resize(base_image, target_size, interpolation=cv2.INTER_AREA)
    base_image_gray = cv2.cvtColor(base_image_resized, cv2.COLOR_RGB2GRAY)

    for img in images:
        img_resized = cv2.resize(img, target_size, interpolation=cv2.INTER_AREA)
        img_gray = cv2.cvtColor(img_resized, cv2.COLOR_RGB2GRAY)
        s = ssim(base_image_gray, img_gray, data_range=img_gray.max() - img_gray.min())
        if s > 0.8:  # Define a suitable threshold
            return True
    return False

def find_image_on_webpage(image_url, webpage_url):
    target_image = download_image(image_url)
    if target_image is None:
        return False

    webpage_images = download_images(webpage_url)
    return compare_images(target_image, webpage_images)

# Example usage
# your_image_url = "https://image.focuspoints.io/Mirjam%20Lurvink.jpg?_jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJmb2N1c1BvaW50WSI6MC4zOSwiZm9jdXNQb2ludFgiOi0wLjAzLCJ3aWR0aCI6MTgwLCJpc3MiOiJmMjFlY2Y3OGM4NDM0ZDVkYjQxZjVkOGEzYWQwZjZkYSIsImFjdGlvbiI6InRyYW5zZm9ybSIsInVybCI6Imh0dHBzOi8vd3d3LmhhbnplLm5sL2JpbmFyaWVzL2NvbnRlbnQvZ2FsbGVyeS9oYW56ZS9vcGxlaWRpbmdlbi9zaWxzL21lZGV3ZXJrZXJzL21pcmphbS1sdXJ2aW5rLmpwZz90cz0xNjU1MzcxNjAxNjgyIiwiaGVpZ2h0IjoxODB9.SL1eQlrTLhlt_YbmpQRsk763fuVAme5fWfBefvcUt3LpUQ4qSqwWaeSOv7CgVDfZTW0aAE3jKAF_BuU7BCqc8g"  # Replace with your image URL
# webpage_url = "https://www.hanze.nl/en/programmes/full-time/master/data-science-for-life-sciences"  # Replace with the webpage URL
#number 2
# webpage_url='https://techmatched.pk/'
# your_image_url='https://techmatched.pk/wp-content/uploads/2022/12/Web-Vertical-Banner-315x1024.png'
#number3
# webpage_url='https://www.naheed.pk/'
# your_image_url='https://media.naheed.pk/homepagetool_homepagetool/t/u/tux-tissue-banner.jpg'
#number4
your_image_url='https://tpc.googlesyndication.com/simgad/15141075400034401808'
webpage_url='https://www.techtarget.com/searchitoperations/definition/Docker'
#numbr5
# your_image_url = "https://cdn.shopify.com/s/files/1/0509/7550/6593/files/loreal-skin-fl-glow-up-1x1.jpg?v=1705778688"
# webpage_url = "https://cozmetica.pk/"
is_found = find_image_on_webpage(your_image_url, webpage_url)
print("Image found on webpage:", is_found)


is_found = find_image_on_webpage(your_image_url, webpage_url)
print("Image found on webpage:", is_found)
