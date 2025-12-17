# Serverless Email Service for HMS

This is the serverless email notification service for the Hospital Management System. It handles appointment confirmations, reminders, and cancellations via Mailgun.

## Setup

### Prerequisites
- Node.js 14+
- Serverless Framework: `npm install -g serverless`
- AWS account with credentials configured
- Mailgun account (free tier available at https://www.mailgun.com/)

### Installation

1. Install dependencies:
```bash
npm install
npm install --save-dev serverless-offline serverless-python-requirements
```

2. Set up environment variables:
```bash
cp .env.example .env
```

3. Edit `.env` with your Mailgun credentials:
```
SENDER_EMAIL=your-email@yourdomain.com
MAILGUN_API_KEY=your_api_key
MAILGUN_DOMAIN=your.mailgun.org
```

4. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Functions

### 1. sendAppointmentConfirmation
- **Endpoint**: `POST /send-confirmation`
- **Purpose**: Send appointment confirmation emails to patients
- **Request Body**:
```json
{
    "patient_email": "patient@example.com",
    "patient_name": "John Doe",
    "doctor_name": "Dr. Jane Smith",
    "appointment_date": "2024-01-15",
    "start_time": "10:00",
    "end_time": "10:30",
    "specialization": "Cardiology"
}
```

### 2. sendReminderEmail
- **Trigger**: Scheduled daily at 8 AM UTC
- **Purpose**: Send appointment reminders to patients with appointments the next day

### 3. sendCancellationEmail
- **Endpoint**: `POST /send-cancellation`
- **Purpose**: Send appointment cancellation notices
- **Request Body**:
```json
{
    "patient_email": "patient@example.com",
    "patient_name": "John Doe",
    "doctor_name": "Dr. Jane Smith",
    "appointment_date": "2024-01-15",
    "start_time": "10:00",
    "reason": "Doctor unavailable"
}
```

## Local Development

Run the serverless offline:
```bash
serverless offline start
```

The service will be available at `http://localhost:3000`

Test the confirmation email:
```bash
curl -X POST http://localhost:3000/send-confirmation \
  -H "Content-Type: application/json" \
  -d '{
    "patient_email": "test@example.com",
    "patient_name": "John Doe",
    "doctor_name": "Dr. Jane Smith",
    "appointment_date": "2024-01-15",
    "start_time": "10:00",
    "end_time": "10:30"
  }'
```

## Deployment

Deploy to AWS:
```bash
serverless deploy
```

Deploy a specific function:
```bash
serverless deploy function -f sendAppointmentConfirmation
```

## Integration with Django Backend

From your Django backend, make HTTP requests to the serverless functions:

```python
import requests
import json

# Send confirmation email
payload = {
    "patient_email": patient.email,
    "patient_name": patient.get_full_name(),
    "doctor_name": f"Dr. {doctor.user.get_full_name()}",
    "appointment_date": appointment.appointment_date.isoformat(),
    "start_time": appointment.start_time.isoformat(),
    "end_time": appointment.end_time.isoformat(),
    "specialization": doctor.specialization
}

response = requests.post(
    'http://localhost:3000/send-confirmation',  # or your deployed endpoint
    json=payload
)
```

## Costs

- **Mailgun**: Free tier includes 5,000 emails/month
- **AWS Lambda**: Free tier includes 1,000,000 requests/month
- **CloudWatch Events**: Free for first 10 rules

Total monthly cost should be minimal for small deployments.
