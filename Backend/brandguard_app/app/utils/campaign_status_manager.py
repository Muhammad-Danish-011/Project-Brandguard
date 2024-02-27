from datetime import datetime
import logging
from app.extensions import db, scheduler
from app.models.models import Campaigns
from app.utils.img_grabber import schedule_screenshot_capture

job_ids_to_remove = []

def check_and_update_campaign_status(app):
    with app.app_context():
        current_time = datetime.now()
        campaigns = Campaigns.query.all()

        for campaign in campaigns:
            if campaign.StartDate <= current_time <= campaign.EndDate:
                if campaign.Status == 'inactive':
                    # print(f"\n\n\n inactive to active camp................ {campaign}")
                    logging.info(f"inactive to active camp................ {campaign}")
                    campaign.Status = 'active'
                    db.session.commit()
                    print(campaign)
                    schedule_campaign(campaign)

            elif current_time > campaign.EndDate and campaign.Status == 'active':
                campaign.Status = 'inactive'
                db.session.commit()
                
                job_id = f"campaign_{campaign.CampaignID}"
                # print(f"\n\n\n\n\n\n\n\n\n job id.......................{job_id}..........remove")
                logging.info(f"job id.......................{job_id}..........remove")
                job_ids_to_remove.append(job_id)
                

        remove_jobs()


def schedule_campaign(campaign):
    # Add the logic to schedule tasks for the campaign
    # Example: scheduling screenshot capture
    job_id = f"campaign_{campaign.CampaignID}"
    # print(f"\n\n\n\n\n\n\n\n\n job id.......................{job_id}..........schedule")
    logging.info(f"job id.......................{job_id}..........schedule")

    scheduler.add_job(
        schedule_screenshot_capture,
        args=[campaign.CampaignID, campaign.IntervalTime],
        id=job_id,
        trigger='interval',
        minutes=campaign.IntervalTime
    )


def schedule_active_campaigns(app):
    with app.app_context():
        active_campaigns = Campaigns.query.filter_by(Status='active').all()
        for campaign in active_campaigns:
            schedule_campaign(campaign)


def remove_jobs():
    for job_id in job_ids_to_remove:
        try:
            scheduler.remove_job(job_id)
            # print(f"\n\n\nJob '{job_id}' removed")
            logging.info(f"Job '{job_id}' removed")
            job_ids_to_remove.remove(job_id)  # Remove the job ID from the list after removal
        except Exception as e:
            print(f"Error removing job '{job_id}': {e}")


# # Scheduling the status check to run periodically
# scheduler.add_job(check_and_update_campaign_status, 'interval', minutes=5)

