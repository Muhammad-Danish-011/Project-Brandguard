from app.extensions import scheduler
from app.factory import create_app
from app.utils.img_grabber import schedule_active_campaigns
from app.models.models import db, Campaigns
import datetime
from datetime import timedelta

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
    except Exception as e:
        app.logger.error(f"Error occurred: {e}")

    import atexit
    atexit.register(lambda: scheduler.shutdown())

def fetch_and_update_data():
    # Fetch data from the database using your model
    campaigns = Campaigns.query.all()

    # Update data or perform any necessary operations
    for campaign in campaigns:
        # Perform your operations on each campaign
        # Example: Calculate expiration date
        expiration_date = campaign.StartDate + timedelta(days=campaign.IntervalTime)
        campaign.EndDate = expiration_date

    # Commit changes to the database
    db.session.commit()

# Add a scheduled job to fetch and update data every day at midnight
scheduler.add_job(fetch_and_update_data, 'cron', hour=0, minute=0, second=0)

if __name__ == '__main__':
    app.run(debug=True)
