# URL Shortener API

This project is a URL shortener API built with FastAPI, PostgreSQL, and Docker.

## Project Structure

The main components of the project are:

- `main.py`: Contains the FastAPI application setup, routing, and exception handlers.
- `db_base_service.py`: Defines a base service class for database operations.
- `settings.py`: Manages application settings using Pydantic.
- `docker-compose.yaml`: Defines the Docker services for the backend and database.
- `be.env` and `db.env`: Environment files for the backend and database services.
- `requirements.dev.txt`: Lists development dependencies.
- `conftest.py`: Contains pytest fixtures for testing.
- `test_urls.py`: Includes test cases for URL-related functionality.

## Setup and Installation

1. Ensure you have Docker and Docker Compose installed on your system.

2. Clone the repository and navigate to the project directory.

3. Create the necessary environment files:
   - `envs/be.env` for backend environment variables
   - `envs/db.env` for database environment variables
4. Build and run the Docker containers:
docker-compose up --build

The API will be available at `http://localhost:9000`.

## Tests
run `pip install -r requirements.txt`

run `pip install -r requirements.dev.txt`

run `pytest`

## LIVE DEMO
also available behind reverse proxy on `dolsz.codes/shortener`

for example `POST dolsz.codes/shortener/urls`