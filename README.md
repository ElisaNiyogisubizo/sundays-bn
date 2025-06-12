# Sunday's Art Hub

A Django-based API for managing an art gallery, with owner authentication and art piece management.

## Prerequisites

- Python 3.8+
- PostgreSQL
- Cloudinary account
- Git

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd sundays_art_hub
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**:
   Create a `.env` file in the project root:
   ```plaintext
   SECRET_KEY=your-django-secret-key
   DEBUG=True
   DB_NAME=sundays_art_hub
   DB_USER=postgres
   DB_PASSWORD=your-postgres-password
   DB_HOST=localhost
   DB_PORT=5432
   CLOUDINARY_CLOUD_NAME=your-cloudinary-cloud-name
   CLOUDINARY_API_KEY=your-cloudinary-api-key
   CLOUDINARY_API_SECRET=your-cloudinary-api-secret
   ```

5. **Set Up PostgreSQL**:
   Create a database named `sundays_art_hub`:
   ```bash
   psql -U postgres -c "CREATE DATABASE sundays_art_hub;"
   ```

6. **Apply Migrations**:
   ```bash
   python manage.py migrate
   ```

7. **Create Database Tables for SQLAlchemy Models**:
   Run the following in a Python shell:
   ```python
   from gallery.models import Base
   from django.db import connection
   Base.metadata.create_all(bind=connection.engine)
   ```

8. **Run the Development Server**:
   ```bash
   python manage.py runserver
   ```

9. **Access the API**:
   - Swagger UI: `http://localhost:8000/swagger/`
   - Admin Panel: `http://localhost:8000/admin/` (create a superuser with `python manage.py createsuperuser`)
   - API Endpoints:
     - Register: `POST /api/register/`
     - Login: `POST /api/login/`
     - Art Pieces: `GET/POST /api/art-pieces/`
     - Art Piece Detail: `GET/PUT/DELETE /api/art-pieces/<id>/`

## API Usage

- **Register Owner**:
  ```bash
  curl -X POST http://localhost:8000/api/register/ -d '{"username": "owner1", "email": "owner1@example.com", "password": "securepassword"}'
  ```

- **Login Owner**:
  ```bash
  curl -X POST http://localhost:8000/api/login/ -d '{"username": "owner1", "password": "securepassword"}'
  ```

- **Create Art Piece** (with token from login):
  ```bash
  curl -X POST http://localhost:8000/api/art-pieces/ -H "Authorization: Token your-token" -F "title=Artwork" -F "description=Beautiful painting" -F "price=100.00" -F "image=@/path/to/image.jpg"
  ```

- **List Art Pieces**:
  ```bash
  curl -X GET http://localhost:8000/api/art-pieces/ -H "Authorization: Token your-token"
  ```

## Notes

- Passwords are stored in plain text for simplicity. In production, use Django's `set_password` for hashing.
- Ensure Cloudinary credentials are correctly set in the `.env` file.
- Use Swagger UI for interactive API testing.