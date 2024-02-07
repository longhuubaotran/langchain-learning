# python-start

-   All edit inside `src` folder will be synced to the docker container.
-   Hot reload is handled with `run-dev.sh` script.
-   Test the API by call [http://localhost:8080/](http://localhost:8080)
-   Swagger is auto generate at [http://localhost:8080/docs](http://localhost:8080/docs)

## Start up docker containers

NOTE: First run will build the images

```bash
docker compose up -d
```

## Stop docker containers

When finish development. Stop it to not conflict with other project may use the same port 8080.

```bash
docker compose down
```

## Get in to docker container

NOTE: Must start the docker container first.

```bash
docker exec -it python-start-app-1 bash
```

## Run development (inside docker container)

This will run a `uvicorn` server with hot reload.

```bash
sh run-dev.sh
```

# FAQ

## What is difference `gunicorn` and `uvicorn`?

[Stackoverflow](https://stackoverflow.com/questions/66362199/what-is-the-difference-between-uvicorn-and-gunicornuvicorn)
