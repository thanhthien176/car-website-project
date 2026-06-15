# Car Website

A full-featured vehicle catalog platform built with Django, Django REST Framework, HTMX, and Alpine.js.

The project provides a complete car browsing experience, including vehicle catalogs, detailed specifications, reviews, comparisons, image management, REST APIs, and an administrative dashboard.

---

## Features

### Vehicle Catalog

* Browse car brands, models, and variants
* Detailed vehicle specifications
* Brand and model pages
* Variant detail pages
* Search and filtering

### Reviews & Ratings

* User review system
* 1–5 star ratings
* Automatic average rating updates using Django signals

### Vehicle Comparison

* Compare multiple vehicle variants
* Compare specifications and safety features
* Interactive comparison interface

### REST API

Built with Django REST Framework.

Available resources:

* Brands
* Car Models
* Variants

API features:

* Filtering
* Pagination
* Search support
* JSON responses

### Media Management

* Image upload validation
* Automatic WebP conversion
* Organized upload paths
* Thumbnail support

### Admin Dashboard

Custom dashboard displaying:

* Total brands
* Total models
* Total variants
* Review statistics

### Data Import

Custom management commands for importing:

* Brands
* Vehicles

from CSV files.

---

## Architecture

The project follows a modular structure with clear separation of responsibilities.

```text
cars/
├── models.py
├── views/
├── services/
├── utils/
├── validators.py
├── signals.py
├── templates/
└── tests/

api/
└── cars/
    ├── serializers.py
    ├── views.py
    ├── filters.py
    └── urls.py
```

### Design Highlights

* Service Layer pattern
* Separate API and template-based views
* Reusable utility modules
* Signal-driven business logic
* Custom management commands
* Comprehensive automated testing

---

## Technology Stack

### Backend

* Python 3.12
* Django 6
* Django REST Framework
* django-filter

### Frontend

* HTML5
* CSS3
* HTMX
* Alpine.js

### Database

* PostgreSQL
* SQLite (development)

### Media Processing

* Pillow

### Testing

* Django Test Framework
* Pytest
* pytest-django

### Utilities

* Requests
* Django Extensions
* Python Decouple

---

## Installation

### Clone Repository

```bash
git clone https://github.com/thanhthien176/car-website-project.git
cd projectcarweb
```

### Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### Install Dependencies

Using Poetry:

```bash
poetry install
```

Or using pip:

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file:

```env
SECRET_KEY=your-secret-key
DEBUG=True

DB_NAME=car_db
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432
```

---

## Database Setup

```bash
python manage.py migrate
```

---

## Import Sample Data

```bash
python manage.py import_brands
python manage.py import_cars
```

---

## Run Development Server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

---

## API Examples

### Brands

```http
GET /api/brands/
GET /api/brands/{slug}/
```

### Car Models

```http
GET /api/cars/
GET /api/cars/{slug}/
```

### Variants

```http
GET /api/variants/
GET /api/variants/{slug}/
```

### Filtering

```http
/api/variants/?fuel_type=hybrid

/api/variants/?brand=toyota

/api/variants/?price_min=500000000

/api/variants/?price_max=1000000000
```

---

## Testing

Run all tests:

```bash
python manage.py test
```

Using pytest:

```bash
pytest
```

Run a specific test group:

```bash
pytest cars/tests/test_models
pytest cars/tests/test_api
pytest cars/tests/test_views
```

---

## Test Coverage

The project includes tests for:

* Models
* Views
* APIs
* Services
* Signals
* Validators
* Utilities

---

## Future Improvements

* User authentication
* Favorites / wishlist
* Recommendation system
* API authentication
* Performance caching
* Elasticsearch integration

---

## License

This project was built for educational and portfolio purposes.
