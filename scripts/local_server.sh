echo
echo "Running migrations"
alembic upgrade head
echo

echo
echo "Starting server"

if [ -z "$OTEL_EXPORTER_OTLP_PROTOCOL" ]
then
    echo "OTEL_EXPORTER_OTLP_PROTOCOL is not set. Starting server without opentelemetry"
    uvicorn app.app:app --host 0.0.0.0 --port 8000
else
    echo "OTEL_EXPORTER_OTLP_PROTOCOL is set. Starting server with opentelemetry"
    opentelemetry-instrument uvicorn app.app:app --host 0.0.0.0 --port 8000
fi
