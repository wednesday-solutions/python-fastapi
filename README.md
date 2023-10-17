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