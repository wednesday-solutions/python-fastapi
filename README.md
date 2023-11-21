<!-- ## Initialize local environment
```
./scripts/initialize-env.sh
```

## Run the project with docker compose
```
./scripts/local_server.sh
```

## Create migrations
```
alembic revision -m 'initialize all models'
```

## Upgrade migrations
```
alembic upgrade head
``` 

## Deploy service on AWS ECS
```
./scripts/setup-ecs.sh develop
```
The `setup-ecs.sh` script deploys the fastapi application on AWS ECS, this script internally uses AWS Copilot to deploy the service. The script requires one argument to successfully deploy the service, the argument that we pass is the environment name, the script creates and deploys an environment and deploys the service on that environment.  -->

# FastAPI Template

This repository provides a template for creating and deploying a FastAPI project. Follow the steps below to set up the local environment, run the project, manage database migrations, and deploy the service on AWS ECS.

## Getting Started

### 1. Initialize Local Environment

To set up your local environment, run the following script:

```
./scripts/initialize-env.sh
```

This script installs the necessary dependencies and prepares the environment for running the FastAPI application on your local machine.

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

