# HMS API Documentation

## Base URL
```
http://localhost:8000/api
```

## Authentication

All endpoints except signup and login require authentication via session cookies.

### How to Authenticate
1. Call the `/auth/login/` endpoint with credentials
2. The response includes session cookie (handled automatically by browsers)
3. Include cookies in subsequent requests

---

## Authentication Endpoints

### 1. Patient Sign Up
```
POST /auth/patient_signup/
```

**Request Body:**
```json
{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepass123",
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "9876543210",
    "role": "patient"
}
```

**Response (201 Created):**
```json
{
    "message": "Patient registered successfully",
    "user_id": 1,
    "username": "john_doe"
}
```

**Status Codes:**
- `201` - Successfully registered
- `400` - Validation error (missing fields, duplicate username/email)

---

### 2. Doctor Sign Up
```
POST /auth/doctor_signup/
```

**Request Body:**
```json
{
    "username": "dr_smith",
    "email": "dr.smith@hms.com",
    "password": "securepass123",
    "first_name": "Jane",
    "last_name": "Smith",
    "specialization": "Cardiology",
    "license_number": "LIC001",
    "experience_years": 10,
    "role": "doctor"
}
```

**Response (201 Created):**
```json
{
    "message": "Doctor registered successfully",
    "user_id": 2,
    "username": "dr_smith"
}
```

---

### 3. Login
```
POST /auth/login/
```

**Request Body:**
```json
{
    "username": "john_doe",
    "password": "securepass123"
}
```

**Response (200 OK):**
```json
{
    "message": "Login successful",
    "user_id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "role": "patient"
}
```

**Status Codes:**
- `200` - Login successful
- `401` - Invalid credentials

---

### 4. Logout
```
POST /auth/logout/
```

**Response (200 OK):**
```json
{
    "message": "Logged out successfully"
}
```

---

### 5. Get Current User
```
GET /auth/current_user/
```

**Authentication:** Required

**Response (200 OK):**
```json
{
    "user": {
        "id": 1,
        "username": "john_doe",
        "email": "john@example.com",
        "first_name": "John",
        "last_name": "Doe"
    },
    "role": "patient",
    "phone_number": "9876543210",
    "created_at": "2024-01-15T10:30:00Z"
}
```

---

## Doctor Endpoints

### 1. List All Doctors
```
GET /doctors/
```

**Authentication:** Required

**Query Parameters:**
- None

**Response (200 OK):**
```json
[
    {
        "id": 1,
        "user": {
            "id": 1,
            "username": "dr_smith",
            "email": "dr.smith@hms.com",
            "first_name": "Jane",
            "last_name": "Smith"
        },
        "specialization": "Cardiology",
        "license_number": "LIC001",
        "experience_years": 10,
        "bio": "Experienced cardiologist",
        "consultation_fee": "500.00",
        "is_available": true,
        "availability_slots": [...]
    }
]
```

**Notes:**
- Patients see all available doctors
- Doctors see only their own profile

---

### 2. Get Doctor's Profile
```
GET /doctors/my_profile/
```

**Authentication:** Required (Doctor only)

**Response (200 OK):**
```json
{
    "id": 1,
    "user": {...},
    "specialization": "Cardiology",
    "license_number": "LIC001",
    "experience_years": 10,
    "bio": "Experienced cardiologist",
    "consultation_fee": "500.00",
    "is_available": true,
    "availability_slots": [...]
}
```

**Status Codes:**
- `200` - Success
- `404` - Doctor profile not found

---

### 3. Get Doctor's Available Slots
```
GET /doctors/{doctor_id}/available_slots/
```

**Authentication:** Required

**Response (200 OK):**
```json
[
    {
        "id": 1,
        "doctor": 1,
        "day_of_week": "MON",
        "start_time": "09:00:00",
        "end_time": "12:00:00",
        "is_active": true
    },
    {
        "id": 2,
        "doctor": 1,
        "day_of_week": "MON",
        "start_time": "14:00:00",
        "end_time": "17:00:00",
        "is_active": true
    }
]
```

---

### 4. Add Availability Slot
```
POST /doctors/availability/
```

**Authentication:** Required (Doctor only)

**Request Body:**
```json
{
    "day_of_week": "MON",
    "start_time": "09:00",
    "end_time": "12:00",
    "is_active": true
}
```

**Response (201 Created):**
```json
{
    "id": 1,
    "doctor": 1,
    "day_of_week": "MON",
    "start_time": "09:00:00",
    "end_time": "12:00:00",
    "is_active": true
}
```

**Day Values:** `MON`, `TUE`, `WED`, `THU`, `FRI`, `SAT`, `SUN`

---

### 5. Update Availability Slot
```
PUT /doctors/availability/{slot_id}/
```

**Authentication:** Required (Doctor only)

**Request Body:** (any of these fields)
```json
{
    "day_of_week": "TUE",
    "start_time": "10:00",
    "end_time": "13:00",
    "is_active": false
}
```

---

### 6. Delete Availability Slot
```
DELETE /doctors/availability/{slot_id}/
```

**Authentication:** Required (Doctor only)

**Response:** `204 No Content`

---

## Appointment Endpoints

### 1. List Appointments
```
GET /appointments/
```

**Authentication:** Required

**Response (200 OK):**
```json
[
    {
        "id": 1,
        "doctor": 1,
        "doctor_name": "Dr. Jane Smith",
        "patient": 1,
        "patient_name": "John Doe",
        "appointment_date": "2024-01-20",
        "start_time": "10:00:00",
        "end_time": "10:30:00",
        "reason": "Regular checkup",
        "status": "scheduled",
        "notes": null
    }
]
```

**Notes:**
- Doctors see their booked appointments
- Patients see their booked appointments

---

### 2. Book Appointment
```
POST /appointments/book_appointment/
```

**Authentication:** Required (Patient only)

**Request Body:**
```json
{
    "doctor_id": 1,
    "appointment_date": "2024-01-20",
    "start_time": "10:00",
    "end_time": "10:30",
    "reason": "Regular checkup"
}
```

**Response (201 Created):**
```json
{
    "id": 1,
    "doctor": 1,
    "doctor_name": "Dr. Jane Smith",
    "patient": 1,
    "patient_name": "John Doe",
    "appointment_date": "2024-01-20",
    "start_time": "10:00:00",
    "end_time": "10:30:00",
    "reason": "Regular checkup",
    "status": "scheduled",
    "notes": null
}
```

**Status Codes:**
- `201` - Successfully booked
- `400` - Time slot already booked
- `404` - Doctor not found

---

### 3. Cancel Appointment
```
POST /appointments/{appointment_id}/cancel_appointment/
```

**Authentication:** Required (Patient only)

**Response (200 OK):**
```json
{
    "id": 1,
    "doctor": 1,
    "doctor_name": "Dr. Jane Smith",
    "patient": 1,
    "patient_name": "John Doe",
    "appointment_date": "2024-01-20",
    "start_time": "10:00:00",
    "end_time": "10:30:00",
    "reason": "Regular checkup",
    "status": "cancelled",
    "notes": null
}
```

**Status Codes:**
- `200` - Successfully cancelled
- `403` - Unauthorized (not appointment owner)

---

## Error Responses

### 400 Bad Request
```json
{
    "error": "Invalid request data",
    "details": {
        "field_name": ["Error message"]
    }
}
```

### 401 Unauthorized
```json
{
    "error": "Invalid username or password"
}
```

### 403 Forbidden
```json
{
    "error": "Unauthorized"
}
```

### 404 Not Found
```json
{
    "error": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
    "error": "Internal server error"
}
```

---

## Rate Limiting

Currently no rate limiting is implemented. For production, implement rate limiting:

```python
# In settings.py
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour'
    }
}
```

---

## Pagination

Pagination can be added in `settings.py`:

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}
```

---

## Testing Examples

### cURL Examples

**Patient Login:**
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{
    "username": "john_doe",
    "password": "securepass123"
  }'
```

**Get Current User:**
```bash
curl http://localhost:8000/api/auth/current_user/ \
  -b cookies.txt
```

**Book Appointment:**
```bash
curl -X POST http://localhost:8000/api/appointments/book_appointment/ \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "doctor_id": 1,
    "appointment_date": "2024-01-20",
    "start_time": "10:00",
    "end_time": "10:30",
    "reason": "Regular checkup"
  }'
```

### Python Requests Examples

```python
import requests

BASE_URL = 'http://localhost:8000/api'

# Create session to maintain cookies
session = requests.Session()

# Login
response = session.post(
    f'{BASE_URL}/auth/login/',
    json={
        'username': 'john_doe',
        'password': 'securepass123'
    }
)
print(response.json())

# Get current user
response = session.get(f'{BASE_URL}/auth/current_user/')
print(response.json())

# Book appointment
response = session.post(
    f'{BASE_URL}/appointments/book_appointment/',
    json={
        'doctor_id': 1,
        'appointment_date': '2024-01-20',
        'start_time': '10:00',
        'end_time': '10:30',
        'reason': 'Regular checkup'
    }
)
print(response.json())
```

---

## Versioning

Current API version: `v1` (implicit)

Future versions can be implemented with URL paths:
- `/api/v1/auth/login/`
- `/api/v2/auth/login/`

---

## CORS Headers

The API includes CORS headers for frontend integration:

```
Access-Control-Allow-Origin: http://localhost:3000
Access-Control-Allow-Credentials: true
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS
Access-Control-Allow-Headers: Content-Type, Authorization
```

---

## Filtering & Search

To add filtering to the API, use Django Filter Backend:

```python
# In views.py
from django_filters.rest_framework import DjangoFilterBackend

class DoctorViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['specialization', 'is_available']
```

Then query with:
```
GET /doctors/?specialization=Cardiology&is_available=true
```

---

## Additional Resources

- [Django REST Framework Documentation](https://www.django-rest-framework.org/)
- [HTTP Status Codes](https://httpwg.org/specs/rfc7231.html#status.codes)
- [JSON API Specification](https://jsonapi.org/)

