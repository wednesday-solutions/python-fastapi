

# FastAPI Template



This repository provides a template for creating and deploying a FastAPI project. Follow the steps below to set up the local environment, run the project, manage database migrations, and deploy the service on AWS ECS.

## Getting Started

### Requirements:
- Python 3.11
- Docker
- redis
- mysql

### 1. Initialize Local Environment

- To set up your local environment, run the following script:

```
./scripts/initialize-env.sh
```

This script installs the necessary dependencies and prepares the environment for running the FastAPI application on your local machine.
- Create a .env.local file with reference of .env.example
  Run following command to inject env file
  ```shell
  set -a source .env.local set +a
  ```
### 2. Run the Project
Start the project locally with the following command:

```
./scripts/local_server.sh
```

This script upgrades the database migrations using Alembic and starts the FastAPI server using Uvicorn. The server is hosted on 0.0.0.0 and port 8000, making it accessible locally.

### 3. Database Migrations
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

### 4. Deploy Service on AWS ECS
To deploy the FastAPI application on AWS ECS, use the following script:

```
./scripts/setup-ecs.sh develop
```

The setup-ecs.sh script leverages AWS Copilot to deploy the service. Provide the environment name as an argument (e.g., develop). The script creates and deploys an environment, then deploys the FastAPI service on that environment.

Note: Ensure you have AWS credentials configured and AWS Copilot installed for successful deployment.

#### New to AWS Copilot?
If you are new to AWS Copilot or you want to learn more about AWS Copilot, please refer to [this helpful article](https://www.wednesday.is/writing-tutorials/how-to-use-copilot-to-deploy-projects-on-ecs) that guides you through the process of setting up AWS Copilot locally as well as also helps you understand how you can publish and update an application using 4 simple steps.

### 5. Redis Dependency
```
docker run --name recorder-redis -p 6379:6379 -d redis:alpine
```
or add the REDIS_URL in .env.local file

### 6. Circuit breakers

## Using the Circuit Breaker for External API Calls

Our application uses a circuit breaker pattern to enhance its resilience against failures in external services. The circuit breaker prevents the application from performing operations that are likely to fail, allowing it to continue operating with degraded functionality instead of complete failure.

## How to Use

- For any external service call, wrap the call with the circuit breaker.
- The circuit breaker is configured to trip after a certain number of consecutive failures. Once tripped, it will prevent further calls to the external service for a defined period.

## Example

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

### Celery Dependencies
- Run following command to initiallize the celery worker
```shell
celery -A app.app.celery worker -l info
```
- Turn Up Celery Flower with
  ```shell
  flower --broker=${REDIS_URL}/6 --port=5555
  ```

### Running Application into Docker Container

- Create a file .env.docker with reference of .env.example
- Inject Docker environment using
  ```shell
  set -a source .env.docker set +a
- use following command to turn on the application
  ```shell
  docker compose --env-file .env.docker up
  ```
