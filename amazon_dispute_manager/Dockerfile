# Dockerfile
FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y  postgresql-client gcc python3-dev musl-dev && apt-get -y install libpq-dev


COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

COPY wait-for-postgres.sh /wait-for-postgres.sh
RUN chmod +x /wait-for-postgres.sh

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "amazon_dispute_manager.wsgi:application"]
