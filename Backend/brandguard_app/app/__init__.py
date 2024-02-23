from app.extensions import scheduler
from app.factory import create_app
# from app.utils.img_grabber import schedule_active_campaigns
from app.models.models import *
from app.utils.campaign_status_manager import check_and_update_campaign_status,schedule_active_campaigns


app = create_app()

# Initialize and start the scheduler here
if not scheduler.running:
    scheduler.start()
    from app.utils.campaign_status_manager import \
        check_and_update_campaign_status
    scheduler.add_job(lambda: check_and_update_campaign_status(
        app), 'interval', minutes=3)

    try:
        schedule_active_campaigns(app)
        # active_campaigns = Campaigns.query.filter_by(Status='active').all()
        # for campaign in active_campaigns:
        #     schedule_campaign(campaign)
    except Exception as e:
        app.logger.error(f"Error occurred: {e}")

    import atexit
    atexit.register(lambda: scheduler.shutdown())
