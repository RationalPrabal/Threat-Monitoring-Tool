# Deployment Guide

## Docker Deployment (Recommended)

1. **Build and Run:**
   ```bash
   docker-compose up -d --build
   ```

2. **Verify Containers:**
   ```bash
   docker-compose ps
   ```

3. **Run Migrations (if not auto-run):**
   ```bash
   docker-compose exec web python manage.py migrate
   ```

4. **Create Superuser:**
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

## Traditional Deployment (Ubuntu/Linux)

1. **Install Dependencies:**
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv postgresql nginx supervisor
   ```

2. **Database Setup:**
   ```bash
   sudo -u postgres psql
   CREATE DATABASE threatmonitor;
   CREATE USER monitoring WITH PASSWORD 'choose_secure_password';
   GRANT ALL PRIVILEGES ON DATABASE threatmonitor TO monitoring;
   ```

3. **Application Setup:**
   - Clone repo and setup venv (see README).
   - Set `.env` with production settings (`DEBUG=False`).
   - Run `python manage.py collectstatic`.

4. **Gunicorn & Supervisor:**
   - Create gunicorn config or run with supervisor to keep it alive.

5. **Nginx:**
   - Configure Nginx as reverse proxy to Gunicorn (port 8000).

## Cloud Deployment (Render/Railway)

1. **Connect Repository** to Render/Railway.
2. **Add PostgreSQL Database** service.
3. **Environment Variables:**
   - `DATABASE_URL`: (internal connection string)
   - `SECRET_KEY`: (generate one)
   - `DJANGO_SETTINGS_MODULE`: `config.settings.production`
4. **Build Command:**
   `pip install -r requirements.txt && python manage.py migrate`
5. **Start Command:**
   `gunicorn config.wsgi:application`
