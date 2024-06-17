# Django Company Review

## Description
Django-Company-Review - This is a Django project designed to create companies and reviews.

## Requirements
- Python 3.10
- PostgreSQL
- virtualenv

## Installation and configuration

### Step 1: Clone the repository
```bash
git clone https://github.com/Rubsun/django-company-review
cd django-company-review
```

### Step 2: Create a virtual environment and install dependencies
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r req.txt
```

### Step 3: Creating a PostgreSQL container
```bash
docker run -d --name your_name -p your_port:5432 -e POSTGRES_PASSWORD=your_password -e POSTGRES_USER=your_user -e POSTGRES_DB=your_db  postgres
```

### Step 4: Create your .env
```bash
POSTGRES_DB=your_db
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=localhost

POSTGRES_PORT=your_port
DJANGO_PORT=8000
SECRET_KEY=create_your_key
```

### Step 5: Make migrations and migrate
```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

### Step 6 Launching the Django Server
```bash
python manage.py runserver
```
