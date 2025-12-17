import json
import os
import requests
from datetime import datetime
from email_templates import appointment_confirmation_template


def send_confirmation(event, context):
    """
    Send appointment confirmation email via Mailgun
    
    Expected request body:
    {
        "patient_email": "patient@example.com",
        "patient_name": "John Doe",
        "doctor_name": "Dr. Jane Smith",
        "appointment_date": "2024-01-15",
        "start_time": "10:00",
        "end_time": "10:30",
        "specialization": "Cardiology"
    }
    """
    
    try:
        body = json.loads(event.get('body', '{}'))
        
        # Validate required fields
        required_fields = ['patient_email', 'patient_name', 'doctor_name', 'appointment_date', 'start_time']
        for field in required_fields:
            if field not in body:
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': f'Missing required field: {field}'})
                }
        
        # Get email configuration
        mailgun_api_key = os.environ.get('MAILGUN_API_KEY')
        mailgun_domain = os.environ.get('MAILGUN_DOMAIN')
        sender_email = os.environ.get('SENDER_EMAIL', 'noreply@hms.example.com')
        
        # Prepare email content
        html_content = appointment_confirmation_template(
            patient_name=body['patient_name'],
            doctor_name=body['doctor_name'],
            appointment_date=body['appointment_date'],
            start_time=body['start_time'],
            end_time=body.get('end_time', ''),
            specialization=body.get('specialization', '')
        )
        
        # Send via Mailgun
        response = requests.post(
            f"https://api.mailgun.net/v3/{mailgun_domain}/messages",
            auth=("api", mailgun_api_key),
            data={
                "from": sender_email,
                "to": body['patient_email'],
                "subject": f"Appointment Confirmation - {body['doctor_name']}",
                "html": html_content
            }
        )
        
        if response.status_code == 200:
            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'Email sent successfully'})
            }
        else:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': 'Failed to send email'})
            }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
