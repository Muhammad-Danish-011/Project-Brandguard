from flask import Flask,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from datetime import datetime

from flask import jsonify

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://brandguard:brandguard@localhost:5432/brandguard_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Campaigns(db.Model):
    __tablename__ = 'campaigns'
    CampaignID = db.Column(db.Integer, primary_key=True)
    CampaignName = db.Column(db.String)
    StartDate = db.Column(db.DateTime)
    EndDate = db.Column(db.DateTime)
    IntervalTime = db.Column(db.Integer)
    Status = db.Column(db.String)

class Websites(db.Model):
    __tablename__ = 'websites'
    WebsiteID = db.Column(db.Integer, primary_key=True)
    CampaignID = db.Column(db.Integer, ForeignKey('campaigns.CampaignID'))
    WebsiteURL = db.Column(db.String)

class Images(db.Model):
    __tablename__ = 'images'
    ImageID = db.Column(db.Integer, primary_key=True)
    CampaignID = db.Column(db.Integer, ForeignKey('campaigns.CampaignID'))
    Extension = db.Column(db.String)  # Add an Extension column
    ImagePath = db.Column(db.String)

    def generate_image_path(self):
        return f"{str(self.CampaignID).zfill(3)}_{str(self.ImageID).zfill(3)}.{self.Extension}"

class Screenshots(db.Model):
    __tablename__ = 'screenshots'
    ScreenshotID = db.Column(db.Integer, primary_key=True)
    CampaignID = db.Column(db.Integer, ForeignKey('campaigns.CampaignID'))
    WebsiteID = db.Column(db.Integer, ForeignKey('websites.WebsiteID'))
    ImageID = db.Column(db.Integer, ForeignKey('images.ImageID'))
    Extension = db.Column(db.String)  # Add an Extension column
    Timestamp = db.Column(db.String)  # Add a Timestamp column
    FilePath = db.Column(db.String)

    def generate_screenshot_path(self):
        return f"{str(self.CampaignID).zfill(3)}_{str(self.ScreenshotID).zfill(3)}_{self.Timestamp}.{self.Extension}"


class AdPositions(db.Model):
    __tablename__ = 'ad_positions'
    AdPositionID = db.Column(db.Integer, primary_key=True)
    ScreenshotID = db.Column(db.Integer, ForeignKey('screenshots.ScreenshotID'))
    XCoordinate = db.Column(db.Float)
    YCoordinate = db.Column(db.Float)

class ScrapedImages(db.Model):
    __tablename__ = 'scraped_images'
    ScrapedImageID = db.Column(db.Integer, primary_key=True)
    ScreenshotID = db.Column(db.Integer, ForeignKey('screenshots.ScreenshotID'))
    Extension = db.Column(db.String)  # Add an Extension column
    FilePath = db.Column(db.String)

    def generate_scraped_image_path(self):
        return f"{str(self.ScreenshotID.CampaignID).zfill(3)}_{str(self.ScreenshotID.ScreenshotID).zfill(3)}_scraped_{str(self.ScrapedImageID).zfill(3)}.{self.Extension}"

class URLS(db.Model):
    __tablename__ = 'URLS'
    URL_id = db.Column(db.Integer,primary_key = True)
    webpage_url = db.Column(db.String)
    template_url = db.Column(db.String)


# Create a new Campaign
@app.route('/campaigns', methods=['POST'])
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
# Get all Campaigns
@app.route('/campaigns', methods=['GET'])
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
@app.route('/websites', methods=['POST'])
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
@app.route('/websites', methods=['GET'])
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



# Create an Image
@app.route('/images', methods=['POST'])
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
@app.route('/images', methods=['GET'])
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

# Create a Screenshot
@app.route('/screenshots', methods=['POST'])
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

# Get All Screenshots
@app.route('/screenshots', methods=['GET'])
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


# Create an Ad Position
@app.route('/adpositions', methods=['POST'])
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

# Get All Ad Positions
@app.route('/adpositions', methods=['GET'])
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


# Create a Scraped Image
@app.route('/scrapedimages', methods=['POST'])
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

# Get All Scraped Images
@app.route('/scrapedimages', methods=['GET'])
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

# Create a URL
@app.route('/urls', methods=['POST'])
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
@app.route('/urls', methods=['GET'])
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




if __name__ == '__main__':
    with app.app_context():
      db.create_all()
    app.run(debug=True)
