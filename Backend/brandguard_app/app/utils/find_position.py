import cv2
import numpy as np
from app.models.models import *


def find_image_position(screenshot_path, reference_image_path, campaignID, scales=np.linspace(0.5, 1.5, 20), threshold=0.7):
    # Read the screenshot and reference image
    screenshot = cv2.imread(screenshot_path)
    reference_image = cv2.imread(reference_image_path)
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    reference_image_gray = cv2.cvtColor(reference_image, cv2.COLOR_BGR2GRAY)

    # Get screen dimensions
    screen_height, screen_width = screenshot_gray.shape

    # Variables to keep track of the best match
    best_match = None
    best_match_value = threshold  # Initial threshold
    best_scale = 1
    best_location = (0, 0)

    # Iterate over the scales
    for scale in scales:
        # Resize the reference image according to the current scale
        resized_reference = cv2.resize(reference_image_gray, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)

        # Check if the resized reference image is smaller than the screenshot
        if resized_reference.shape[0] > screenshot_gray.shape[0] or resized_reference.shape[1] > screenshot_gray.shape[1]:
            continue

        # Perform template matching
        result = cv2.matchTemplate(screenshot_gray, resized_reference, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # Update best match if a better one is found
        if max_val > best_match_value:
            best_match_value = max_val
            best_match = result
            best_scale = scale
            best_location = max_loc

    # Check if a match was found
    if best_match is None:
        save_found_status(campaignID, found='no')
        return "Reference image not found."

    save_found_status(campaignID, found='yes')

    # Calculate the position of the best match
    ref_image_height, ref_image_width = reference_image_gray.shape[:2]
    top_left = best_location
    bottom_right = (top_left[0] + int(ref_image_width * best_scale), top_left[1] + int(ref_image_height * best_scale))

    # Calculate midpoints
    mid_x = (top_left[0] + bottom_right[0]) // 2
    mid_y = (top_left[1] + bottom_right[1]) // 2

    # Determine the position names
    position_names = {}
    position_names['top'] = mid_y < screen_height / 3
    position_names['bottom'] = mid_y > 2 * screen_height / 3
    position_names['left'] = mid_x < screen_width / 3
    position_names['right'] = mid_x > 2 * screen_width / 3
    position_names['mid'] = not any([position_names['top'], position_names['bottom'], position_names['left'], position_names['right']])

    # Construct the result string
    result_string = "Reference image found at "
    for position, value in position_names.items():
        if value:
            result_string += position + " "

    print(result_string)
    return result_string


def get_screenshot_path(campaignID):
    latest_screenshot = Screenshots.query.filter_by(CampaignID=campaignID).order_by(
        Screenshots.Timestamp.desc()).first()

    if latest_screenshot is not None:
        return latest_screenshot.FilePath
    else:
        return None


def get_refrence_image(campaignID):
    image = Images.query.filter_by(CampaignID=campaignID).first()

    if image:
        image_path = image.ImagePath
        # print(image_path)
        return (image_path)
    else:
        print("Image not found for the given Campaign ID.")


def save_found_status(campaignID, found):
    # Create a new visibility record and add it to the database
    screenshot = Screenshots.query.filter_by(CampaignID=campaignID).order_by(
        Screenshots.Timestamp.desc()).first()
    if screenshot:
        screenshotID = screenshot.ScreenshotID

    new_AdPositions = AdPositions(
        ScreenshotID=screenshotID,
        CampaignID=campaignID,
        Found_Status=found
    )
    db.session.add(new_AdPositions)
    db.session.commit()


# def calculate_success_rate(campaignID):
#     # Query the visibility table to get counts
#     total_count = visibility.query.filter_by(CampaignID=campaignID).count()
#     success_count = visibility.query.filter(func.lower(
#         visibility.Found_Status) == 'yes', visibility.CampaignID == campaignID).count()

    # if total_count > 0:
    #     success_rate = (success_count / total_count) * 100
    #     print("\n\n")
    #     print(f"campaignID: {campaignID}")
    #     print(f"yes count: {success_count}")
    #     print(f"total count: {total_count}")
    #     print(f"Success Rate: {success_rate}%")
    #     print("\n\n")
    # else:
    #     print("\n\n")
    #     print("No detection results in the database.")
    #     print("\n\n")
