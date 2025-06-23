# 🍽️ Online Restaurant Ordering System

A full-stack web application built with Django that allows users to browse the restaurant menu, place delivery orders, and manage their profile. The system is built with clean architecture, asynchronous task processing (via Celery), and containerization using Docker.

---

## 🚀 Features

- ✅ User registration, login, logout
- ✅ Menu browsing for all visitors
- ✅ Authenticated users can place delivery orders
- ✅ Orders must be scheduled at least 30 minutes ahead
- ✅ Users can view and manage their profile
- ✅ Automatic background email notifications (order confirmation + late delivery)
- ✅ Responsive frontend using Bootstrap 5 and Django crispy forms
- ✅ Admin panel for staff
- ✅ Clean code structure, validation, and error handling
- ✅ Linting, static analysis, and test coverage via GitHub Actions

---

## 🧱 Project Structure
```
online-restaurant/
├── .github/workflows/
│ └── checks.yml                    # GitHub Actions CI config

├── app/
│    ├── app/                       # Django project root
│    │ ├── init.py
│    │ ├── asgi.py
│    │ ├── celery.py
│    │ ├── settings.py
│    │ ├── urls.py
│    │ └── wsgi.py
│    
│    ├── menu/                      # Menu app
│    │ ├── migrations/
│    │ ├── templates/menu
│    │ │ ├── base.html
│    │ │ ├── item_detail.html
│    │ │ └── menu_list.html
│    │ ├── tests/
│    │ │  └── test_views.py
│    │ ├── admin.py
│    │ ├── apps.py
│    │ ├── models.py
│    │ ├── urls.py
│    │ ├── views.py│    
│    
│    ├── orders/                    # Orders app
│    │ ├── migrations/
│    │ ├── templates/orders
│    │ │ ├── create_order.html
│    │ │ ├── order_list.html
│    │ │ └── order_success.html
│    │ └── tests/
│    │ │ ├── test_order_form.py
│    │ │ ├── test_tasks.py
│    │ │ └── test_views.py
│    │ ├── admin.py
│    │ ├── apps.py
│    │ ├── forms.py
│    │ ├── models.py
│    │ ├── tasks.py
│    │ ├── urls.py
│    │ ├── views.py
│    
│    ├── users/                     # Users app
│    │ ├── migrations/
│    │ ├── templates/users
│    │ │ ├── change_password.html
│    │ │ ├── change_password_done.html
│    │ │ ├── login.html
│    │ │ ├── logout.html
│    │ │ ├── profile.html
│    │ │ └── register.html
│    │ └── tests/
│    │ │ ├── test_auth.py
│    │ │ └── test_profile.py
│    │ ├── admin.py
│    │ ├── apps.py
│    │ ├── forms.py
│    │ ├── models.py
│    │ ├── urls.py
│    │ ├── views.py

├── .dockerignore                   # Files to ignore in Docker build
├── .env                            # Local environment variables
├── .env.example                    # Example env file for setup
├── .gitignore                      # Ignored files by Git
├── docker-compose.yml              # Docker Compose services definition
├── Dockerfile                      # Docker image instructions
├── lint.bat                        # Linting helper script
├── README.md                       # Project documentation
├── requirements.txt                # Base dependencies
├── requirements.dev.txt            # Dev dependencies
```
---

## ⚙️ Tech Stack

- **Backend**: Django 5.2, PostgreSQL
- **Frontend**: Django Templates, Bootstrap 5, crispy-forms
- **Async Tasks**: Celery + Redis
- **Containerization**: Docker & Docker Compose
- **Testing & CI**: Django TestCase, GitHub Actions, `flake8`, `mypy`, `isort`

---

## ✅ Prerequisites

Ensure you have the following installed:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

---

## 📦 Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/ayatsuliak/online-restaurant.git
cd online-restaurant
```
### 2. Create a `.env` file

Use `.env.example` as a template:

```bash
cp .env.example .env
```
Then, edit `.env` to set your own `SECRET_KEY`, `POSTGRES_PASSWORD`, etc.

### 3. Build and start the containers

```bash
docker-compose up --build
```

### 4. Apply database migrations and create superuser
Open another terminal and run the following commands to set up the database:
```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```
Also load sample menu items
```bash
docker-compose exec web python manage.py loaddata menu/fixtures/menu_items.json
````
Visit the app at http://localhost:8000

### 5. Access Admin Panel (optional)
Visit http://localhost:8000/admin and log in with the superuser credentials you created.

## 🔄 Background Tasks (Celery)
This project includes two Celery workers:
- `celery`: handles order confirmation emails
- `celery-beat`: runs periodic task every minute to check for overdue deliveries

No manual setup needed — both workers are configured in `docker-compose.yml`.

## 🧪 Running Tests
Covered 94% of the codebase with tests.
#### Run all tests
Open another terminal and run:
```bash
docker-compose run --rm web python manage.py test
```

#### Lint and style check
```bash
docker-compose run --rm web flake8 .
docker-compose run --rm web isort .
docker-compose run --rm web mypy .
```

## 🔁 Continuous Integration
A GitHub Actions workflow runs automatically on push:
- Generates a dummy .env file for CI
- Runs Django tests
- Lints the code with `flake8`, `isort`, and `mypy`

Config file: `.github/workflows/checks.yml`

## 👤 User Management
- Users can register with a unique email and username
- Login/logout with validation
- Profile view with update form
- Custom validations to ensure uniqueness of email/username

## 🧾 Orders
- Users can create orders from menu items
- Required delivery time must be at least 30 minutes from current time
- Invalid date/time inputs are caught and shown clearly in the form
- Order success message is displayed after valid submission

## 📨 Emails
- Upon order creation, user gets confirmation via email (console backend by default)
- Celery beat scans for overdue (not delivered) orders and sends alerts

## 🙌 Author
Made with care and attention to detail by **Andrii Yatsuliak**
