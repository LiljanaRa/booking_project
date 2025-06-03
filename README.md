# Booking Project Backend API

A backend system for managing rental properties, bookings, and user reviews — built with Django and Django REST Framework.

---

## Features

- User registration & JWT authentication
- Property listing & management
- Property search with filtering, sorting, and popularity tracking
- Review system (only after completed booking)
- Search & view history tracking
- Role-based permissions

## Tech Stack

- Python 3.12
- Django 5.2
- Django REST Framework
- MySQL
- Simple JWT for authentication

---

## Getting Started

### 1. Clone the repository

git clone https://github.com/LiljanaRa/booking_project.git

cd booking_project

### 2. Create and activate a virtual environment

python -m venv venv

source venv/bin/activate

### 3. Install dependencies

pip install -r requirements.txt

### 4. Apply migrations

python manage.py migrate

### 5. Create a superuser

python manage.py createsuperuser

### 6. Run the development server

python manage.py runserver
