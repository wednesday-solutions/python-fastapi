# FastAPI Template

This repository provides a template for creating and deploying a FastAPI project. Follow the steps below to set up the local environment, run the project, manage database migrations, and deploy the service on AWS ECS.

## Table of Contents

- [Features](#features)
- [Getting started](#getting-started)
- [Advanced Usage](#advanced-usage)

### Features

- Python 3.11+ support
- SQLAlchemy 2.0+ support
- Asynchoronous capabilities
- Database migrations using Alembic
- Basic Authentication using JWT
- Caching using Redis
- Error reporting using Sentry
- Asynchoronous background tasks using Celery
- Test cases
- Dockerized application
- Readily available CRUD operations
- Readily available middlewares for rate limiting, request id injection etc
- Type checking using mypy
- Linting using flake8
- Formatting using black
- Code quality analysis using SonarQube
- Application monitoring using Signoz
- Feature flagging added - User can enable/disable features
- Database Monitoring using percona
- Loadtests using locust

### Getting Started

#### Requirements:
- Python 3
- Docker
- mysql

#### 1. Initialize Local Environment

- To set up your local environment, run the following script:

```
./scripts/initialize-env.sh
```

This script installs the necessary dependencies and prepares the environment for running the FastAPI application on your local machine.

Create a .env.local file with reference of .env.example
  Run following command to inject env file
  ```shell
  set -a source .env.local set +a
  ```

#### 2. Database Migrations
Create new database migrations when you make changes to your models. Use the following command:
```
alembic revision -m 'brief description of changes'
```

This command initializes a new migration script based on the changes made to your models. Provide a brief description of the changes in the migration message.

Apply the database migrations with the following command:
```
alembic upgrade head
```
This command updates the database schema to reflect the latest changes defined in the migration scripts

#### 3. Redis Dependency
```
docker run --name recorder-redis -p 6379:6379 -d redis:alpine
```
or add the REDIS_URL in .env.local file


#### 4. Celery Dependency
- Run following command to initiallize the celery worker
  ```shell
    celery -A app.app.celery worker -l info
  ```
- Turn Up Celery Flower with
  ```shell
  flower --broker=${REDIS_URL}/6 --port=5555
  ```

#### 5. Run the Project

##### Running Application Locally

```
./scripts/local_server.sh
```

This script upgrades the database migrations using Alembic and starts the FastAPI server using Uvicorn. The server is hosted on 0.0.0.0 and port 8000, making it accessible locally.

##### Running Application into Docker Container

- Create a file .env.docker with reference of .env.example
- Inject Docker environment using
  ```shell
  set -a source .env.docker set +a
- use following command to turn on the application
  ```shell
  docker compose --env-file .env.docker up
  ```


#### 6. Deploy Service on AWS ECS
To deploy the FastAPI application on AWS ECS, use the following script:

```
./scripts/setup-ecs.sh develop
```

The setup-ecs.sh script leverages AWS Copilot to deploy the service. Provide the environment name as an argument (e.g., develop). The script creates and deploys an environment, then deploys the FastAPI service on that environment.

Note: Ensure you have AWS credentials configured and AWS Copilot installed for successful deployment.

#### New to AWS Copilot?
If you are new to AWS Copilot or you want to learn more about AWS Copilot, please refer to [this helpful article](https://www.wednesday.is/writing-tutorials/how-to-use-copilot-to-deploy-projects-on-ecs) that guides you through the process of setting up AWS Copilot locally as well as also helps you understand how you can publish and update an application using 4 simple steps.


#### 7. Circuit breakers

Using the Circuit Breaker for External API Calls

Our application uses a circuit breaker pattern to enhance its resilience against failures in external services. The circuit breaker prevents the application from performing operations that are likely to fail, allowing it to continue operating with degraded functionality instead of complete failure.

How to Use?
- For any external service call, wrap the call with the circuit breaker.
- The circuit breaker is configured to trip after a certain number of consecutive failures. Once tripped, it will prevent further calls to the external service for a defined period.

Example

Here's an example of using the circuit breaker in an API route:

```
@app.get("/external-service")
async def external_service_endpoint():
    try:
        with circuit_breaker:
            result = await external_service_call()
            return {"message": result}
    except CircuitBreakerError:
        raise HTTPException(status_code=503, detail="Service temporarily unavailable")
```

### Advanced Usage

#### Using Signoz Monitoring Tool

To utilize Signoz for monitoring your applications, follow these steps:

1. **Sign Up:**
   - Go to the Signoz cloud portal [here](https://signoz.io/teams/).
   - Sign up for an account.
   - After signing up, you will receive a verification email from Signoz.

2. **Verify Email:**
   - Verify your email through the verification email sent by Signoz.

3. **Application Monitoring Setup:**
   - Once verified, log in to your Signoz account.
   - Click on "Application Monitoring".

4. **Configure Application:**
   - Select Python as the language.
   - Provide a service name.
   - Choose FastAPI as the framework.

5. **Setup Quickstart:**
   - Select your OS and architecture.
   - Choose Quickstart.
6. **Install Dependencies:**
   - Skip this step and move to next step
7. **Configure Environment Variables:**
   - In the next step, you need to update the values for the following variables in `.env.local` and `.env.docker` files:
     ```shell
     OTEL_RESOURCE_ATTRIBUTES=
     OTEL_EXPORTER_OTLP_ENDPOINT=
     OTEL_EXPORTER_OTLP_HEADERS=
     OTEL_EXPORTER_OTLP_PROTOCOL=
     ```

#### Logging with Signoz

To enable logging with Signoz, follow these steps:

1. **Open Dashboard:**
   - Log in to your Signoz dashboard.

2. **Navigate to Logs Section:**
   - Go to the logs section of your dashboard.

3. **Configure Log Sending:**
   - Click on "Sending Logs to Signoz".

4. **Follow Instructions:**
   - Follow the instructions provided to configure log sending to Signoz.

By following these steps, you can effectively set up application monitoring and logging using Signoz for your Python FastAPI applications.

#### Database Monitoring Using Percona

To monitor your database using Percona, follow these steps:

1. **Run Application Inside Docker Container:**
   - Ensure that your application is running inside a Docker container.

2. **Open Dashboard:**
   - Open your web browser and navigate to `https://localhost:443`.

3. **Login:**
   - Use the following credentials to log in:
     ```shell
     Username: admin
     Password: admin
     ```

4. **Access Settings:**
   - Once logged in, navigate to the settings section of the dashboard.

5. **Add Service:**
   - Within the settings, locate the "Add Service" option.

6. **Select MySQL:**
   - Choose MySQL as the service you want to monitor.

7. **Provide Database Details:**
   - Enter the hostname, username, password, and any other necessary environment variables required to connect to your MySQL database.

8. **Finish Configuration:**
   - Click add service.

By following these steps, you'll successfully configure Percona to monitor your MySQL database.

#### Dashboard Links
- Percona: https://localhost:443
- Flower: http://localhost:5556
- Locust UI: http://localhost:8089
- Swagger UI: http://localhost:8000


#### Useful scripts
- Tests - scripts/run_tests.sh
- Linting & Formatting - scripts/lint_and_format.sh
- Load tests - scripts/load_tests.sh (Change [locust.conf](https://docs.locust.io/en/stable/configuration.html) accordinly)
