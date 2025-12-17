# HMS Deployment Guide

This guide covers deploying the Hospital Management System to production.

## Pre-Deployment Checklist

- [ ] All tests passing
- [ ] Code reviewed
- [ ] Environment variables configured
- [ ] Database backups configured
- [ ] Email service (Mailgun) credentials set up
- [ ] HTTPS certificates ready
- [ ] Security headers configured
- [ ] Rate limiting configured
- [ ] Logging and monitoring set up

## Production Settings

### 1. Update Django Settings

Edit `hms_backend/hms_project/settings.py`:

```python
# Production settings
DEBUG = False

# Generate new secret key
SECRET_KEY = 'your-random-secret-key-here'

# Update allowed hosts
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# HTTPS settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
    }
}

# Static files
STATIC_ROOT = '/var/www/hms/static/'
STATIC_URL = '/static/'
```

### 2. Create Production .env File

```bash
# Security
DEBUG=False
DJANGO_SECRET_KEY=your-random-secret-key

# Database
DB_NAME=hms_production
DB_USER=hms_prod_user
DB_PASSWORD=strong-password-here
DB_HOST=your-rds-endpoint.amazonaws.com
DB_PORT=5432

# Email
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.mailgun.org
EMAIL_PORT=587
EMAIL_HOST_USER=postmaster@yourdomain.mailgun.org
EMAIL_HOST_PASSWORD=your-mailgun-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com

# CORS
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

## Deployment Options

### Option 1: AWS EC2 + RDS

#### 1.1 Setup EC2 Instance

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3.9 python3-pip python3-venv postgresql-client nginx gunicorn

# Clone repository
git clone https://github.com/your-repo/hms.git
cd hms/hms_backend

# Setup virtual environment
python3.9 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Create systemd service
sudo nano /etc/systemd/system/hms.service
```

#### 1.2 Create Systemd Service File

```ini
[Unit]
Description=HMS Django Application
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/hms/hms_backend
ExecStart=/home/ubuntu/hms/hms_backend/venv/bin/gunicorn \
    --workers 4 \
    --bind 127.0.0.1:8000 \
    hms_project.wsgi:application
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

#### 1.3 Configure Nginx

```bash
sudo nano /etc/nginx/sites-available/hms
```

```nginx
upstream hms_app {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    client_max_body_size 10M;

    location /static/ {
        alias /var/www/hms/static/;
    }

    location /media/ {
        alias /var/www/hms/media/;
    }

    location / {
        proxy_pass http://hms_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### 1.4 Enable Nginx Site

```bash
sudo ln -s /etc/nginx/sites-available/hms /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 1.5 Setup SSL with Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

#### 1.6 Start Services

```bash
sudo systemctl start hms
sudo systemctl enable hms
sudo systemctl start nginx
sudo systemctl enable nginx
```

### Option 2: Heroku Deployment

#### 2.1 Install Heroku CLI

```bash
curl https://cli.heroku.com/install.sh | sh
heroku login
```

#### 2.2 Create Heroku App

```bash
cd hms/hms_backend
heroku apps:create your-app-name
```

#### 2.3 Add Procfile

```bash
cat > Procfile << 'EOF'
web: gunicorn hms_project.wsgi --log-file -
EOF
```

#### 2.4 Configure Environment Variables

```bash
heroku config:set DEBUG=False
heroku config:set DJANGO_SECRET_KEY=your-secret-key
heroku config:set DB_NAME=$(heroku config:get DATABASE_URL)
# ... other environment variables
```

#### 2.5 Add PostgreSQL

```bash
heroku addons:create heroku-postgresql:standard-0
```

#### 2.6 Deploy

```bash
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

### Option 3: PythonAnywhere

1. Sign up at PythonAnywhere.com
2. Upload code via Git or web interface
3. Create virtual environment
4. Configure WSGI file
5. Set environment variables
6. Configure static files
7. Reload application

### Option 4: DigitalOcean App Platform

1. Connect GitHub repository
2. Set build command: `pip install -r requirements.txt`
3. Set run command: `gunicorn hms_project.wsgi`
4. Configure environment variables
5. Deploy

## Database Management

### Backup PostgreSQL

```bash
# Automated daily backup
pg_dump -U postgres hms_db > /backups/hms_$(date +%Y%m%d).sql

# With pgAdmin Cloud
pg_dump -U postgres hms_db | gzip > backup.sql.gz
```

### Restore PostgreSQL

```bash
psql -U postgres hms_db < /backups/hms_20240115.sql
```

### AWS RDS Backup

```bash
aws rds create-db-snapshot \
    --db-instance-identifier hms-db \
    --db-snapshot-identifier hms-db-backup-$(date +%Y%m%d)
```

## Monitoring & Logging

### Django Logging

Add to `settings.py`:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/var/log/hms/django.log',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'INFO',
    },
}
```

### Application Monitoring

**Option 1: Sentry**
```bash
pip install sentry-sdk
```

```python
# In settings.py
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="https://your-key@sentry.io/project-id",
    integrations=[DjangoIntegration()],
    traces_sample_rate=0.1,
)
```

**Option 2: New Relic**
```bash
pip install newrelic
newrelic-admin generate-config your-key newrelic.ini
```

## Security Hardening

### 1. HTTPS/TLS Configuration

```bash
# Test SSL configuration
curl -I https://yourdomain.com
```

### 2. Security Headers

```nginx
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
```

### 3. Database Security

```bash
# Enable SSL for RDS
# Configure security groups to restrict access
# Use strong passwords
# Enable database encryption at rest
```

### 4. API Rate Limiting

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

## Performance Optimization

### 1. Database Query Optimization

```python
# Use select_related() for foreign keys
doctors = Doctor.objects.select_related('user').all()

# Use prefetch_related() for reverse relations
appointments = Appointment.objects.prefetch_related('doctor__user').all()
```

### 2. Caching

```python
# In settings.py
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}

# In views
from django.views.decorators.cache import cache_page

@cache_page(60 * 5)  # Cache for 5 minutes
def list_doctors(request):
    ...
```

### 3. CDN for Static Files

Use AWS CloudFront or Cloudflare for static file delivery:

```python
# In settings.py
STATIC_URL = 'https://cdn.yourdomain.com/static/'
```

## Serverless Email Deployment

See `serverless_email/README.md` for deployment instructions.

```bash
cd serverless_email
serverless deploy
```

## Health Checks

### API Health Endpoint

Add to `urls.py`:
```python
path('health/', views.health_check, name='health'),
```

```python
# In views.py
from django.http import JsonResponse
from django.db import connection

def health_check(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        return JsonResponse({'status': 'healthy'})
    except Exception as e:
        return JsonResponse({'status': 'unhealthy', 'error': str(e)}, status=500)
```

### Configure Monitoring

```bash
# AWS CloudWatch
aws cloudwatch put-metric-alarm \
    --alarm-name hms-health-check \
    --alarm-description "HMS Application Health" \
    --metric-name HealthCheckStatus \
    --namespace AWS/ApplicationELB \
    --statistic Average \
    --period 300 \
    --evaluation-periods 2 \
    --threshold 1 \
    --comparison-operator LessThanThreshold
```

## Troubleshooting Production Issues

### 502 Bad Gateway
1. Check Gunicorn is running: `systemctl status hms`
2. Check logs: `tail -f /var/log/nginx/error.log`
3. Restart: `sudo systemctl restart hms`

### Database Connection Issues
1. Check RDS security groups
2. Verify credentials in .env
3. Test connection: `psql -h endpoint -U user -d database`

### Static Files Not Loading
1. Collect static: `python manage.py collectstatic`
2. Check Nginx configuration
3. Verify file permissions: `sudo chown -R www-data:www-data /var/www/hms/`

### High Memory Usage
1. Monitor: `htop`
2. Check Django memory leaks
3. Increase server RAM
4. Use database query optimization

## Maintenance Schedule

| Task | Frequency | Command |
|------|-----------|---------|
| Database Backup | Daily | `pg_dump ...` |
| Log Rotation | Weekly | `logrotate` |
| Security Updates | Monthly | `apt update && apt upgrade` |
| Dependency Updates | Monthly | `pip list --outdated` |
| Database Cleanup | Monthly | `python manage.py clearsessions` |
| SSL Certificate Renewal | Auto (Let's Encrypt) | `certbot renew` |
| Performance Review | Quarterly | Check logs & metrics |

## Cost Estimation

| Component | Cost |
|-----------|------|
| AWS EC2 (t3.medium) | $30/month |
| RDS PostgreSQL | $100-200/month |
| Domain | $10-15/year |
| Email (Mailgun) | $50-200/month |
| **Total** | **$180-450/month** |

---

**Happy Deploying!** 🚀

