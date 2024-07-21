# Clamor Restuarant System

The Clamor Restaurant System is designed to streamline operations and enhance customer experience at a high-volume restaurant. It integrates various functionalities to manage orders, inventory, reservations, and customer interactions efficiently.

### Installation:

Install required packages using:

```bash
pip install -r requirements.txt
```

### Usage:

Create a .env file in the root of your project
```dosini
SECRET_KEY = 'django-insecure-5#yue*5y#r=-q&c381!9nlj@=&&x9lsn_3^sa6fu5-kbe10zuk'
APP_URL = http://127.0.0.1:3000/ #Frontend url

PROD = False #True in production
AUTH =  False #True in production 
USE_S3 = False #True in production
SWAGGER = True 

# Database Details
DB_ENGINE= "django.db.backends.postgresql"
DB_USERNAME=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
DB_NAME=postgres

# AWS S3 Bucket Credentials
AWS_ACCESS_KEY_ID = 
AWS_SECRET_ACCESS_KEY = 
AWS_STORAGE_BUCKET_NAME = 
AWS_S3_REGION_NAME = 

# Email settings
EMAIL_HOST = sandbox.smtp.mailtrap.io
EMAIL_HOST_USER = user
EMAIL_HOST_PASSWORD = password
EMAIL_PORT = 587
```

### Migrate tables:

```bash
python manage.py migrtae
```


### Running the Server:

```bash
python manage.py runserver 8000
```

### API Documentation:

```bash
http://127.0.0.1:8000/
```
