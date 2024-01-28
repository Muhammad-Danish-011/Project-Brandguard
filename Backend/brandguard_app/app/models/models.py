
from app.extensions import db
from sqlalchemy import ForeignKey


class Campaigns(db.Model):
    __tablename__ = 'campaigns'
    CampaignID = db.Column(db.Integer, primary_key=True)
    CampaignName = db.Column(db.String)
    StartDate = db.Column(db.DateTime)
    EndDate = db.Column(db.DateTime)
    IntervalTime = db.Column(db.Integer)
    Status = db.Column(db.String, nullable=True)
    websites = db.relationship('Websites', backref='campaign', lazy=True)
    images = db.relationship('Images', backref='campaign', lazy=True)


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

    # def generate_image_path(self, local_directory):
    #     filename = f"{str(self.CampaignID).zfill(3)}_{str(self.ImageID).zfill(3)}.{self.Extension}"
    #     return os.path.join(local_directory, filename)


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
    ScreenshotID = db.Column(
        db.Integer, ForeignKey('screenshots.ScreenshotID'))
    XCoordinate = db.Column(db.Float)
    YCoordinate = db.Column(db.Float)


class ScrapedImages(db.Model):
    __tablename__ = 'scraped_images'
    ScrapedImageID = db.Column(db.Integer, primary_key=True)
    ScreenshotID = db.Column(
        db.Integer, ForeignKey('screenshots.ScreenshotID'))
    Extension = db.Column(db.String)  # Add an Extension column
    FilePath = db.Column(db.String)

    def generate_scraped_image_path(self):
        return f"{str(self.ScreenshotID.CampaignID).zfill(3)}_{str(self.ScreenshotID.ScreenshotID).zfill(3)}_scraped_{str(self.ScrapedImageID).zfill(3)}.{self.Extension}"


class URLS(db.Model):
    __tablename__ = 'urls'
    URL_id = db.Column(db.Integer, primary_key=True)
    webpage_url = db.Column(db.String)
    template_url = db.Column(db.String)
