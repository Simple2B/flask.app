echo Run API server
poetry run uvicorn --workers 4 --host 0.0.0.0 --port 8000 api:app
