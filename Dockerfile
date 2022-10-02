FROM python:latest

USER root

RUN git clone https://github.com/andrematte/scraping-covid19-brazil.git 

WORKDIR /scraping-covid19-brazil/

RUN pip install -r requirements.txt

ENTRYPOINT ["streamlit", "run", "scraper-app.py"]