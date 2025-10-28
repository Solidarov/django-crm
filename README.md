# Teal CRM (Django)

## Description
Teal CRM is a lightweight CRM built with Django that helps track Leads and Clients within Teams (workspaces). Each user can sign up, manage their own records, and operate inside a Team with a selected Plan that limits how many leads/clients can be created. It’s a clean starter for learning and extending a multi-tenant CRM.

## ✨ Demo
- Live demo: https://your-demo-url.example (TBD)
- Screenshots:
  - Dashboard: docs/screenshots/dashboard.png (TBD)
  - Leads: docs/screenshots/leads.png (TBD)
  - Clients: docs/screenshots/clients.png (TBD)

## 🚀 Features
- User authentication (signup, login, logout, account) ([userprofile/urls.py](userprofile/urls.py))
- Leads: list, detail, create, edit, delete, convert to client ([lead/urls.py](lead/urls.py))
- Clients: list, detail, create, edit, delete ([client/urls.py](client/urls.py))
- Teams (workspaces) with per-user default team; Plans limiting max leads/clients ([team/models.py](team/models.py))
- Dashboard overview for leads and clients ([dashboard/views.py](dashboard/views.py))
- Admin to manage Teams and Plans ([team/admin.py](team/admin.py))
- Tailwind via CDN for simple styling ([core/templates/core/base.html](core/templates/core/base.html))

## 🛠️ Technologies Used
- Python 3.11+
- Django 5.2
- PostgreSQL
- python-decouple for environment variables
- Tailwind CSS (CDN)
- Django messages and template system

## 🏃 How to Run Locally

1) Prerequisites (Linux)
- Python 3.11+, pip, virtualenv
- PostgreSQL 14+ (or compatible)
- Git

Install PostgreSQL (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

2) Clone the repository
```bash
git clone https://github.com/Solidarov/lucid-landing-page.git
cd <your-repo>/django-crm
```

3) Create and activate a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

4) Install dependencies
```bash
pip install -r requirements.txt
```

5) Create the database and user (PostgreSQL)
```bash
sudo -u postgres psql
-- In the psql shell:
CREATE USER <your-user> WITH PASSWORD '<your-pass>';
CREATE DATABASE <your-db> OWNER <your-user>;
GRANT ALL PRIVILEGES ON DATABASE <your-db> TO <your-user>;
\q
```

6) Configure environment variables
Create a .env file in django-crm/ (same folder as crm_core/settings.py):
```env
SECRET_KEY=replace-with-a-strong-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=<your-db>
DB_USER=<your-user>
DB_PASSWORD=<your-pass>
DB_HOST=localhost
DB_PORT=5432
```

7) Apply migrations and create a superuser
```bash
python manage.py migrate
python manage.py createsuperuser
```

8) (Optional) Seed minimal business data
- Log in to the admin at http://127.0.0.1:8000/admin/
- Create at least one Plan under Team > Plans (fields: name, max_leads, max_clients, etc.)
- Sign up via the app or use your superuser to create a normal user; ensure the user’s Team has a Plan assigned (via Teams UI or Admin).

9) Run the development server
```bash
python manage.py runserver
```
Notes
- Settings use python-decouple to read environment from .env ([crm_core/settings.py](crm_core/settings.py)).
- Static assets use Tailwind via CDN; no extra build step is required for development.