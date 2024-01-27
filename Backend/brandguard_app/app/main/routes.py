from flask import render_template, request, jsonify,current_app
from app.extensions import db
from app.models.models import *
from app.main import bp
from datetime import datetime  # Corrected import statement
from app.utils.img_grabber import *
from werkzeug.utils import secure_filename
from app.utils import img_grabber

@bp.route('/')
def index():
    return 'Welcome to Brandguard!'

@bp.route('/hello/')
def hello():
    return 'Hello, World!'

# Create a new Campaign
@bp.route('/campaigns', methods=['POST'])
def create_campaign():
    data = request.get_json()

    if 'CampaignName' not in data or 'StartDate' not in data or 'EndDate' not in data or 'IntervalTime' not in data or 'Status' not in data:
        return jsonify(message='Invalid request data'), 400

    new_campaign = Campaigns(
        CampaignName=data['CampaignName'],
        StartDate=datetime.strptime(data['StartDate'], '%Y-%m-%d %H:%M:%S'),  # Convert to datetime
        EndDate=datetime.strptime(data['EndDate'], '%Y-%m-%d %H:%M:%S'),  # Convert to datetime
        IntervalTime=data['IntervalTime'],
        Status=data['Status']
    )
    db.session.add(new_campaign)
    db.session.commit()
    return jsonify(message='Campaign created successfully'), 201

@bp.route('/campaigns', methods=['GET'])
def get_campaigns():
    campaigns = Campaigns.query.all()
    result = []
    for campaign in campaigns:
        result.append({
            'CampaignID': campaign.CampaignID,
            'CampaignName': campaign.CampaignName,
            'StartDate': campaign.StartDate,
            'EndDate': campaign.EndDate,
            'IntervalTime': campaign.IntervalTime,
            'Status': campaign.Status
        })
    return jsonify(result)




# Create a new Website
@bp.route('/websites', methods=['POST'])
def create_website():
    data = request.get_json()

    if 'CampaignID' not in data or 'WebsiteURL' not in data:
        return jsonify(message='Invalid request data'), 400

    new_website = Websites(
        CampaignID=data['CampaignID'],
        WebsiteURL=data['WebsiteURL']
    )
    db.session.add(new_website)
    db.session.commit()
    return jsonify(message='Website created successfully'), 201



# Get all Websites
@bp.route('/websites', methods=['GET'])
def get_websites():
    websites = Websites.query.all()
    result = []
    for website in websites:
        result.append({
            'WebsiteID': website.WebsiteID,
            'CampaignID': website.CampaignID,
            'WebsiteURL': website.WebsiteURL
        })
    return jsonify(result)



# # Create an Image
@bp.route('/images', methods=['POST'])
def create_image():
    data = request.get_json()
    new_image = Images(
        CampaignID=data['CampaignID'],
        Extension=data['Extension'],
        ImagePath=data['ImagePath']
    )
    db.session.add(new_image)
    db.session.commit()
    return jsonify({'message': 'Image created successfully'}), 201

# Get All Images
@bp.route('/images', methods=['GET'])
def get_images():
    images = Images.query.all()
    result = []
    for image in images:
        result.append({
            'ImageID': image.ImageID,
            'CampaignID': image.CampaignID,
            'Extension': image.Extension,
            'ImagePath': image.ImagePath
        })
    return jsonify(result)

# # Create a Screenshot
@bp.route('/screenshots', methods=['POST'])
def create_screenshot():
    data = request.get_json()
    new_screenshot = Screenshots(
        CampaignID=data['CampaignID'],
        WebsiteID=data['WebsiteID'],
        ImageID=data['ImageID'],
        Extension=data['Extension'],
        Timestamp=data['Timestamp'],
        FilePath=data['FilePath']
    )
    db.session.add(new_screenshot)
    db.session.commit()
    return jsonify({'message': 'Screenshot created successfully'}), 201

# # Get All Screenshots
@bp.route('/screenshots', methods=['GET'])
def get_screenshots():
    screenshots = Screenshots.query.all()
    result = []
    for screenshot in screenshots:
        result.append({
            'ScreenshotID': screenshot.ScreenshotID,
            'CampaignID': screenshot.CampaignID,
            'WebsiteID': screenshot.WebsiteID,
            'ImageID': screenshot.ImageID,
            'Extension': screenshot.Extension,
            'Timestamp': screenshot.Timestamp,
            'FilePath': screenshot.FilePath
        })
    return jsonify(result)


# # Create an Ad Position
@bp.route('/adpositions', methods=['POST'])
def create_ad_position():
    data = request.get_json()
    new_ad_position = AdPositions(
        ScreenshotID=data['ScreenshotID'],
        XCoordinate=data['XCoordinate'],
        YCoordinate=data['YCoordinate']
    )
    db.session.add(new_ad_position)
    db.session.commit()
    return jsonify({'message': 'Ad Position created successfully'}), 201

# # Get All Ad Positions
@bp.route('/adpositions', methods=['GET'])
def get_ad_positions():
    ad_positions = AdPositions.query.all()
    result = []
    for ad_position in ad_positions:
        result.append({
            'AdPositionID': ad_position.AdPositionID,
            'ScreenshotID': ad_position.ScreenshotID,
            'XCoordinate': ad_position.XCoordinate,
            'YCoordinate': ad_position.YCoordinate
        })
    return jsonify(result)


# # Create a Scraped Image
@bp.route('/scraped-images', methods=['POST'])
def create_scraped_image():
    data = request.get_json()
    new_scraped_image = ScrapedImages(
        ScreenshotID=data['ScreenshotID'],
        Extension=data['Extension'],
        FilePath=data['FilePath']
    )
    db.session.add(new_scraped_image)
    db.session.commit()
    return jsonify({'message': 'Scraped Image created successfully'}), 201

# # Get All Scraped Images
@bp.route('/scraped-images', methods=['GET'])
def get_scraped_images():
    scraped_images = ScrapedImages.query.all()
    result = []
    for scraped_image in scraped_images:
        result.append({
            'ScrapedImageID': scraped_image.ScrapedImageID,
            'ScreenshotID': scraped_image.ScreenshotID,
            'Extension': scraped_image.Extension,
            'FilePath': scraped_image.FilePath
        })
    return jsonify(result)

# # Create a URL
@bp.route('/urls', methods=['POST'])
def create_url():
    data = request.get_json()
    new_url = URLS(
        webpage_url=data['webpage_url'],
        template_url=data['template_url']
    )
    db.session.add(new_url)
    db.session.commit()
    return jsonify({'message': 'URL created successfully'}), 201

# Get All URLs
@bp.route('/urls', methods=['GET'])
def get_urls():
    urls = URLS.query.all()
    result = []
    for url in urls:
        result.append({
            'URL_id': url.URL_id,
            'webpage_url': url.webpage_url,
            'template_url': url.template_url
        })
    return jsonify(result)


# Define an API endpoint to capture screenshots by compainID
@bp.route('/screenshot/<int:campaignID>', methods=['GET'])
def capture_screenshot_api(campaignID):
    try:
        result = schedule_screenshot_capture(campaignID)
        return jsonify(result)
    except Exception as e:
        traceback.print_exc()  # Log the exception traceback
        return {"error": str(e)}, 500




@bp.route('/interval_time/<int:compainID>', methods=['GET'])
def interval_time(campainID):
    try:
        result = get_interval_time(campainID)
        return jsonify(result)
    except Exception as e:
        traceback.print_exc()  # Log the exception traceback
        return {"error": str(e)}, 500

@bp.route('/get_website/<int:compainID>', methods=['GET'])
def getwebsite(campainID):
    try:
        result = get_website(campainID)
        return (result)
    except Exception as e:
        traceback.print_exc()  # Log the exception traceback
        return {"error": str(e)}, 500


@bp.route('/campaign_details', methods=['POST'])
def add_campaign_details():
    try:
        # Extract data from the request JSON
        data = request.get_json()
        campaign_name = data.get('CampaignName')
        start_date = data.get('StartDate')
        end_date = data.get('EndDate')
        interval_time = data.get('IntervalTime')
        status = data.get('Status')
        websites = data.get('Websites')
        images = data.get('Images')
        # Create a new campaign and add it to the database
        # Create a new campaign without websites
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

        # Add the campaign and websites to the database
        db.session.add(new_campaign)
        db.session.add_all(website_instances)
        db.session.add_all(image_instances)

        # Commit the changes
        db.session.commit()

        return jsonify({"status": "Campaign added successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/image_position/<int:campaignID>', methods = ['GET'])
def img_position(campaignID):
    result = image_position(campaignID)
    return jsonify(result)