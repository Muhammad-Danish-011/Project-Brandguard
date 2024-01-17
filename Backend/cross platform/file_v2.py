import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import threading

def scrape_data(url, size):
    # Create Chrome options
    chrome_options = Options()
    # Set the window size
    chrome_options.add_argument(f"--window-size={size[0]},{size[1]}")

    # Initialize a webdriver (e.g., Chrome)
    driver = webdriver.Chrome(options=chrome_options)

    # Navigate to the URL
    driver.get(url)

    # Wait for the page to load completely (you can adjust the time as needed)
    driver.implicitly_wait(10)

    # Wait for an additional 5 seconds
    time.sleep(5)

    # Auto scroll to the middle of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 2);")
    time.sleep(2)

    # Auto scroll to the bottom of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    # Get the content after JavaScript execution
    dynamic_content = driver.page_source

    # Save dynamic_content to a text file
    with open(f'text_{size[0]}x{size[1]}.txt', 'w', encoding='utf-8') as file:
        file.write(dynamic_content)

    # Part 1: Extract links from text.txt and write to url.txt
    with open(f'text_{size[0]}x{size[1]}.txt', 'r', encoding='utf-8') as file:
        content = file.read()

    # Fix the regular expression to properly capture the iframe tag
    matches = re.findall(r'<iframe id="([^"]+)"', content)

    url_content = []

    # Extract <img> URLs from the main content
    # img_urls_in_main_content = re.findall(r'<img src="([^"]+)"', content)
    img_urls_in_main_content = re.findall(r'<img[^>]*>', content)
    url_content.extend(img_urls_in_main_content)

    for match in matches:
        # Find the iframe element by its ID
        iframe_element = driver.find_element(By.ID, match)

        # Switch to the iframe
        driver.switch_to.frame(iframe_element)

        # Now, you can extract content within the iframe
        inner_html_content = driver.page_source

        # Fix the regex pattern to properly capture the src attribute of img tag
        img_urls_in_iframe = re.findall(r'<img src="([^"]+)"', inner_html_content)

        # Append the extracted URLs from the iframe to the url_content list
        url_content.extend(img_urls_in_iframe)

        # Switch back to the default content
        driver.switch_to.default_content()

    # Write the extracted URLs to url.txt
    with open(f'url_{size[0]}x{size[1]}.txt', 'w', encoding='utf-8') as file:
        for img_url in url_content:
            if img_url.startswith(('http', 'https')) or img_url.lower().endswith('.jpg'):
                file.write(img_url + '\n')

    # Close the browser
    driver.quit()

# Define the URL and window sizes
    
url = "https://www.daraz.pk/"
# url = "https://www.spiceworks.com/tech/artificial-intelligence/articles/what-is-sentiment-analysis/"

# url = "https://www.techtarget.com/searchitoperations/definition/Docker"
window_sizes = [(1200, 800), (768, 1024), (375, 667)]

# Create threads for each window size
threads = []

for size in window_sizes:
    thread = threading.Thread(target=scrape_data, args=(url, size))
    threads.append(thread)
    thread.start()

# Wait for all threads to finish
for thread in threads:
    thread.join()
