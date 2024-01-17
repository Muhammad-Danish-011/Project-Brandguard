
# ################################################## tech target web


# import time
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.common.exceptions import WebDriverException
# from selenium.webdriver.chrome.options import Options
# import re


# # Create Chrome options
# chrome_options = Options()
# #chrome_options.add_argument("--headless")  # This line makes Chrome run in headless mode

# url = "https://www.techtarget.com/searchitoperations/definition/Docker"

# # Initialize a webdriver (e.g., Chrome)
# driver = webdriver.Chrome(options=chrome_options)

# # Navigate to the URL
# driver.get(url)

# # Wait for the page to load completely (you can adjust the time as needed)
# driver.implicitly_wait(10)

# # Wait for an additional 10 minutes
# time.sleep(5)

# # Get the content after JavaScript execution
# dynamic_content = driver.page_source
# # Save dynamic_content to a text file


# # # Find all iframes on the page
# # iframes = driver.find_elements(By.TAG_NAME, 'iframe')

# # # Print iframe IDs on the console
# # for iframe in iframes:
# #     iframe_id = iframe.get_attribute('id')
    


# # # Find the iframe element by its ID, name, or any other locator strategy                                 top iframe 
# # iframe_element_{iframe_id} = driver.find_element(By.ID, "{iframe_id}")
# # # Switch to the iframe
# # driver.switch_to.frame(iframe_element_{iframe_id})

# # # Now, you can extract content within the iframe
# # inner_html_content_{iframe_id} = driver.page_source

# # # Switch back to the default content
# # driver.switch_to.default_content()


# with open('text.txt', 'w', encoding='utf-8') as file:
#     file.write(dynamic_content)

# # Part 1: Extract links from inner_text.txt and write to img.txt
# with open('text.txt', 'r', encoding='utf-8') as file:
#     content = file.read()

# # Fix the regular expression to properly capture the src attribute
# matches = re.findall(r'<iframe id="([^"]+)"', content)


# for match in matches:
    
#     # Find the iframe element by its ID, name, or any other locator strategy                                 top iframe 
#     iframe_element_{match} = driver.find_element(By.ID, "{match}")
#     # Switch to the iframe
#     driver.switch_to.frame(iframe_element_{match})

#     # Now, you can extract content within the iframe
#     inner_html_content_{match} = driver.page_source

#     url_content = re.findall(r'<img id="([^"]+)"', inner_html_content_{match})

#     # Switch back to the default content
#     driver.switch_to.default_content()

# with open('url.txt', 'w', encoding='utf-8') as file:
#     file.write(url_content)

# # Close the browser
# driver.quit()


########################################## update 1


import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Create Chrome options
chrome_options = Options()
# chrome_options.add_argument("--headless")  # This line makes Chrome run in headless mode

#url = "https://www.spiceworks.com/tech/artificial-intelligence/articles/what-is-sentiment-analysis/"

url = "https://www.techtarget.com/searchitoperations/definition/Docker"

# Initialize a webdriver (e.g., Chrome)
driver = webdriver.Chrome(options=chrome_options)

# Navigate to the URL
driver.get(url)

# Wait for the page to load completely (you can adjust the time as needed)
driver.implicitly_wait(10)

# Wait for an additional 10 minutes
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
with open('text.txt', 'w', encoding='utf-8') as file:
    file.write(dynamic_content)

# Part 1: Extract links from inner_text.txt and write to img.txt
with open('text.txt', 'r', encoding='utf-8') as file:
    content = file.read()

# Fix the regular expression to properly capture the iframe tag
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

# Write the extracted URLs to url.txt
with open('url.txt', 'w', encoding='utf-8') as file:
    for url in url_content:
        if url.startswith(('http', 'https')):
            file.write(url + '\n')

# Close the browser
driver.quit()
