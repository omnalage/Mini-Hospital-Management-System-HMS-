hms/
│
├── 📄 README.md                          # Complete project documentation
├── 📄 QUICKSTART.md                      # 5-minute setup guide
├── 📄 API_DOCUMENTATION.md               # Full API reference with examples
├── 📄 DEPLOYMENT.md                      # Production deployment guide
├── 📄 PROJECT_SUMMARY.md                 # This project summary
├── 📄 ALL_REQUIREMENTS.txt               # All project dependencies
├── 📄 .gitignore                         # Git ignore rules
├── 🔧 quick_start.sh                     # Automated setup script
│
├── 📁 hms_backend/                       # Django Backend
│   │
│   ├── 📁 hms_project/                   # Django Project Config
│   │   ├── 📄 __init__.py
│   │   ├── 📄 settings.py                # Django settings
│   │   ├── 📄 urls.py                    # URL routing
│   │   └── 📄 wsgi.py                    # WSGI application
│   │
│   ├── 📁 hms_app/                       # Main Application
│   │   ├── 📄 __init__.py
│   │   ├── 📄 apps.py                    # App configuration
│   │   ├── 📄 models.py                  # Database models
│   │   │   ├── UserProfile (Doctor/Patient roles)
│   │   │   ├── Doctor (Profile, specialization)
│   │   │   ├── DoctorAvailability (Time slots)
│   │   │   └── Appointment (Bookings)
│   │   ├── 📄 views.py                   # API views & viewsets
│   │   │   ├── SignUpView
│   │   │   ├── DoctorViewSet
│   │   │   ├── DoctorAvailabilityViewSet
│   │   │   └── AppointmentViewSet
│   │   ├── 📄 serializers.py             # DRF serializers
│   │   ├── 📄 permissions.py             # Custom permissions
│   │   ├── 📄 admin.py                   # Django admin config
│   │   ├── 📄 template_views.py          # Template views
│   │   │
│   │   └── 📁 urls/                      # URL routing modules
│   │       ├── 📄 __init__.py
│   │       ├── 📄 auth.py                # Auth endpoints
│   │       ├── 📄 doctors.py             # Doctor endpoints
│   │       └── 📄 appointments.py        # Appointment endpoints
│   │
│   ├── 📁 templates/                     # HTML Templates
│   │   ├── 📁 auth/
│   │   │   └── 📄 login_signup.html      # Login/signup page
│   │   │       ├── Login form
│   │   │       ├── Patient signup form
│   │   │       └── Doctor signup form
│   │   │
│   │   └── 📁 dashboard/
│   │       ├── 📄 doctor.html            # Doctor dashboard
│   │       │   ├── Profile section
│   │       │   ├── Availability management
│   │       │   └── Appointments list
│   │       │
│   │       └── 📄 patient.html           # Patient dashboard
│   │           ├── Browse doctors
│   │           ├── Book appointments
│   │           └── View appointments
│   │
│   ├── 📁 static/                        # Static files (css, js)
│   │
│   ├── 📄 manage.py                      # Django management script
│   ├── 📄 requirements.txt                # Python dependencies
│   ├── 📄 .env.example                   # Environment template
│   ├── 📄 populate_db.py                 # Sample data script
│   │   └── Creates 3 doctors + 2 patients + availability slots
│   │
│   └── 📁 __pycache__/                   # Python cache
│
├── 📁 serverless_email/                  # Serverless Email Service
│   │
│   ├── 📁 handlers/                      # Lambda Functions
│   │   ├── 📄 __init__.py
│   │   ├── 📄 send_appointment_confirmation.py
│   │   │   └── Sends confirmation email via Mailgun
│   │   ├── 📄 send_reminder.py
│   │   │   └── Scheduled daily reminder (8 AM UTC)
│   │   └── 📄 send_cancellation.py
│   │       └── Sends cancellation notification
│   │
│   ├── 📄 email_templates.py             # HTML email templates
│   │   ├── appointment_confirmation_template()
│   │   ├── appointment_reminder_template()
│   │   └── appointment_cancellation_template()
│   │
│   ├── 📄 serverless.yml                 # Serverless Framework config
│   │   ├── AWS Lambda functions
│   │   ├── Environment variables
│   │   └── Scheduled events
│   │
│   ├── 📄 requirements.txt                # Python dependencies
│   │   ├── requests
│   │   ├── python-dotenv
│   │   └── requests-toolbelt
│   │
│   ├── 📄 .env.example                   # Environment template
│   ├── 📄 README.md                      # Setup guide
│   │
│   └── 📁 node_modules/                  # NPM packages (after npm install)
│
└── 📁 logs/                              # Application logs (created at runtime)

═══════════════════════════════════════════════════════════════

KEY FILES EXPLAINED:

📄 models.py
   → Defines database schema
   → 4 main models: UserProfile, Doctor, DoctorAvailability, Appointment
   → Uses Django ORM with PostgreSQL

📄 views.py
   → REST API endpoints
   → ViewSets for CRUD operations
   → Custom actions for complex operations

📄 serializers.py
   → Converts models to JSON
   → Data validation
   → Nested serialization

📄 urls/
   → Routes API endpoints
   → Modular structure (auth, doctors, appointments)

📄 login_signup.html
   → Beautiful responsive UI
   → JavaScript for form handling
   → API integration

📄 doctor.html
   → Doctor dashboard
   → Manage availability slots
   → View appointments

📄 patient.html
   → Patient dashboard
   → Browse and book doctors
   → Manage appointments

📄 serverless.yml
   → AWS Lambda configuration
   → Function definitions
   → Scheduled triggers

═══════════════════════════════════════════════════════════════

DATABASE SCHEMA:

Users (Django built-in)
│
├── UserProfile
│   ├── user → User
│   ├── role (doctor/patient)
│   ├── phone_number
│   └── timestamps
│
├── Doctor
│   ├── user → User (1:1)
│   ├── specialization
│   ├── license_number
│   ├── experience_years
│   ├── consultation_fee
│   └── is_available
│
├── DoctorAvailability
│   ├── doctor → Doctor (FK)
│   ├── day_of_week
│   ├── start_time
│   ├── end_time
│   └── is_active
│
└── Appointment
    ├── doctor → Doctor (FK)
    ├── patient → User (FK)
    ├── appointment_date
    ├── start_time
    ├── end_time
    ├── reason
    ├── status (scheduled/completed/cancelled/no_show)
    └── notes

═══════════════════════════════════════════════════════════════

API ENDPOINTS OVERVIEW:

Auth:
  POST   /api/auth/patient_signup/
  POST   /api/auth/doctor_signup/
  POST   /api/auth/login/
  POST   /api/auth/logout/
  GET    /api/auth/current_user/

Doctors:
  GET    /api/doctors/
  GET    /api/doctors/my_profile/
  GET    /api/doctors/{id}/available_slots/
  POST   /api/doctors/availability/
  PUT    /api/doctors/availability/{id}/
  DELETE /api/doctors/availability/{id}/

Appointments:
  GET    /api/appointments/
  POST   /api/appointments/book_appointment/
  POST   /api/appointments/{id}/cancel_appointment/

═══════════════════════════════════════════════════════════════

DEPENDENCIES:

Backend:
  ✓ Django==4.2.7
  ✓ djangorestframework==3.14.0
  ✓ django-cors-headers==4.3.1
  ✓ psycopg2-binary==2.9.9
  ✓ python-decouple==3.8

Serverless:
  ✓ requests==2.31.0
  ✓ python-dotenv==1.0.0

Database:
  ✓ PostgreSQL 12+

External Services:
  ✓ Mailgun (email service)
  ✓ AWS Lambda (serverless)

═══════════════════════════════════════════════════════════════

QUICK START FILES:

1. README.md
   → Full documentation, features, troubleshooting

2. QUICKSTART.md
   → Step-by-step 5-minute setup

3. API_DOCUMENTATION.md
   → Complete API reference with cURL examples

4. DEPLOYMENT.md
   → Production deployment guide (AWS, Heroku, etc.)

5. PROJECT_SUMMARY.md
   → Overview and feature list

6. populate_db.py
   → Load sample data for testing

7. quick_start.sh
   → Automated setup script

═══════════════════════════════════════════════════════════════

STATUS: ✅ PRODUCTION READY

This project is fully functional and ready to:
  ✓ Deploy to production
  ✓ Extend with new features
  ✓ Use as portfolio project
  ✓ Learn from
  ✓ Share with others

═══════════════════════════════════════════════════════════════
