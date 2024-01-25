from flask import render_template, request, jsonify
from app.extensions import db
from app.models.models import *
from app.main import bp
from datetime import datetime  # Corrected import statement
from app.utils.img_grabber import *

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