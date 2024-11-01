Commands:

alembic init migrations

alembic revision --autogenerate -m "Commit"

alembic upgrade head | hash

uvicorn app.main:app --reload

uvicorn client_site.main:app --host 127.0.0.1 --port 8080

docker build -t backend-image .

docker run --rm backend-image -s -v


Deploy:

Run: ```docker compose up -d```

Bash: ```docker exec -t -i itsm-app-full-server-1 /bin/bash```
