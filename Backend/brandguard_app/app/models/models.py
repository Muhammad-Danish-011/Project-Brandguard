
from datetime import datetime

from app.extensions import db
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import column_property


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
    __table_args__ = (
        UniqueConstraint('CampaignName'),
    )


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


class Screenshots(db.Model):
    __tablename__ = 'screenshots'
    ScreenshotID = db.Column(db.Integer, primary_key=True)
    CampaignID = db.Column(db.Integer, ForeignKey('campaigns.CampaignID'))
    WebsiteID = db.Column(db.Integer, ForeignKey('websites.WebsiteID'))
    ImageID = db.Column(db.Integer, ForeignKey('images.ImageID'))
    Extension = db.Column(db.String)  # Add an Extension column
    Timestamp = db.Column(db.String)  # Add a Timestamp column
    FilePath = db.Column(db.String)


class AdPositions(db.Model):
    __tablename__ = 'ad_positions'
    AdPositionID = db.Column(db.Integer, primary_key=True)
    ScreenshotID = db.Column(
        db.Integer, ForeignKey('screenshots.ScreenshotID'))
    CampaignID = db.Column(db.Integer, ForeignKey(
        'campaigns.CampaignID'), nullable=False)
    Campaign = db.relationship('Campaigns', foreign_keys=[CampaignID])
    # Website = db.Column(db.String, ForeignKey('websites.WebsiteURL'), nullable=False)
    Capture_DateTime = db.Column(db.DateTime, default=datetime.now)
    Found_Status = db.Column(db.String)
    Ad_Position = db.Column(db.String)

    # Additional columns for data from related tables
    campaign_name = column_property(Campaigns.CampaignName, deferred=True)
    start_date = column_property(Campaigns.StartDate, deferred=True)
    end_date = column_property(Campaigns.EndDate, deferred=True)


class Scrape_Image_Status(db.Model):
    __tablename__ = 'scrape_image_status'
    StatusID = db.Column(db.Integer, primary_key=True)
    CampaignID = db.Column(db.Integer, ForeignKey('campaigns.CampaignID'))
    DateTime = db.Column(db.DateTime, default=datetime.now)
    Found_Status = db.Column(db.String)


class ScrapedImages(db.Model):
    __tablename__ = 'scraped_images'
    ScrapedImageID = db.Column(db.Integer, primary_key=True)
    ScreenshotID = db.Column(
        db.Integer, ForeignKey('screenshots.ScreenshotID'))
    Extension = db.Column(db.String)  # Add an Extension column
    FilePath = db.Column(db.String)

    # def generate_scraped_image_path(self):
    #     return f"{str(self.ScreenshotID.CampaignID).zfill(3)}_{str(self.ScreenshotID.ScreenshotID).zfill(3)}_scraped_{str(self.ScrapedImageID).zfill(3)}.{self.Extension}"


class URLS(db.Model):
    __tablename__ = 'urls'
    URL_id = db.Column(db.Integer, primary_key=True)
    webpage_url = db.Column(db.String)
    template_url = db.Column(db.String)
