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
from config.headers import *

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
 website is based on death certificates sent by the registry offices countrywide for deaths that take place in hospitals, residences, public roads, etc.
"""


# ------------------------------ Scraping Config ----------------------------- #

start_date, final_date, df_selected, selection = app_config()
dates_2020, dates_2019, dates_2021 = setup_dates(start_date, final_date)

diseases = ['COVID', 'SRAG', 'PNEUMONIA', 'INSUFICIENCIA_RESPIRATORIA', 'SEPTICEMIA', "AVC", "CARDIOPATIA",  "CHOQUE_CARD", "COVID_AVC", "COVID_INFARTO", "INFARTO",  "SUBITA", 'INDETERMINADA', 'OUTRAS']
save_path = f"data/PTRC-{pd.Timestamp.today().strftime('%Y-%m-%d')}-{selection}/"

if st.sidebar.checkbox('Show Selected Cities'):
    st.sidebar.header('Selected Cities:')
    st.sidebar.dataframe(df_selected)
    

# ---------------------------- Start Web Scraping ---------------------------- #

st.header('Data Collection')
""" 
- The web scraper settings can be found on the left sidebar. 
- Press the button below when you're ready to start the process.
"""
if st.button('Start Data Collection'):
    
    st.write("Starting Web Scraping... This might take a while!" )
    
    # Create directory to save the files
    try:
        os.mkdir(save_path)
    except:
        pass
    
    # Scrape cities from df_selected one at a time
    for index, row in df_selected.iterrows():
        st.write(f"Scraping data - State: {row['Estados']} - City: {row['Cidades']}")
        progress = st.empty()
        
        # Make one dataframe for each year
        dataframe_2019 = pd.DataFrame(columns = diseases)
        dataframe_2020 = pd.DataFrame(columns = diseases)
        dataframe_2021 = pd.DataFrame(columns = diseases)
        del dataframe_2019['COVID']
        
        for date_2020, date_2019, date_2021 in zip(dates_2020.strftime('%Y-%m-%d'), dates_2019.strftime('%Y-%m-%d'), dates_2021.strftime('%Y-%m-%d')):
            progress.text(f'Scraping date: {date_2020}')
            
            # Define URL with the query
            URL = f"https://transparencia.registrocivil.org.br/api/covid-cardiaco?start_date={date_2021}&end_date={date_2021}&state={row['Estados']}&city_id={row['ID']}&chart=chartCardiac1&places[]=HOSPITAL&places[]=DOMICILIO&places[]=VIA_PUBLICA&places[]=OUTROS&diffCity=false&cor_pele=I"

            # Scrape URL and retrieve chart data
            chart_data = scrape_url(URL, headers)
            
            # Process scraped data and create dataframe
            df = process_dataframes(chart_data, diseases,
                                    date_2019, date_2020, date_2021,
                                    dataframe_2019, dataframe_2020, dataframe_2021)
        
        # Save dataframe on file_path
        df.to_csv(save_path + f"/PTRC-{row['Estados']}-{row['Cidades']}.csv")
        progress.text(f'Saved to: {save_path}')
        
    st.balloons()
    st.success('Scraping finished!')
        