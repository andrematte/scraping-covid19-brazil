FROM python:latest

USER root

RUN apt-get update && apt-get upgrade -y && \
    git clone https://github.com/micasense/scraping-covid19-brazil.git 

WORKDIR /scraping-covid19-brazil/

RUN pip install -r requirements.txt

ENTRYPOINT ["streamlit", "run", "scraper-app.py"]