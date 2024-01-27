import cv2
import numpy as np
from app.models.models import *
def find_image_position(screenshot_path, reference_image_path):
    # Read the screenshot and reference image
    screenshot = cv2.imread(screenshot_path)
    reference_image = cv2.imread(reference_image_path)

    # Convert images to grayscale
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    reference_image_gray = cv2.cvtColor(reference_image, cv2.COLOR_BGR2GRAY)

    # Use template matching to find the location of the reference image
    result = cv2.matchTemplate(screenshot_gray, reference_image_gray, cv2.TM_CCOEFF_NORMED)

    # Define a threshold
    threshold = 0.8
    locations = np.where(result >= threshold)
    locations = list(zip(*locations[::-1]))  # Switch x and y coordinates to (x, y)

    if not locations:
        return "Reference image not found."

    # For simplicity, take the first location found above the threshold
    max_loc = locations[0]

    # Determine the position of the reference image
    height, width = reference_image_gray.shape
    mid_x, mid_y = max_loc[0] + width // 2, max_loc[1] + height // 2

    # Initialize positions based on relative location
    position_names = {
        'top': False,
        'bottom': False,
        'left': False,
        'right': False,
        'mid': False
    }

    # Update positions based on relative location
    screen_width, screen_height = screenshot.shape[1], screenshot.shape[0]
    position_names['top'] = mid_y < screen_height / 3
    position_names['bottom'] = mid_y > 2 * screen_height / 3
    position_names['left'] = mid_x < screen_width / 3
    position_names['right'] = mid_x > 2 * screen_width / 3
    position_names['mid'] = not any([position_names['top'], position_names['bottom'], position_names['left'], position_names['right']])

    # Print only the true positions
    true_positions = [key for key, value in position_names.items() if value]
    print("Reference image position: " + ', '.join(true_positions))
    return "Reference image position: " + ', '.join(true_positions)

def get_screenshot_path(campainID):
  screenshots = Screenshots.query.filter_by(CampaignID=campainID).all()
  file_path=None
# Generate and print file paths for each screenshot
  for screenshot in screenshots:
    file_path = screenshot.FilePath
    #break
#   print(file_path)
  return(file_path)

def get_refrence_image(campaignID):
    image = Images.query.filter_by(CampaignID=campaignID).first()

    if image:
        image_path = image.ImagePath
        # print(image_path)
        return(image_path)
    else:
        print("Image not found for the given Campaign ID.")


 
