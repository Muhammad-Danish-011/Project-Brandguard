from app.extensions import db
from app.models.models import Websites

def get_website_urls():
    websites = Websites.query.all()
    urls = [website.WebsiteURL for website in websites]
    return urls
