# Hestia App

A modern cooking application built with React, TypeScript, Tailwind CSS, FastAPI, and PostgreSQL.

## Tech Stack

- **Frontend**: React 19, TypeScript, Tailwind CSS v4, Vite
- **Backend**: FastAPI, Python 3.12, SQLAlchemy, Alembic
- **Database**: PostgreSQL 16
- **Containerization**: Docker & Docker Compose

## Prerequisites

- Docker and Docker Compose installed
- Node.js 20+ (for local development)
- Python 3.12+ (for local development)

## Getting Started

### Using Docker (Recommended)

1. Clone the repository and navigate to the project directory

2. Copy the environment file:

   ```bash
   cp backend/.env.example backend/.env
   ```

3. Start all services:

   ```bash
   docker-compose up --build
   ```

4. Access the application:
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   - Database: localhost:5432

### Local Development

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

#### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

#### Database

Make sure PostgreSQL is running and update the `DATABASE_URL` in `backend/.env`.

## Project Structure

```
surpass-cooking2/
├── frontend/          # React + TypeScript + Tailwind CSS
│   ├── src/
│   ├── public/
│   └── package.json
├── backend/           # FastAPI application
│   ├── main.py       # FastAPI app entry point
│   ├── database.py   # Database configuration
│   ├── models.py     # SQLAlchemy models
│   └── requirements.txt
└── docker-compose.yml # Docker services configuration
```

## Database Migrations

To create and run migrations:

```bash
cd backend
alembic init alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

## Environment Variables

See `backend/.env.example` for required environment variables.

## Development Tips

- The backend auto-reloads on code changes when running with `--reload`
- The frontend uses Vite's HMR for instant updates
- Database data persists in a Docker volume named `postgres_data`
