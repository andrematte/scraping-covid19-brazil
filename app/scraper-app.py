"""
Brazilian Civil Registry Death Data Scraper Web App

Author: André Mattos - carlos.mattos@itec.ufpa.br

App to run web scraper functions using your browser.
Scrapes daily data from https://transparencia.registrocivil.org.br/registral-covid.
Need to setup headers and city selection file.
Run the app via termial by calling 'streamlit run app/scraper-app.py'.
"""
 
# ---------------------------- Importing Libraries --------------------------- #
 
from datetime import datetime
import streamlit as st
import pandas as pd
import random as rd

#from source.utils import *


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
st.image('./images/sample-plot-ptrc.png')
"""
## Brazilian Transparency Portal of Civil Registry

 The [Brazilian Transparency Portal of Civil Registry](https://transparencia.registrocivil.org.br/especial-covid) offers data on deaths registered due to COVID-19 
 (confirmed or suspected) and respiratory diseases, such as severe acute respiratory syndrome (SARS), pneumonia, and respiratory failure. The civil registry data 
 website is based on death certificates sent by the registry offices countrywide for deaths that take place in hospitals, residences, public roads, etc [1].
"""

# ------------------------------ Sidebar Options ----------------------------- #
st.sidebar.title('Configurações')
st.sidebar.subheader('Selecione o Período')
st.sidebar.write('O algoritmo irá baixar os dados para o período correspondente às datas abaixo.')

# Date Settings
start_date = st.sidebar.date_input('Data Inicial',
                                   value=datetime(2020, 1, 1),
                                   min_value=datetime(2020, 1, 1),
                                   max_value=datetime(2020, 12, 31))

final_date = st.sidebar.date_input('Data Final',
                                   value=datetime(2020, 12, 31),
                                   min_value=datetime(2020, 1, 1),
                                   max_value=datetime(2020, 12, 31))

dates = pd.date_range(start_date, final_date)
backdates = pd.date_range(start_date.replace(year=2019), final_date.replace(year=2019))
frontdates = pd.date_range(start_date.replace(year=2021), final_date.replace(year=2021))

st.sidebar.subheader('Selecione as Cidades')
st.sidebar.write('Os dados referentes às cidades selecionadas serão baixados.')

# City Settings
cities = ['Todos os estados', 'Todas as capitais']
selected_cities = st.sidebar.selectbox('Cidades', cities)

# Path to save csv files
data_path = f"../data/PTRC_{pd.Timestamp.today().strftime('%Y-%m-%d')}/"