from twilio.rest import Client
import smtplib
from email.mime.text import MIMEText

def send_email_alert(user_email, link, image_url):
    sender_email = "your_email@gmail.com"
    sender_password = "your_password"

    subject = "Face Match Found!"
    body = f"Your face was detected on this website: {link}\nImage: {image_url}"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = user_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, user_email, msg.as_string())


# Twilio credentials (Replace with your actual Twilio details)
TWILIO_SID = "AC7f48128567bf744234f2db4098e64225"
TWILIO_AUTH = "147283eafdf21388019cf8e6be32f8e8"
TWILIO_PHONE = r"+18777804236"


def send_alert(user, website):
    """
    Sends an SMS alert to the user when their face is found online.

    :param user: User object (contains phone number)
    :param website: URL where the user's face was detected
    """
    if not user.phone:
        print("User has no phone number linked. Skipping SMS alert.")
        return

    client = Client(TWILIO_SID, TWILIO_AUTH)
    message_body = f"🔔 Alert! Your face was found on {website}. Check it now!"

    try:
        message = client.messages.create(
            to=user.phone,
            from_=TWILIO_PHONE,
            body=message_body
        )
        print(f"✅ SMS sent to {user.phone}: {message.sid}")
    except Exception as e:
        print(f"❌ Failed to send SMS: {e}")
