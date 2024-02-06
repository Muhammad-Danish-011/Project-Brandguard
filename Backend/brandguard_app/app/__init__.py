from app.extensions import scheduler
from app.factory import create_app
from app.utils.img_grabber import schedule_active_campaigns

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
