from app.extensions import scheduler
from app.factory import create_app
from app.utils.img_grabber import  capture_screenshot_by_campaignid
from app.models.models import *

app = create_app()

# Initialize and start the scheduler here
if not scheduler.running:
    scheduler.start()
    from app.utils.campaign_status_manager import \
        check_and_update_campaign_status
    scheduler.add_job(lambda: check_and_update_campaign_status(
        app), 'interval', minutes=3)

    try:
        active_campaigns = Campaigns.query.filter_by(Status='active').all()
        for campaign in active_campaigns:
            job_id = f"campaign_{campaign.CampaignID}"
            scheduler.add_job(capture_screenshot_by_campaignid,
            args=[campaign.CampaignID, campaign.IntervalTime],
            id=job_id,
            trigger='interval',
            minutes=campaign.IntervalTime
            )
            
    except Exception as e:
        app.logger.error(f"Error occurred: {e}")

    import atexit
    atexit.register(lambda: scheduler.shutdown())
