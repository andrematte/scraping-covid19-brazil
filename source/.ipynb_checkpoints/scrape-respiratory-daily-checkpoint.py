# # Web Scraping of COVID-19 Data from the Brazilian Civil Registry
# Author: André Mattos - carlos.mattos@itec.ufpa.br
# 
# 
# - Scrapes daily data from https://transparencia.registrocivil.org.br/registral-covid
# - Need to setup headers and city selection file
# 


# Importing libraries
import datetime
import pandas as pd
import random as rd
import requests, os, glob, ast, json, shutil, time

from utils import *


# Set up death causes and dates to scrape
causes = ['COVID', 'SRAG', 'PNEUMONIA', 'INSUFICIENCIA_RESPIRATORIA', 'SEPTICEMIA', 'INDETERMINADA', 'OUTRAS']

start_date = pd.Timestamp(year=2020, month=1, day=1)
end_date = pd.Timestamp.today()

dates = pd.date_range(start_date, end_date)
backdates = pd.date_range(start_date.replace(year=2019), end_date.replace(year=2019))

data_path = f"../data/Respiratory_RC_{pd.Timestamp.today().strftime('%Y-%m-%d')}/"


# Create dictionary of selected cities and their IDs (set up on CitySelect.txt)
city_select, cities, states, headers = load_data()


# Execute the web scraping function
scrape_data(cities, states, headers, dates, backdates, causes, data_path)