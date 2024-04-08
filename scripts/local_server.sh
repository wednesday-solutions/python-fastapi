echo
echo "Activating local python environment"
source ./venv/bin/activate
echo
echo "Local python environment activated"

echo
echo "Running migrations"
alembic upgrade head
echo

echo
echo "Starting server"
opentelemetry-instrument uvicorn app.app:app --host 0.0.0.0 --port 8000
