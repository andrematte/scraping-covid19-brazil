import datetime
import pandas as pd
import random as rd
import streamlit as st
import requests, os, glob, ast, json, shutil, time

from datetime import datetime
# ------------------------------- App Functions ------------------------------ #

def app_config():
    """
    sidebar_widgets 
    Set-up widgets for the app sidebar

    Returns:
        start_date [datetime]: Date to start scraping from
        final_date [datetime]: Date to stop scraping
        df_selected [dataframe]: Cities selected for scraping
        selected_cities [string]: 
    """
    st.sidebar.title('Settings')
    
    st.sidebar.subheader('Date Range:')
    st.sidebar.write('Choose dates for 2020\n\n Equivalent data for 2019 and 2021 will also be downloaded.')
    
    # Date Settings
    start_date = st.sidebar.date_input('Start Date',
                                    value=datetime(2020, 1, 1),
                                    min_value=datetime(2020, 1, 1),
                                    max_value=datetime(2020, 12, 31))

    final_date = st.sidebar.date_input('Final Date',
                                    value=datetime(2020, 12, 31),
                                    min_value=start_date,
                                    max_value=datetime(2020, 12, 31))

    
    st.sidebar.subheader('City Select')
    
    # City Settings
    cities = ['All States', 'All Capitals', 'Select Individually']
    selected_cities = st.sidebar.selectbox('Cities', cities)
                                                  
    # Process selected cities
    df_cities = pd.read_csv('config/cities.csv').sort_values(by='uf')
        
    if selected_cities == 'All States':
        df_selected = pd.DataFrame(df_cities['uf'].unique(), columns=['Estados'])
        df_selected['Cidades'] = 'all'
        df_selected['ID'] = 'all'
        selected_cities = 'STATES'
        
    elif selected_cities == 'All Capitals':
        df_selected = df_cities[df_cities['capital'] == True][['uf', 'nome', 'city_id']]
        df_selected = df_selected.rename(columns={'uf': 'Estados', 'nome': 'Cidades', 'city_id': 'ID'})
        df_selected = df_selected.reset_index(drop=True)
        selected_cities = 'CAPITALS'

    elif selected_cities == 'Select Individually':
        selected_state = st.sidebar.selectbox('Select State:', df_cities['uf'].unique())
        
        city_list = list(df_cities[df_cities['uf'] == selected_state ]['nome'].values)
        city_list.insert(0, 'all')
        selected_city = st.sidebar.selectbox('Select City', city_list)
        
        if selected_city == 'all':
            selected_id = 'all'
        else:
            selected_id = df_cities[ df_cities['nome'] == selected_city]['city_id'].values[0]
               
        df_selected = pd.DataFrame(columns=['Estados', 'Cidades', 'ID'], index=[0])
        df_selected.iloc[0] = [selected_state, selected_city, selected_id]

        selected_cities = f"{df_selected['Estados'].values[0]}-{df_selected['Cidades'].values[0]}"  
        
    return start_date, final_date, df_selected, selected_cities

def setup_dates(start_date, final_date):
    """
    setup_scrape

    Process and returns necessary parameters for the scraping process.

    Args:
        start_date (datetime): Date to start scraping from
        final_date (datetime): Date to stop scraping

    Returns:
        dates_2020 (date_range): List of dates do scrape (2020)
        dates_2019 (date_range): List of dates do scrape (2019)
        dates_2019 (date_range): List of dates do scrape (2021)
    """
    # Process dates
    dates_2020 = pd.date_range(start_date, final_date)
    dates_2019 = pd.date_range(start_date.replace(year=2019), final_date.replace(year=2019))
    dates_2021 = pd.date_range(start_date.replace(year=2021), final_date.replace(year=2021))
        
    return dates_2020, dates_2019, dates_2021


# ---------------------------- Scraping Functions ---------------------------- #

def scrape_url(URL, headers):
    """
    scrape_url 

    Scrape chart data from a single chart in the webpage

    Args:
        URL (string): URL of the website containing the data query
        headers (dictionary): Internet browser credentials

    Returns:
        dictionary: Data collected from chart
    """
    while True:
        page = requests.get(URL, headers = headers)
        if page.status_code == 200:
            break
        else:
            print('Request Failed')
            time.sleep(2 + rd.random()*5)

    data_json = page.json()
    time.sleep(0.5 + rd.random() * 3)
    
    return data_json['chart']


# ------------------------- Post Scraping Processing ------------------------- #

def process_dataframes(chart_data, diseases, date_2019, date_2020, date_2021, dataframe_2019, dataframe_2020, dataframe_2021):
    """
    process_dataframes 

    Build and concatenate dataframes containing all data from 2019-2021 for all the diseases.

    Args:
        chart_data (dictionary): Data collected from chart
        diseases (list): List of disease names
        date_2019 (datetime): Date of the current iteration
        date_2020 (datetime): Date of the current iteration
        date_2021 (datetime): Date of the current iteration
        dataframe_2019 (dataframe): dataframe of the year
        dataframe_2020 (dataframe): dataframe of the year
        dataframe_2021 (dataframe): dataframe of the year

    Returns:
        dataframe: Dataframe containing all data
    """
    # Process dataframes
    ano_2020 = pd.DataFrame(columns = diseases)
    ano_2019 = pd.DataFrame(columns = diseases)
    ano_2021 = pd.DataFrame(columns = diseases)
    
    ano_2020 = ano_2020.append(chart_data['2020'], ignore_index=True)
    ano_2019 = ano_2019.append(chart_data['2019'], ignore_index=True)
    ano_2021 = ano_2021.append(chart_data['2021'], ignore_index=True)

    try:
        dataframe_2020.loc[f'{date_2020}'] = ano_2020.iloc[-1]
    except:
        dataframe_2020.loc[f'{date_2020}'] = 0

    try:    
        dataframe_2019.loc[f'{date_2019}'] = ano_2019.iloc[-1]
    except:
        dataframe_2019.loc[f'{date_2019}'] = 0
        
    try:    
        dataframe_2021.loc[f'{date_2021}'] = ano_2021.iloc[-1]
    except:
        dataframe_2021.loc[f'{date_2021}'] = 0
        
    dataframe_2020.fillna(0)
    dataframe_2019.fillna(0)
    dataframe_2021.fillna(0)
    
    dataframe_2020['DATA'] = pd.to_datetime(dataframe_2020.index)
    dataframe_2020 = dataframe_2020.set_index('DATA')

    dataframe_2019['DATA'] = pd.to_datetime(dataframe_2019.index)
    dataframe_2019 = dataframe_2019.set_index('DATA')
    dataframe_2019['COVID'] = 0
    
    dataframe_2021['DATA'] = pd.to_datetime(dataframe_2021.index)
    dataframe_2021 = dataframe_2021.set_index('DATA')
    
    concat = pd.concat([dataframe_2019, dataframe_2020, dataframe_2021], axis=0)
    concat = concat.rename(columns={'OUTRAS': 'DEMAIS OBITOS',
                                    'INSUFICIENCIA_RESPIRATORIA': 'INSUFICIENCIA RESPIRATORIA',
                                    'COVID': 'COVID19',
                                    'CHOQUE_CARD': 'CHOQUE CARDIOPATICO',
                                    'COVID_AVC': 'AVC (COVID)',
                                    'COVID_INFARTO': 'INFARTO (COVID)'})  
    
    concat = concat.fillna(0)
    concat = concat.sort_values(by = 'DATA')
    
    return concat

