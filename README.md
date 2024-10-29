Commands:

alembic init migrations
alembic revision --autogenerate -m "Commit"
alembic upgrade head | hash

uvicorn app.main:app --reload