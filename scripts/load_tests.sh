echo "Running load tests"
echo
locust -f loadtests --headless --users 10 --spawn-rate 1 -t 2m -H http://0.0.0.0:8000
