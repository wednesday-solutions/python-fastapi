## Initialize local environment
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

## Redis Dependency
```
docker run --name recorder-redis -p 6379:6379 -d redis:alpine
```
or add the REDIS_URL in .env file

## Tests
run test by using the below script
```
source scripts/run_tests.sh
```
or
```
./scripts/run_tests.sh
```