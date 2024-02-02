import os
from datetime import datetime  # Corrected import statement

from app.extensions import db
from app.main import bp
from app.models.models import *
from app.utils.img_grabber import *
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, current_app, jsonify, request
from flask_cors import CORS
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})


scheduler = BackgroundScheduler()
scheduler.start()
CORS(bp)

UPLOAD_FOLDER = os.path.abspath('./reference_images')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Define allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Create a new Campaign


# @bp.route('/campaigns', methods=['POST'])
# def create_campaign():
#     data = request.get_json()

#     if 'CampaignName' not in data or 'StartDate' not in data or 'EndDate' not in data or 'IntervalTime' not in data or 'Status' not in data:
#         return jsonify(message='Invalid request data'), 400

#     new_campaign = Campaigns(
#         CampaignName=data['CampaignName'],
#         StartDate=datetime.strptime(
#             data['StartDate'], '%Y-%m-%d %H:%M:%S'),  # Convert to datetime
#         EndDate=datetime.strptime(
#             data['EndDate'], '%Y-%m-%d %H:%M:%S'),  # Convert to datetime
#         IntervalTime=data['IntervalTime'],
#         Status=data['Status']
#     )
#     db.session.add(new_campaign)
#     db.session.commit()
#     return jsonify(message='Campaign created successfully'), 201


# @bp.route('/campaigns', methods=['GET'])
# def get_campaigns():
#     campaigns = Campaigns.query.all()
#     result = []
#     for campaign in campaigns:
#         result.append({
#             'CampaignID': campaign.CampaignID,
#             'CampaignName': campaign.CampaignName,
#             'StartDate': campaign.StartDate,
#             'EndDate': campaign.EndDate,
#             'IntervalTime': campaign.IntervalTime,
#             'Status': campaign.Status
#         })
#     return jsonify(result)


# # Create a new Website
# @bp.route('/websites', methods=['POST'])
# def create_website():
#     data = request.get_json()

#     if 'CampaignID' not in data or 'WebsiteURL' not in data:
#         return jsonify(message='Invalid request data'), 400

#     new_website = Websites(
#         CampaignID=data['CampaignID'],
#         WebsiteURL=data['WebsiteURL']
#     )
#     db.session.add(new_website)
#     db.session.commit()
#     return jsonify(message='Website created successfully'), 201


# # Get all Websites
# @bp.route('/websites', methods=['GET'])
# def get_websites():
#     websites = Websites.query.all()
#     result = []
#     for website in websites:
#         result.append({
#             'WebsiteID': website.WebsiteID,
#             'CampaignID': website.CampaignID,
#             'WebsiteURL': website.WebsiteURL
#         })
#     return jsonify(result)


# # Create an Image
# @bp.route('/images', methods=['POST'])
# def create_image():
#     data = request.get_json()
#     new_image = Images(
#         CampaignID=data['CampaignID'],
#         Extension=data['Extension'],
#         ImagePath=data['ImagePath']
#     )
#     db.session.add(new_image)
#     db.session.commit()
#     return jsonify({'message': 'Image created successfully'}), 201

# # Get All Images


# @bp.route('/images', methods=['GET'])
# def get_images():
#     images = Images.query.all()
#     result = []
#     for image in images:
#         result.append({
#             'ImageID': image.ImageID,
#             'CampaignID': image.CampaignID,
#             'Extension': image.Extension,
#             'ImagePath': image.ImagePath
#         })
#     return jsonify(result)

# # Create a Screenshot


# @bp.route('/screenshots', methods=['POST'])
# def create_screenshot():
#     data = request.get_json()
#     new_screenshot = Screenshots(
#         CampaignID=data['CampaignID'],
#         WebsiteID=data['WebsiteID'],
#         ImageID=data['ImageID'],
#         Extension=data['Extension'],
#         Timestamp=data['Timestamp'],
#         FilePath=data['FilePath']
#     )
#     db.session.add(new_screenshot)
#     db.session.commit()
#     return jsonify({'message': 'Screenshot created successfully'}), 201

# # Get All Screenshots


# @bp.route('/screenshots', methods=['GET'])
# def get_screenshots():
#     screenshots = Screenshots.query.all()
#     result = []
#     for screenshot in screenshots:
#         result.append({
#             'ScreenshotID': screenshot.ScreenshotID,
#             'CampaignID': screenshot.CampaignID,
#             'WebsiteID': screenshot.WebsiteID,
#             'ImageID': screenshot.ImageID,
#             'Extension': screenshot.Extension,
#             'Timestamp': screenshot.Timestamp,
#             'FilePath': screenshot.FilePath
#         })
#     return jsonify(result)


# # Create an Ad Position
# @bp.route('/adpositions', methods=['POST'])
# def create_ad_position():
#     data = request.get_json()
#     new_ad_position = AdPositions(
#         ScreenshotID=data['ScreenshotID'],
#         XCoordinate=data['XCoordinate'],
#         YCoordinate=data['YCoordinate']
#     )
#     db.session.add(new_ad_position)
#     db.session.commit()
#     return jsonify({'message': 'Ad Position created successfully'}), 201

# # Get All Ad Positions


# @bp.route('/adpositions', methods=['GET'])
# def get_ad_positions():
#     ad_positions = AdPositions.query.all()
#     result = []
#     for ad_position in ad_positions:
#         result.append({
#             'AdPositionID': ad_position.AdPositionID,
#             'ScreenshotID': ad_position.ScreenshotID,
#             'XCoordinate': ad_position.XCoordinate,
#             'YCoordinate': ad_position.YCoordinate
#         })
#     return jsonify(result)


# # Create a Scraped Image
# @bp.route('/scraped-images', methods=['POST'])
# def create_scraped_image():
#     data = request.get_json()
#     new_scraped_image = ScrapedImages(
#         ScreenshotID=data['ScreenshotID'],
#         Extension=data['Extension'],
#         FilePath=data['FilePath']
#     )
#     db.session.add(new_scraped_image)
#     db.session.commit()
#     return jsonify({'message': 'Scraped Image created successfully'}), 201

# # Get All Scraped Images


# @bp.route('/scraped-images', methods=['GET'])
# def get_scraped_images():
#     scraped_images = ScrapedImages.query.all()
#     result = []
#     for scraped_image in scraped_images:
#         result.append({
#             'ScrapedImageID': scraped_image.ScrapedImageID,
#             'ScreenshotID': scraped_image.ScreenshotID,
#             'Extension': scraped_image.Extension,
#             'FilePath': scraped_image.FilePath
#         })
#     return jsonify(result)

# # Create a URL


# @bp.route('/urls', methods=['POST'])
# def create_url():
#     data = request.get_json()
#     new_url = URLS(
#         webpage_url=data['webpage_url'],
#         template_url=data['template_url']
#     )
#     db.session.add(new_url)
#     db.session.commit()
#     return jsonify({'message': 'URL created successfully'}), 201

# # Get All URLs


# @bp.route('/urls', methods=['GET'])
# def get_urls():
#     urls = URLS.query.all()
#     result = []
#     for url in urls:
#         result.append({
#             'URL_id': url.URL_id,
#             'webpage_url': url.webpage_url,
#             'template_url': url.template_url
#         })
#     return jsonify(result)


# # Define an API endpoint to capture screenshots by campaignID
# @bp.route('/screenshot/<int:campaignID>', methods=['GET'])
# def capture_screenshot_api(campaignID):
#     try:
#         result = schedule_screenshot_capture(campaignID)
#         return jsonify(result)
#     except Exception as e:
#         traceback.print_exc()  # Log the exception traceback
#         return {"error": str(e)}, 500


# @bp.route('/interval_time/<int:campaignID>', methods=['GET'])
# def interval_time(campaignID):
#     try:
#         result = get_interval_time(campaignID)
#         return jsonify(result)
#     except Exception as e:
#         traceback.print_exc()  # Log the exception traceback
#         return {"error": str(e)}, 500


# @bp.route('/get_website/<int:campaignID>', methods=['GET'])
# def getwebsite(campaignID):
#     try:
#         result = get_website(campaignID)
#         return (result)
#     except Exception as e:
#         traceback.print_exc()  # Log the exception traceback
#         return {"error": str(e)}, 500


@bp.route('/campaign_details', methods=['POST'])
def add_campaign_details():
    try:
        # Extract data from the request JSON
        data = request.get_json()
        campaign_name = data.get('CampaignName')
        start_date = datetime.strptime(
            data.get('StartDate'), '%Y-%m-%d %H:%M:%S')
        end_date = datetime.strptime(data.get('EndDate'), '%Y-%m-%d %H:%M:%S')
        interval_time = int(data.get('IntervalTime'))
        websites = data.get('Websites')
        images = data.get('Images')
        current_datetime = datetime.now()

        # Determine the status based on the current date
        status = 'active' if start_date <= current_datetime <= end_date else 'inactive'

        # Create a new campaign
        new_campaign = Campaigns(
            CampaignName=campaign_name,
            StartDate=start_date,
            EndDate=end_date,
            IntervalTime=interval_time,
            Status=status
        )

        # Create a list of website instances
        website_instances = [Websites() for _ in websites]
        # Create image instances

        # Create image instances
        image_instances = []
        for image_path in images:
            image = Images()
            image.ImagePath = image_path
            image_instances.append(image)
        # Set WebsiteURL for each website instance
        for i, website in enumerate(website_instances):
            website.WebsiteURL = websites[i]
        # Associate the websites with the campaign
        new_campaign.websites.extend(website_instances)
        new_campaign.images.extend(image_instances)

        # Add the campaign and related entities to the database
        db.session.add(new_campaign)
        db.session.add_all(website_instances)
        db.session.add_all(image_instances)
        db.session.commit()

        current_app.logger.info(
            f"Campaign status set to: {new_campaign.Status}")  # Logging status

        # Schedule the campaign if it's active
        if new_campaign.Status == 'active':
            schedule_campaign(new_campaign.CampaignID, interval_time)

        response_data = {
            "status": "Campaign added successfully.",
            "CampaignID": new_campaign.CampaignID
        }

        return jsonify(response_data), 201

    except Exception as e:
        current_app.logger.error(
            f"Error in add_campaign_details: {e}")  # Log the exception
        return jsonify({"error": str(e)}), 500


def schedule_campaign(campaignID, interval_time):
    """
    Schedule tasks for a specific campaign.
    """
    scheduler.add_job(
        capture_screenshot_by_campaignid,
        'interval',
        minutes=interval_time,
        args=[campaignID],
        max_instances=5
    )
    scheduler.add_job(
        image_scraping,
        'interval',
        minutes=interval_time,
        args=[campaignID]
    )


# @bp.route('/image_position/<int:campaignID>', methods=['GET'])
# def img_position(campaignID):
#     result = image_position(campaignID)
#     return jsonify(result)


@bp.route('/upload', methods=['POST'])
def upload_image():
    # Check if the post request has the file part
    if 'image' not in request.files:
        return 'No file part', 400

    file = request.files['image']

    # If the user does not select a file, the browser submits an empty file without a filename
    if file.filename == '':
        return 'No selected file', 400

    if file and allowed_file(file.filename):
        # Use secure_filename to avoid security issues
        filename = secure_filename(file.filename)

        # Save the file to the specified upload folder
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # Ensure the directory exists before saving
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        file.save(file_path)

        try:
            # Return the path of the saved file
            return {"message": "File uploaded successfully", "file_path": file_path}
        except Exception as e:
            print(f"An error occurred: {e}")
            return {"error": "Internal Server Error"}, 500

    return 'Invalid file format', 400


@bp.route('/save_image_path', methods=['POST'])
def save_image_path():
    try:
        data = request.get_json()

        # Make sure the key matches the JSON you're sending
        new_image_path = data.get('new_image_path', '')
        new_campaign_id = data.get('campaign_id', '')
        print("Received file path:", new_image_path)

        if new_image_path:  # Check if the path is not empty
            new_image = Images(CampaignID=new_campaign_id,
                               ImagePath=new_image_path)
            db.session.add(new_image)
            db.session.commit()
            return jsonify({"message": "Image path saved successfully"})
        else:
            return jsonify({"error": "No image path provided"}), 400
    except Exception as e:
        traceback.print_exc()  # This will print the stack trace to the console
        return jsonify({"error": f"Error saving image path: {str(e)}"}), 500


@bp.route('/general_report', methods=['GET'])
def get_general_report():
    try:
        # Fetch data from Campaigns, Websites, AdPositions, and Scrape_Image_Status tables
        campaigns = Campaigns.query.all()

        general_report = []
        for campaign in campaigns:
            # Fetch data for each campaign
            campaign_data = {
                'CampaignID': campaign.CampaignID,
                'CampaignName': campaign.CampaignName,
                'StartDate': campaign.StartDate.strftime('%Y-%m-%d %H:%M:%S'),
                'EndDate': campaign.EndDate.strftime('%Y-%m-%d %H:%M:%S'),
                'WebsiteURL': [],
                'Found_Status_Screenshot': 0,  # Initialize to 0, will be calculated later
                'Found_Status_Scraping': 0  # Initialize to 0, will be calculated later
            }

            # Fetch associated websites for the campaign
            websites = Websites.query.filter_by(
                CampaignID=campaign.CampaignID).all()
            for website in websites:
                campaign_data['WebsiteURL'].append(website.WebsiteURL)

            # Fetch AdPositions for the campaign
            ad_positions = AdPositions.query.filter_by(
                CampaignID=campaign.CampaignID).all()

            # Calculate Found_Status_Screenshot as a percentage
            total_positions = len(ad_positions)
            found_positions_screenshot = sum(
                1 for ad_position in ad_positions if ad_position.Found_Status == 'yes')

            if total_positions > 0:
                campaign_data['Found_Status_Screenshot'] = found_positions_screenshot / \
                    total_positions * 100

            # Fetch Scrape_Image_Status for the campaign
            scrape_image_statuses = Scrape_Image_Status.query.filter_by(
                CampaignID=campaign.CampaignID).all()

            # Calculate Found_Status_Scraping as a percentage
            total_scrape_statuses = len(scrape_image_statuses)
            found_scrape_statuses = sum(
                1 for scrape_status in scrape_image_statuses if scrape_status.Found_Status == 'yes')

            if total_scrape_statuses > 0:
                campaign_data['Found_Status_Scraping'] = found_scrape_statuses / \
                    total_scrape_statuses * 100

            general_report.append(campaign_data)

        return jsonify(general_report)

    except Exception as e:
        current_app.logger.error(f"Error in get_general_report: {e}")
        return jsonify({"error": str(e)}), 500


@bp.route('/scraping_report/<int:campaignID>', methods=['GET'])
def get_scraping_report(campaignID):
    try:
        # Fetch data from Campaigns, Websites, and Scrape_Image_Status tables for the specified campaignID
        campaign = Campaigns.query.get(campaignID)

        if not campaign:
            return jsonify({"error": "Campaign not found"}), 404

        scraping_report = {
            'CampaignID': campaign.CampaignID,
            'CampaignName': campaign.CampaignName,
            'WebsiteURL': [],
            'ScrapeImageStatus': []
        }

        # Fetch associated websites for the campaign
        websites = Websites.query.filter_by(
            CampaignID=campaign.CampaignID).all()
        for website in websites:
            scraping_report['WebsiteURL'].append(website.WebsiteURL)

        # Fetch Scrape_Image_Status for the campaign
        scrape_image_statuses = Scrape_Image_Status.query.filter_by(
            CampaignID=campaign.CampaignID).all()

        for scrape_status in scrape_image_statuses:
            scrape_data = {
                'DateTime': scrape_status.DateTime.strftime('%Y-%m-%d %H:%M:%S'),
                'Found_Status': scrape_status.Found_Status
            }
            scraping_report['ScrapeImageStatus'].append(scrape_data)

        return jsonify(scraping_report)

    except Exception as e:
        current_app.logger.error(f"Error in get_scraping_report: {e}")
        return jsonify({"error": str(e)}), 500


@bp.route('/screenshot_report/<int:campaignID>', methods=['GET'])
def get_screenshot_report(campaignID):
    try:
        # Fetch data from Campaigns, Websites, AdPositions, and Screenshots tables for the specified campaignID
        campaign = Campaigns.query.get(campaignID)

        if not campaign:
            return jsonify({"error": "Campaign not found"}), 404

        screenshot_report = {
            'CampaignID': campaign.CampaignID,
            'CampaignName': campaign.CampaignName,
            'WebsiteURL': [],
            'AdPositions': []
        }

        # Fetch associated websites for the campaign
        websites = Websites.query.filter_by(
            CampaignID=campaign.CampaignID).all()
        for website in websites:
            screenshot_report['WebsiteURL'].append(website.WebsiteURL)

        # Fetch AdPositions and Screenshots for the campaign
        ad_positions = AdPositions.query.filter_by(
            CampaignID=campaign.CampaignID).all()

        for ad_position in ad_positions:
            # Fetch the corresponding screenshot to get FilePath
            screenshot = Screenshots.query.filter_by(
                ScreenshotID=ad_position.ScreenshotID).first()

            screenshot_data = {
                'Capture_DateTime': ad_position.Capture_DateTime.strftime('%Y-%m-%d %H:%M:%S'),
                'FilePath': screenshot.FilePath if screenshot else None,
                'Found_Status': ad_position.Found_Status
            }
            screenshot_report['AdPositions'].append(screenshot_data)

        return jsonify(screenshot_report)

    except Exception as e:
        current_app.logger.error(f"Error in get_screenshot_report: {e}")
        return jsonify({"error": str(e)}), 500
