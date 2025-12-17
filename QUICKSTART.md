# Quick Start Guide for Hospital Management System

## Prerequisites

- Python 3.9+
- PostgreSQL 12+
- Node.js 14+ (for serverless email)
- Git

## Quick Setup (5 minutes)

### 1. Database Setup

```bash
# Open PostgreSQL
psql -U postgres

# Create database and user
CREATE DATABASE hms_db;
CREATE USER hms_user WITH PASSWORD 'hms_password';
ALTER ROLE hms_user SET client_encoding TO 'utf8';
ALTER ROLE hms_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE hms_user SET default_transaction_deferrable TO on;
ALTER ROLE hms_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE hms_db TO hms_user;
\q
```

### 2. Backend Setup

```bash
# Navigate to backend
cd hms_backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your PostgreSQL credentials

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# (Optional) Load sample data
python manage.py shell < populate_db.py
```

### 3. Start Development Server

```bash
# From hms_backend directory with venv activated
python manage.py runserver
```

Visit `http://localhost:8000/` to access the application.

## Test Users (if sample data loaded)

### Doctors
- Username: `dr_smith` | Password: `DoctorPass123`
- Username: `dr_johnson` | Password: `DoctorPass123`
- Username: `dr_brown` | Password: `DoctorPass123`

### Patients
- Username: `john_doe` | Password: `PatientPass123`
- Username: `jane_patient` | Password: `PatientPass123`

## Key URLs

| URL | Purpose |
|-----|---------|
| `http://localhost:8000/` | Login/Signup |
| `http://localhost:8000/dashboard/doctor/` | Doctor Dashboard |
| `http://localhost:8000/dashboard/patient/` | Patient Dashboard |
| `http://localhost:8000/admin/` | Django Admin (superuser) |
| `http://localhost:8000/api/` | API Endpoints |

## API Testing with cURL

### Patient Signup
```bash
curl -X POST http://localhost:8000/api/auth/patient_signup/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "securepass123",
    "first_name": "Test",
    "last_name": "User",
    "role": "patient"
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{
    "username": "testuser",
    "password": "securepass123"
  }'
```

### Get Current User
```bash
curl http://localhost:8000/api/auth/current_user/ \
  -b cookies.txt
```

## Serverless Email Setup

For email notifications setup, see `serverless_email/README.md`

```bash
cd serverless_email
npm install
cp .env.example .env
# Add Mailgun credentials to .env
serverless offline start
```

## Database Models Overview

1. **UserProfile**: Extended user with role (doctor/patient)
2. **Doctor**: Doctor details, specialization, license
3. **DoctorAvailability**: Time slots when doctors are available
4. **Appointment**: Patient appointments with doctors

## Project Structure

```
hms/
├── hms_backend/           # Django backend
│   ├── hms_project/       # Settings
│   ├── hms_app/           # Application
│   ├── templates/         # HTML templates
│   ├── manage.py
│   ├── requirements.txt
│   └── populate_db.py     # Sample data script
├── serverless_email/      # Email service
├── README.md              # Full documentation
└── quick_start.sh         # This setup script
```

## Common Issues & Solutions

### "relation \"hms_app_doctor\" does not exist"
→ Run migrations: `python manage.py migrate`

### "CORS error"
→ Check `ALLOWED_HOSTS` in `hms_project/settings.py`

### "role 'hms_user' does not exist"
→ Recreate the PostgreSQL user as shown in Database Setup

### Port 8000 already in use
→ Use different port: `python manage.py runserver 8001`

## Next Steps

1. ✅ Run the application
2. 📝 Test user registration and login
3. 👨‍⚕️ Create doctor profile and set availability
4. 👤 Create patient profile and book appointments
5. 📧 Setup Serverless email service for notifications

## Need Help?

- Check the main `README.md` for full documentation
- See `serverless_email/README.md` for email setup
- Django docs: https://docs.djangoproject.com/
- DRF docs: https://www.django-rest-framework.org/
- Serverless docs: https://www.serverless.com/framework/docs

## Production Checklist

- [ ] Set `DEBUG=False` in .env
- [ ] Generate new `DJANGO_SECRET_KEY`
- [ ] Use strong database password
- [ ] Setup HTTPS
- [ ] Configure email service (Mailgun)
- [ ] Setup logging
- [ ] Configure backups
- [ ] Use production WSGI server (Gunicorn)
- [ ] Setup monitoring

---

**Ready to build!** 🏥✨
