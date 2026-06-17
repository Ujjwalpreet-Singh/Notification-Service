# Notification Service

## Features

- User Registration/Login
- JWT Authentication
- Send notifications to other users
- Notification Inbox
- Sent Notifications
- Filtering by status/channel/title
- Docker Support
- Unit Tested

## Database

The project uses SQLAlchemy as its ORM.

By default the application is configured to use SQLite:

DATABASE_URL=sqlite:///./notifications.db

To switch to PostgreSQL or MySQL, update the DATABASE_URL and install the corresponding database driver. No application code changes are required.

## Run Locally

pip install -r requirements.txt \
uvicorn app.main:app --reload

## Run Tests

pytest

## Run Coverage

pytest --cov=app --cov-report=term-missing

## Docker

docker build -t notification-service . \
docker run -p 8000:8000 notification-service

## API Docs

http://localhost:8000/docs \
http://localhost:8000/redoc
