from datetime import datetime

from app.extensions import db, scheduler
from app.models.models import Campaigns
from app.utils.img_grabber import schedule_screenshot_capture


def check_and_update_campaign_status(app):
    with app.app_context():
        current_time = datetime.now()
        campaigns = Campaigns.query.all()

        for campaign in campaigns:
            if campaign.StartDate <= current_time <= campaign.EndDate:
                if campaign.Status == 'inactive':
                    campaign.Status = 'active'
                    db.session.commit()
                    print(campaign)
                    schedule_campaign(campaign)

            elif current_time > campaign.EndDate and campaign.Status == 'active':
                campaign.Status = 'inactive'
                db.session.commit()
                # Stop the job (Shahzaib will implement it soon)


def schedule_campaign(campaign):
    # Add the logic to schedule tasks for the campaign
    # Example: scheduling screenshot capture
    scheduler.add_job(
        schedule_screenshot_capture,
        args=[campaign.CampaignID, campaign.IntervalTime],
        trigger='interval',
        minutes=campaign.IntervalTime
    )

# # Scheduling the status check to run periodically
# scheduler.add_job(check_and_update_campaign_status, 'interval', minutes=5)
