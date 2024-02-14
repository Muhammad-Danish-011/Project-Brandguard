# webhooks.py
from flask import Blueprint,Flask, jsonify, request
from datetime import datetime, timedelta
from app.models.models import Campaigns
from app.extensions import  db
from flask import Flask
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

webhook_bp = Blueprint('webhooks', __name__)

# Your email configuration
smtp_server = 'smtp.gmail.com'
smtp_port = 587
sender_email = 'aqsat1506@gmail.com'
sender_password = 'wykx edvn sgkl atfj'

def send_email(sender_email, sender_password, subject, message, receiver_email, smtp_server, smtp_port):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

class WebhookHandler:
    @staticmethod
    def notify_expired_ads():
        today = datetime.now()
        expired_ads = Campaigns.query.filter(Campaigns.expiration_date <= today).all()

        notifications = []

        for ad in expired_ads:
            notifications.append(f'Ad {ad.id} has expired!')
            send_email(f'Ad {ad.id} has expired', f'Ad {ad.id} has expired!', ad.user_email)

        return notifications

    @staticmethod
    def calculate_and_update_expiration():
        today = datetime.now()
        expiring_soon_ads = Campaigns.query.filter(
            Campaigns.expiration_date > today,
            Campaigns.expiration_date <= today + timedelta(days=3)
        ).all()

        for ad in expiring_soon_ads:
            days_until_expiration = (ad.expiration_date - today).days
            ad.days_until_expiration = days_until_expiration

        db.session.commit()

    @staticmethod
    def receive_ad_tracking_data(data):
        try:
            ad_id = data.get('ID')
            expiration_date = data.get('Expiration_Date')
            user_email = data.get('UserEmail')

            if ad_id is not None and expiration_date is not None and user_email is not None:
                expiration_datetime = datetime.strptime(expiration_date, '%Y-%m-%d')
                ad = Campaigns.query.get(ad_id)

                if ad:
                    ad.expiration_date = expiration_datetime
                    ad.user_email = user_email
                    db.session.commit()
                    return jsonify({'message': f'Ad {ad_id} expiration duration saved.'}), 201
                else:
                    return jsonify({'message': f'Ad {ad_id} not found.'}), 404
            else:
                return jsonify({'message': 'Invalid data.'}), 400

        except Exception as e:
            return jsonify({'message': f'Error processing webhook: {str(e)}'}), 500

webhook_handler = WebhookHandler()

app = Flask(__name__)

@webhook_bp.route('/webhook', methods=['POST'])
def webhook_handler_route():
    webhook_data = request.json
    webhook_handler.receive_ad_tracking_data(webhook_data)
    return jsonify({'message': 'Webhook processed successfully'}), 200

@webhook_bp.route('/notify', methods=['GET'])
def check_and_send_notifications():
    notifications = webhook_handler.notify_expired_ads()
    return jsonify({'notifications': notifications}), 200

@webhook_bp.route('/check-ad-expiration', methods=['GET'])
def check_ad_expiration():
    webhook_handler.check_ad_expiration()
    return jsonify({'message': 'Expiration calculated and updated.'}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)