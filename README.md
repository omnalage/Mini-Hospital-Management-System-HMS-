# Hospital Management System (HMS)

A mini hospital management web application built with Django and Django REST Framework. The system includes doctor availability management, patient appointment booking, and a serverless email notification service.

## Features

### Doctor Features
- Sign up and authentication
- Doctor dashboard with profile management
- Set and manage availability time slots (day of week, start/end times)
- View all booked appointments
- Mark appointment status (scheduled, completed, cancelled, no-show)

### Patient Features
- Sign up and authentication
- Patient dashboard
- Browse available doctors with specialization and experience
- View doctor availability slots
- Book appointments with doctors
- Manage their appointments (view and cancel)
- Receive email confirmations and reminders

### Serverless Email Service
- Appointment confirmation emails
- Appointment reminder emails (daily scheduled)
- Appointment cancellation notifications
- Built with Serverless Framework and Mailgun

## Tech Stack

- **Backend**: Django 4.2.7 + Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: Django session-based auth
- **API**: RESTful API with Django REST Framework
- **Email Service**: Serverless Framework with Mailgun
- **Frontend**: HTML/CSS/JavaScript (Single Page Application style)

## Project Structure

```
hms/
├── hms_backend/              # Django backend
│   ├── hms_project/          # Django project settings
│   │   ├── settings.py       # Configuration
│   │   ├── urls.py           # URL routing
│   │   └── wsgi.py           # WSGI application
│   ├── hms_app/              # Main application
│   │   ├── models.py         # Data models
│   │   ├── views.py          # API views
│   │   ├── serializers.py    # DRF serializers
│   │   ├── permissions.py    # Custom permissions
│   │   ├── urls/             # URL routing
│   │   │   ├── auth.py       # Auth endpoints
│   │   │   ├── doctors.py    # Doctor endpoints
│   │   │   └── appointments.py # Appointment endpoints
│   │   └── admin.py          # Django admin config
│   ├── templates/            # HTML templates
│   │   ├── auth/             # Login/signup pages
│   │   └── dashboard/        # Doctor and patient dashboards
│   ├── manage.py             # Django management script
│   ├── requirements.txt      # Python dependencies
│   └── .env.example          # Environment variables template
│
├── serverless_email/         # Serverless email service
│   ├── handlers/             # Lambda function handlers
│   │   ├── send_appointment_confirmation.py
│   │   ├── send_reminder.py
│   │   └── send_cancellation.py
│   ├── email_templates.py    # Email HTML templates
│   ├── serverless.yml        # Serverless framework config
│   ├── requirements.txt      # Python dependencies
│   ├── .env.example          # Environment variables template
│   └── README.md             # Serverless setup guide
│
└── .gitignore
```

## Installation & Setup

### Prerequisites
- Python 3.9+
- PostgreSQL 12+
- Node.js 14+ (for serverless)
- pip and virtualenv

### Backend Setup

1. **Create PostgreSQL Database**
```bash
# Connect to PostgreSQL
psql -U postgres

# Create database and user
CREATE DATABASE hms_db;
CREATE USER hms_user WITH PASSWORD 'your_password';
ALTER ROLE hms_user SET client_encoding TO 'utf8';
ALTER ROLE hms_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE hms_user SET default_transaction_deferrable TO on;
ALTER ROLE hms_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE hms_db TO hms_user;
\q
```

2. **Setup Python Virtual Environment**
```bash
cd hms_backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure Environment**
```bash
cp .env.example .env
# Edit .env with your database credentials
```

5. **Run Migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Create Superuser**
```bash
python manage.py createsuperuser
```

7. **Start Development Server**
```bash
python manage.py runserver
```

The backend will be available at `http://localhost:8000`

### Frontend URLs

- **Login/Signup**: `http://localhost:8000/` (or specify in urls.py)
- **Doctor Dashboard**: `http://localhost:8000/dashboard/doctor`
- **Patient Dashboard**: `http://localhost:8000/dashboard/patient`
- **Admin**: `http://localhost:8000/admin`

### Serverless Email Setup

See `serverless_email/README.md` for detailed setup instructions.

**Quick Start**:
```bash
cd serverless_email
npm install
npm install --save-dev serverless-offline serverless-python-requirements
cp .env.example .env
# Edit .env with Mailgun credentials
serverless offline start
```

## API Endpoints

### Authentication
- `POST /api/auth/patient_signup/` - Patient registration
- `POST /api/auth/doctor_signup/` - Doctor registration
- `POST /api/auth/login/` - Login
- `POST /api/auth/logout/` - Logout
- `GET /api/auth/current_user/` - Get current user info

### Doctors
- `GET /api/doctors/` - List all available doctors (for patients)
- `GET /api/doctors/my_profile/` - Get own doctor profile (for doctors)
- `GET /api/doctors/{id}/available_slots/` - Get doctor's available slots
- `POST /api/doctors/availability/` - Add availability slot (doctor only)
- `PUT /api/doctors/availability/{id}/` - Update availability slot
- `DELETE /api/doctors/availability/{id}/` - Delete availability slot

### Appointments
- `GET /api/appointments/` - List user's appointments
- `POST /api/appointments/book_appointment/` - Book an appointment
- `POST /api/appointments/{id}/cancel_appointment/` - Cancel appointment

## Database Models

### UserProfile
- Extended user profile with role (Doctor/Patient)
- Phone number, created/updated timestamps

### Doctor
- User reference
- Specialization, license number
- Years of experience
- Consultation fee
- Availability status

### DoctorAvailability
- Doctor reference
- Day of week (MON-SUN)
- Start and end time
- Active status

### Appointment
- Doctor and patient references
- Appointment date and time
- Reason for visit
- Status (scheduled, completed, cancelled, no_show)
- Notes

## Workflow Examples

### Patient Booking an Appointment

1. Patient logs in to their dashboard
2. Searches and views available doctors
3. Clicks "Book Now" on a doctor
4. Selects an available time slot
5. Provides reason for visit
6. Confirms booking
7. Receives confirmation email

### Doctor Managing Availability

1. Doctor logs in to their dashboard
2. Clicks "Add Time Slot"
3. Selects day of week and time
4. Saves availability
5. Can edit or delete slots as needed

## Email Notifications

### Confirmation Email
Sent when patient books an appointment with:
- Doctor name and specialization
- Appointment date and time
- Request to arrive 10 minutes early

### Reminder Email
Sent daily at 8 AM for appointments scheduled for the next day

### Cancellation Email
Sent when appointment is cancelled with:
- Original appointment details
- Cancellation reason

## Security Considerations

1. **Authentication**: Session-based authentication with Django
2. **Authorization**: Role-based access control
3. **CSRF Protection**: Django CSRF middleware enabled
4. **CORS**: Configured for trusted origins only
5. **Password Security**: Django's built-in password validators
6. **SQL Injection**: Protected by Django ORM
7. **XSS Protection**: Django template escaping

## Development Tips

### Testing with cURL

```bash
# Patient signup
curl -X POST http://localhost:8000/api/auth/patient_signup/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepass123",
    "first_name": "John",
    "last_name": "Doe",
    "role": "patient"
  }'

# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "john_doe", "password": "securepass123"}' \
  -c cookies.txt

# Get current user
curl http://localhost:8000/api/auth/current_user/ \
  -b cookies.txt
```

### Admin Dashboard

Access Django admin at `http://localhost:8000/admin` with superuser credentials to:
- Manage users and profiles
- View and edit doctor information
- View and manage appointments
- Add test data

## Deployment

### Backend Deployment (Django)
- Use Gunicorn as WSGI server
- Deploy to AWS EC2, Heroku, PythonAnywhere, etc.
- Use environment variables for sensitive data
- Set `DEBUG=False` in production

### Serverless Deployment (Email Service)
```bash
cd serverless_email
serverless deploy
```

### Database
- Use managed PostgreSQL service (RDS, Heroku Postgres, etc.)
- Set strong passwords
- Enable backups
- Configure security groups

## Costs

- **PostgreSQL**: ~$50-200/month for managed service
- **Django Hosting**: $20-100+/month (depends on platform)
- **Serverless Email**: Free tier (Mailgun) + AWS Lambda free tier
- **Total**: Minimal for small deployments

## Troubleshooting

### Database Connection Error
```bash
# Check PostgreSQL is running
psql -U postgres

# Reset migrations if needed
python manage.py migrate zero hms_app
python manage.py makemigrations
python manage.py migrate
```

### Migration Issues
```bash
# Show migration history
python manage.py showmigrations

# Revert to specific migration
python manage.py migrate hms_app 0001
```

### CORS Issues
Update `CORS_ALLOWED_ORIGINS` in `settings.py` to include your frontend URL

### Email Not Sending
- Check Mailgun credentials in `.env`
- Verify Mailgun domain configuration
- Check Mailgun logs for errors

## Future Enhancements

- [ ] Video consultation integration
- [ ] Prescription management
- [ ] Medical records storage
- [ ] Patient health analytics
- [ ] SMS notifications
- [ ] Payment integration
- [ ] Insurance verification
- [ ] Telemedicine features
- [ ] Mobile app (React Native)
- [ ] Advanced search and filtering

## License

MIT License - feel free to use for personal and educational purposes.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review Django and DRF documentation
3. Check Serverless Framework docs
4. Open an issue in the repository

## Contributors

- Built as a mini project for hospital management system

---

**Happy Coding!** 🏥✨
