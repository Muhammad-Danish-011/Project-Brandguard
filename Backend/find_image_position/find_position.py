import cv2
import numpy as np

def find_image_position(screenshot_path, reference_image_path):
    # Read the screenshot and reference image
    screenshot = cv2.imread(screenshot_path)
    reference_image = cv2.imread(reference_image_path)

    # Convert images to grayscale
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    reference_image_gray = cv2.cvtColor(reference_image, cv2.COLOR_BGR2GRAY)

    # Use template matching to find the location of the reference image
    result = cv2.matchTemplate(screenshot_gray, reference_image_gray, cv2.TM_CCOEFF_NORMED)
    _, _, _, max_loc = cv2.minMaxLoc(result)

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
    print("Reference image position:", ', '.join(true_positions))

# Example usage
screenshot_path = '/home/shahzaibkhan/work/brandguard/webdriver_mvp_xloop/screenshots/Kokan - 20240116200720/screenshot_20240116200819.png'
# reference_image_path = '/home/shahzaibkhan/work/brandguard/img_comp/ad_banner_template.png'
reference_image_path = '/home/shahzaibkhan/work/brandguard/img_comp/ad_banner_template.png'

find_image_position(screenshot_path, reference_image_path)

# position = find_image_position(screenshot_path, reference_image_path)
# print("Reference image position:", position)