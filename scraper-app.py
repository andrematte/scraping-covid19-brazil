"""
Brazilian Civil Registry Death Data Scraper Web App

Author: André Mattos - carlos.mattos@itec.ufpa.br

App to run web scraper functions using your browser.
Scrapes daily data from https://transparencia.registrocivil.org.br/registral-covid.
Need to setup headers and city selection file.
Run the app via termial by calling 'streamlit run app/scraper-app.py'.
"""
 
# ---------------------------- Importing Libraries --------------------------- #
 

import streamlit as st
import pandas as pd
import random as rd

from source.utils import *


# ----------------------------- App Configuration ---------------------------- #

title = 'Brazilian Civil Registry Scraper'
st.set_page_config(page_title=title, page_icon=":eyeglasses:")


# --------------------------------- Main App --------------------------------- #

"""
# Scraping COVID-19 Pandemic Data from the Brazilian Civil Registry Portal
[![Star](https://img.shields.io/github/stars/andrematte/scraping-covid19-brazil.svg?logo=github&style=social)](https://github.com/andrematte/scraping-covid19-brazil)

This code scrapes daily data from the Brazilian Civil Registry Transparency Portal.
Data contains the number of deaths by respiratory and cardiovascular system diseases by city/state in Brazil in 2020.
Data from 2019 is also included for comparison.
""" 
st.image('images/sample-plot-ptrc.png')
"""
## Brazilian Transparency Portal of Civil Registry

 The [Brazilian Transparency Portal of Civil Registry](https://transparencia.registrocivil.org.br/especial-covid) offers data on deaths registered due to COVID-19 
 (confirmed or suspected) and respiratory diseases, such as severe acute respiratory syndrome (SARS), pneumonia, and respiratory failure. The civil registry data 
 website is based on death certificates sent by the registry offices countrywide for deaths that take place in hospitals, residences, public roads, etc [1].
"""



# ------------------------------ Scraping Config ----------------------------- #

start_date, final_date, df_selected = app_config()
dates_2020, dates_2019, dates_2021, data_path = setup_scrape(start_date, final_date)

st.header('Selected Cities:')
st.dataframe(df_selected)