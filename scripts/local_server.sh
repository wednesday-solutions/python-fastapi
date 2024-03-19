# Run migrations and start server
alembic upgrade head && uvicorn app.app:app --host 0.0.0.0 --port 8000
