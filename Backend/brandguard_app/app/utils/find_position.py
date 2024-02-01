import cv2
import numpy as np
from app.models.models import *
from sqlalchemy import func


def find_image_position(screenshot_path, reference_image_path, campaignID):
    # Read the screenshot and reference image
    screenshot = cv2.imread(screenshot_path)
    reference_image = cv2.imread(reference_image_path)

    # Convert images to grayscale
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    reference_image_gray = cv2.cvtColor(reference_image, cv2.COLOR_BGR2GRAY)

    # Use template matching to find the location of the reference image
    result = cv2.matchTemplate(
        screenshot_gray, reference_image_gray, cv2.TM_CCOEFF_NORMED)

    # Define a threshold
    threshold = 0.8
    locations = np.where(result >= threshold)
    # Switch x and y coordinates to (x, y)
    locations = list(zip(*locations[::-1]))

    # if not locations:
    #     return "Reference image not found."

    if not locations:
        # Reference image not found
        save_found_status(campaignID, found='no')
        # calculate_success_rate(campaignID)
        return "Reference image not found."
     # Reference image found
    save_found_status(campaignID, found='yes')
    # calculate_success_rate(campaignID)

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
    position_names['mid'] = not any(
        [position_names['top'], position_names['bottom'], position_names['left'], position_names['right']])

    # Print only the true positions
    true_positions = [key for key, value in position_names.items() if value]
    print("Reference image position: " + ', '.join(true_positions))
    return "Reference image position: " + ', '.join(true_positions)


def get_screenshot_path(campaignID):
    latest_screenshot = Screenshots.query.filter_by(CampaignID=campaignID).order_by(
        Screenshots.Timestamp.desc()).first()

    print(f"Hammad print {latest_screenshot}")

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
            print(f"\n\n\n\n\n\n\n\n\nHammad print screenshotID {screenshotID}\n\n\n\n\n\n\n\n\n\n")

    new_AdPositions = AdPositions(
        ScreenshotID=screenshotID,
        CampaignID=campaignID,
        Found_Status=found
    )
    db.session.add(new_AdPositions)
    db.session.commit()


# def calculate_success_rate(campaignID):
#     # Query the visibility table to get counts
#     total_count = AdPositions.query.filter_by(CampaignID=campaignID).count()
#     success_count = AdPositions.query.filter(func.lower(
#         AdPositions.Found_Status) == 'yes', AdPositions.CampaignID == campaignID).count()



################################          for testing purpose by gpt

# def calculate_success_rate(campaignID):
#     # Join the AdPositions, Campaigns, and Websites tables
#     query_result = db.session.query(
#         AdPositions.CampaignID,
#         Campaigns.CampaignName,                                                   
#         Campaigns.StartDate,
#         Campaigns.EndDate,
#         Websites.WebsiteURL,
#         AdPositions.Found_Status
#     ).join(Campaigns, AdPositions.CampaignID == Campaigns.CampaignID) \
#      .join(Websites, AdPositions.ScreenshotID == Websites.WebsiteID) \
#      .filter(AdPositions.CampaignID == campaignID).all()

#     # Print the results in a table format
#     print("{:<15} {:<20} {:<20} {:<20} {:<20} {:<15}".format(
#         "Campaign ID", "Campaign Name", "Start Date", "End Date", "Website URL", "Found Status"))
    
#     for result in query_result:
#         campaign_id, campaign_name, start_date, end_date, website_url, found_status = result
#         print("{:<15} {:<20} {:<20} {:<20} {:<20} {:<15}".format(
#             campaign_id, campaign_name, start_date, end_date, website_url, found_status))
    

#######################             testing purpose by hammad
    
# def calculate_success_rate(campaignID):
# # Create a new visibility record and add it to the database
#     campaigns = Campaigns.query.filter_by(CampaignID=campaignID).first()
#     if campaigns:
#             campaignName = campaigns.CampaignName
#             start_date = campaigns.StartDate
#             end_date = campaigns.EndDate

#             print(f"\n\n\n\n\n\n\n\n\nHammad print screenshotID {campaignName}+++++++++++++++{start_date}+++++++++++++++{end_date} \n\n\n\n\n\n\n\n\n\n")
