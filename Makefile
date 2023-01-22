.PHONY: help req db start

req:
        pip install -r requirements.txt
db:
        docker run --rm -it -d -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=admin -p 5432:5432 postgres
start:
        python main.py
