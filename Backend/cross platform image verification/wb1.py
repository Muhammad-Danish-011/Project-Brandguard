import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def scroll_full_page(driver):
    # Calculate total page height
    scroll_height = driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);")

    # Auto scroll continuously from top to bottom
    scroll_step = 500  # You can adjust the scroll step based on your preference
    current_scroll = 0
    while current_scroll < scroll_height:
        driver.execute_script(f"window.scrollTo(0, {current_scroll});")
        time.sleep(0.5)  # Reduce sleep time for faster scrolling
        current_scroll += scroll_step

def save_content_to_file(content, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)

def extract_iframe_img_urls(driver, content):
    matches = re.findall(r'<iframe id="([^"]+)"', content)
    url_content = []

    for match in matches:
        # Find the iframe element by its ID
        iframe_element = driver.find_element(By.ID, match)

        # Switch to the iframe
        driver.switch_to.frame(iframe_element)

        # Now, you can extract content within the iframe
        inner_html_content = driver.page_source

        # Fix the regex pattern to properly capture the src attribute of img tag
        img_urls = re.findall(r'<img src="([^"]+)"', inner_html_content)

        # Append the extracted URLs to the url_content list
        url_content.extend(img_urls)

        # Switch back to the default content
        driver.switch_to.default_content()

    return url_content

def perform_cross_screen_image_compatibility_test(urls, screen_size):
    # Create Chrome options
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # This line makes Chrome run in headless mode

    # Set the window size based on the user's choice
    if screen_size == 'desktop':
        chrome_options.add_argument("--window-size=1920,1080")  # Adjust the resolution for desktop
    elif screen_size == 'tablet':
        chrome_options.add_argument("--window-size=768,1024")  # Adjust the resolution for tablet
    elif screen_size == 'mobile':
        chrome_options.add_argument("--window-size=375,667")  # Adjust the resolution for mobile

    for url in urls:
        # Initialize a webdriver (e.g., Chrome)
        driver = webdriver.Chrome(options=chrome_options)

        try:
            # Navigate to the provided URL
            driver.get(url)

            # Wait for the page to load completely (you can adjust the time as needed)
            driver.implicitly_wait(10)

            # Scroll the entire page
            scroll_full_page(driver)

            # Get the content after JavaScript execution
            dynamic_content = driver.page_source

            # Save dynamic_content to a text file
            save_content_to_file(dynamic_content, f'text_{url.replace("://", "_").replace("/", "_")}.txt')

            # Extract links from inner_text.txt and write to img.txt
            content = dynamic_content  # Use the dynamic content for extraction
            url_content = extract_iframe_img_urls(driver, content)

            # Write the extracted URLs to url.txt
            with open(f'url_{url.replace("://", "_").replace("/", "_")}.txt', 'w', encoding='utf-8') as file:
                for img_url in url_content:
                    if img_url.startswith(('http', 'https')):
                        file.write(img_url + '\n')

        finally:
            # Close the browser
            driver.quit()

# Example usage:
user_provided_urls = input("Enter the URLs : ").split(',')
print("Choose screen size:")
print("1. Desktop")
print("2. Tablet")
print("3. Mobile")
choice = input("Enter your choice (1/2/3): ")

if choice == '1':
    screen_size = 'desktop'
elif choice == '2':
    screen_size = 'tablet'
elif choice == '3':
    screen_size = 'mobile'
else:
    print("Invalid choice. Please choose 1, 2, or 3.")

perform_cross_screen_image_compatibility_test(user_provided_urls, screen_size)

