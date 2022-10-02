FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt

RUN pip3 install -r requirements.txt

ENTRYPOINT ["streamlit", "run", "scraper-app.py", "--server.port=8888", "--server.address=0.0.0.0"]