import os
from datetime import datetime  # Corrected import statement

from app.extensions import db
from app.main import bp
from app.models.models import *
from app.utils.img_grabber import *
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, current_app, jsonify, request, send_file
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

@bp.route('/image')
def serve_image():
    # Get folder and file names from query parameters
    folder_name = request.args.get('folder')
    file_name = request.args.get('file')

    # Construct the file path
    image_path = os.path.join('/home/shahzaibkhan/work/Project-Brandguard/Backend/brandguard_app/app/utils/screenshots', folder_name, file_name)

    # Sending the file in the response
    return send_file(image_path, mimetype='image/png')
    # http://localhost:5000/image?folder=www.daraz.pk%20%20-%2020240206145858&file=screenshot_20240206145915.png

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

        # Make sure the keys match the JSON you're sending
        new_image_path = data.get('new_image_path', '')
        campaign_id = data.get('campaign_id', '')

        print("Received file path:", new_image_path)

        if new_image_path and campaign_id:  # Check if both the path and campaign_id are provided
            # Validate campaign_id (optional, depending on your requirements)
            # campaign = Campaign.query.get_or_404(campaign_id)

            new_image = Images(CampaignID=campaign_id,
                               ImagePath=new_image_path)

            db.session.add(new_image)
            db.session.commit()

            # Extract the CampaignID from the new_image object
            saved_campaign_id = new_image.CampaignID

            return jsonify({"message": "Image path saved successfully", "campaign_id": saved_campaign_id})
        else:
            return jsonify({"error": "Invalid data provided"}), 400
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
                'Found_Status_Scraping': 0,  # Initialize to 0, will be calculated later
                'Screenshot_Attempts': 0,
                'Scraping_Attempts': 0
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
            campaign_data['Screenshot_Attempts'] = total_positions

            if total_positions > 0:
                campaign_data['Found_Status_Screenshot'] = round(found_positions_screenshot / total_positions * 100, 2)

            # Fetch Scrape_Image_Status for the campaign
            scrape_image_statuses = Scrape_Image_Status.query.filter_by(
                CampaignID=campaign.CampaignID).all()

            # Calculate Found_Status_Scraping as a percentage
            total_scrape_statuses = len(scrape_image_statuses)
            found_scrape_statuses = sum(
                1 for scrape_status in scrape_image_statuses if scrape_status.Found_Status == 'yes')

            if total_scrape_statuses > 0:
                campaign_data['Found_Status_Scraping'] = round(found_scrape_statuses / total_scrape_statuses * 100, 2)
            campaign_data['Scraping_Attempts'] = total_scrape_statuses

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
                'Found_Status': ad_position.Found_Status,
                'Ad_Position': ad_position.Ad_Position
            }
            screenshot_report['AdPositions'].append(screenshot_data)

        return jsonify(screenshot_report)

    except Exception as e:
        current_app.logger.error(f"Error in get_screenshot_report: {e}")
        return jsonify({"error": str(e)}), 500
