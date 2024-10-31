Commands:

alembic init migrations
alembic revision --autogenerate -m "Commit"
alembic upgrade head | hash

uvicorn app.main:app --reload
uvicorn client_site.main:app --host 127.0.0.1 --port 8080