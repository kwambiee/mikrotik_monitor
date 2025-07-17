# Mikrotik Router Monitor

A Django-based web application for managing and monitoring Mikrotik routers. The project provides a web interface to view, add, edit, and reboot routers, as well as periodic background tasks for updating router status.

## Features

- List, add, edit, and view details of Mikrotik routers
- Filter routers by MAC address, phone number, and status
- Reboot routers via the web interface
- Periodic background tasks using Celery and Redis
- REST API endpoints (via Django REST Framework)
- Responsive Bootstrap UI

## Project Structure

- `mikrotik_monitor/` – Django project settings and configuration
- `routers/` – Django app for router management (models, views, tasks, templates)
- `templates/` – HTML templates for the web UI
- `requirements.txt` – Python dependencies

## Requirements

- Python 3.10+
- Redis (for Celery broker and result backend)
- PostgreSQL or SQLite (default: SQLite)

## Installation

1. **Clone the repository:**
   ```sh
   git clone <your-repo-url>
   cd mikrotik_monitor
   ```

2. **Create and activate a virtual environment:**
   ```sh
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   - Copy `.env.example` to `.env` and configure as needed.

5. **Apply migrations:**
   ```sh
   python manage.py migrate
   ```

6. **Create a superuser (optional, for admin access):**
   ```sh
   python manage.py createsuperuser
   ```

## Running the Application

### Start Django development server

```sh
python manage.py runserver
```

### Start Celery worker and beat

In separate terminals:

```sh
celery -A mikrotik_monitor worker --loglevel=info
celery -A mikrotik_monitor beat --loglevel=info
```

### Or use Supervisor/Procfile for production

- `Procfile` is provided for deployment with Gunicorn.
- `supervisord.conf` is provided for process management.

## Usage

- Access the web UI at [http://localhost:8000/routers/](http://localhost:8000/routers/)
- Use the navigation bar to add routers or view the list.
- Use the "Reboot" button to reboot a router.
- Edit router details as needed.

## Technologies Used

- Django 5.1
- Celery 5.5
- Redis
- Django REST Framework
- Bootstrap 5

## License

MIT License

---

**Note:** For RouterOS API integration, ensure your Mikrotik routers are accessible and credentials are correct in the router records.
