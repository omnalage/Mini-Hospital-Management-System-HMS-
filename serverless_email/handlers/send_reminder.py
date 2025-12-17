import json
import os
import requests
from datetime import datetime, timedelta
from email_templates import appointment_reminder_template


def send_reminder(event, context):
    """
    Send appointment reminder emails
    This is triggered by a scheduled CloudWatch event
    """
    
    try:
        # Get email configuration
        mailgun_api_key = os.environ.get('MAILGUN_API_KEY')
        mailgun_domain = os.environ.get('MAILGUN_DOMAIN')
        sender_email = os.environ.get('SENDER_EMAIL', 'noreply@hms.example.com')
        
        # In a real scenario, you'd fetch upcoming appointments from your database
        # For now, this is a placeholder showing the structure
        
        # Example: Fetch appointments for tomorrow
        tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        
        # This would be replaced with actual database query
        appointments = []
        
        sent_count = 0
        for appointment in appointments:
            html_content = appointment_reminder_template(
                patient_name=appointment['patient_name'],
                doctor_name=appointment['doctor_name'],
                appointment_date=appointment['appointment_date'],
                start_time=appointment['start_time']
            )
            
            response = requests.post(
                f"https://api.mailgun.net/v3/{mailgun_domain}/messages",
                auth=("api", mailgun_api_key),
                data={
                    "from": sender_email,
                    "to": appointment['patient_email'],
                    "subject": f"Appointment Reminder - {appointment['doctor_name']}",
                    "html": html_content
                }
            )
            
            if response.status_code == 200:
                sent_count += 1
        
        return {
            'statusCode': 200,
            'body': json.dumps({'message': f'Sent {sent_count} reminder emails'})
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
