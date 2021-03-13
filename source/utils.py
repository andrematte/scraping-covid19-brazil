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
    """
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
                                    min_value=start_date,
                                    max_value=datetime(2020, 12, 31))

    st.sidebar.subheader('Selecione as Cidades')
    st.sidebar.write('Os dados referentes às cidades selecionadas serão baixados.')

    # City Settings
    cities = ['Todos os estados', 'Todas as capitais', 'Selecionar estado']
    selected_cities = st.sidebar.selectbox('Cidades', cities)
                                                  
    # Process selected cities
    df_cities = pd.read_csv('config/cities.csv').sort_values(by='uf')
        
    print(selected_cities)
    if selected_cities == 'Todos os estados':
        df_selected = pd.DataFrame(df_cities['uf'].unique(), columns=['Estados'])
        df_selected['Cidades'] = 'all'
        df_selected['ID'] = 'all'
        
        
    elif selected_cities == 'Todas as capitais':
        df_selected = df_cities[df_cities['capital'] == True][['uf', 'nome', 'city_id']]
        df_selected = df_selected.rename(columns={'uf': 'Estados', 'nome': 'Cidades', 'city_id': 'ID'})
        df_selected = df_selected.reset_index(drop=True)
        

    elif selected_cities == 'Selecionar estado':
        selected_state = st.sidebar.selectbox('Selecione o Estado:', df_cities['uf'].unique())
        
        city_list = list(df_cities[df_cities['uf'] == selected_state ]['nome'].values)
        city_list.insert(0, 'all')
        selected_city = st.sidebar.selectbox('Selecione a Cidade', city_list)
        
        if selected_city == 'all':
            selected_id = 'all'
        else:
            selected_id = df_cities[ df_cities['nome'] == selected_city]['city_id'].values[0]
               
        df_selected = pd.DataFrame(columns=['Estados', 'Cidades', 'ID'], index=[0])
        df_selected.iloc[0] = [selected_state, selected_city, selected_id]
    
    return start_date, final_date, df_selected

def terminal_config():
    """
    Under construction
    
    Returns:
        start_date [datetime]: Date to start scraping from
        final_date [datetime]: Date to stop scraping
        selected_cities [list]: Cities selected for scraping
    """
    return

def setup_scrape(start_date, final_date):
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
    
    
    # Path to save csv files
    data_path = f"data/PTRC_{pd.Timestamp.today().strftime('%Y-%m-%d')}/"
    
    return dates_2020, dates_2019, dates_2021, data_path








# ----------------------------- Utility Functions ---------------------------- #

def scrape_data(cities, states, headers, dates, backdates, frontdates, causes, data_path):
    '''
        Scrapes the desired data and saves on the /data directory.
    '''
    
    try:
        os.mkdir(data_path)
    except:
        pass

    for state, city in zip(states.keys(), cities.keys()):

        dataframe_2019 = pd.DataFrame(columns = causes)
        dataframe_2020 = pd.DataFrame(columns = causes)
        dataframe_2021 = pd.DataFrame(columns = causes)
        del dataframe_2019['COVID']

        print(f'Scraping {city}, {state} data.')

        for date, backdate, frontdate in zip(dates.strftime('%Y-%m-%d'), backdates.strftime('%Y-%m-%d'), frontdates.strftime('%Y-%m-%d')):

            print('Scraping the following date: ', date)
            URL = f'https://transparencia.registrocivil.org.br/api/covid-covid-registral?start_date={date}&end_date={date}&state={state}&city_id={cities[city]}&chart=chart1&places[]=HOSPITAL&places[]=DOMICILIO&places[]=VIA_PUBLICA&places[]=OUTROS&cor_pele=I&diffCity=false     ' 

            while True:
                page = requests.get(URL, headers = headers)
                if page.status_code == 200:
                    break
                else:
                    print('Request Failed')
                    time.sleep(2 + rd.random()*5)

            data_json = page.json()
            time.sleep(0.5 + rd.random() * 3)
            chart = data_json['chart']

            ano_2020 = pd.DataFrame(columns = causes)
            ano_2019 = pd.DataFrame(columns = causes)
            ano_2021 = pd.DataFrame(columns = causes)
            
            ano_2020 = ano_2020.append(chart['2020'], ignore_index=True)
            ano_2019 = ano_2019.append(chart['2019'], ignore_index=True)
            ano_2021 = ano_2021.append(chart['2021'], ignore_index=True)

            try:
                dataframe_2020.loc[f'{date}'] = ano_2020.iloc[-1]
            except:
                dataframe_2020.loc[f'{date}'] = 0

            try:    
                dataframe_2019.loc[f'{backdate}'] = ano_2019.iloc[-1]
            except:
                dataframe_2019.loc[f'{backdate}'] = 0
                
            try:    
                dataframe_2021.loc[f'{frontdate}'] = ano_2021.iloc[-1]
            except:
                dataframe_2021.loc[f'{frontdate}'] = 0


        dataframe_2020.fillna(0)
        dataframe_2019.fillna(0)
        dataframe_2021.fillna(0)

        dataframe_2020['Month'] = pd.to_datetime(dataframe_2020.index)
        dataframe_2020 = dataframe_2020.set_index('Month')

        dataframe_2019['Month'] = pd.to_datetime(dataframe_2019.index)
        dataframe_2019 = dataframe_2019.set_index('Month')
        dataframe_2019['COVID'] = 0
        
        dataframe_2021['Month'] = pd.to_datetime(dataframe_2021.index)
        dataframe_2021 = dataframe_2021.set_index('Month')

        concat = pd.concat([dataframe_2019, dataframe_2020, dataframe_2021], axis=0)
        concat = concat.rename(columns={'OUTRAS': 'DEMAIS OBITOS', 'INSUFICIENCIA_RESPIRATORIA': 'INSUFICIENCIA RESPIRATORIA', 'COVID': 'COVID19'})  
        concat.fillna(0, inplace=True)

        concat.to_csv(data_path + f'/RC_{state}_{city}.csv')

def scrape_data_cardiac(cities, states, headers, dates, backdates, causes, data_path):
    '''
        Scrapes the desired data and saves on the /data directory.
    '''
    
    try:
        os.mkdir(data_path)
    except:
        pass

    for state, city in zip(states.keys(), cities.keys()):

        dataframe_2019 = pd.DataFrame(columns = causes)
        dataframe_2020 = pd.DataFrame(columns = causes)
        del dataframe_2019['COVID']

        print(f'Scraping {city}, {state} data.')

        for date, backdate in zip(dates.strftime('%Y-%m-%d'), backdates.strftime('%Y-%m-%d')):

            print('Scraping the following date: ', date)
            URL = f'https://transparencia.registrocivil.org.br/api/covid-cardiaco?start_date={date}&end_date={date}&state={state}&city_id={cities[city]}&chart=chartCardiac1&places[]=HOSPITAL&places[]=DOMICILIO&places[]=VIA_PUBLICA&places[]=OUTROS&diffCity=false&cor_pele=I'

            while True:
                page = requests.get(URL, headers = headers)
                if page.status_code == 200:
                    break
                else:
                    print('Request Failed')
                    time.sleep(2 + rd.random()*5)

            data_json = page.json()
            time.sleep(0.5 + rd.random() * 3)
            chart = data_json['chart']           

            ano_2020 = pd.DataFrame(columns = causes)
            ano_2019 = pd.DataFrame(columns = causes)

            ano_2020 = ano_2020.append(chart['2020'], ignore_index=True)
            ano_2019 = ano_2019.append(chart['2019'], ignore_index=True)

            try:
                dataframe_2020.loc[f'{date}'] = ano_2020.iloc[-1]
            except:
                dataframe_2020.loc[f'{date}'] = 0

            try:    
                dataframe_2019.loc[f'{backdate}'] = ano_2019.iloc[-1]
            except:
                dataframe_2019.loc[f'{backdate}'] = 0


        dataframe_2020.fillna(0)
        dataframe_2019.fillna(0)

        dataframe_2020['Month'] = pd.to_datetime(dataframe_2020.index)
        dataframe_2020 = dataframe_2020.set_index('Month')

        dataframe_2019['Month'] = pd.to_datetime(dataframe_2019.index)
        dataframe_2019 = dataframe_2019.set_index('Month')
        dataframe_2019['COVID'] = 0

        #TODO Renomear colunas com underline
        concat = pd.concat([dataframe_2019, dataframe_2020], axis=0)
        concat = concat.rename(columns={'OUTRAS': 'DEMAIS OBITOS', 'INSUFICIENCIA_RESPIRATORIA': 'INSUFICIENCIA RESPIRATORIA', 'COVID': 'COVID19'})  
        concat.fillna(0, inplace=True)

        concat.to_csv(data_path + f'/RC_{state}_{city}.csv')



#TODO Erase Deprecated Functions        
def load_data():
    city_select = dict()
    cities = dict()
    states = dict()
    headers = dict()

    with open('../CitySelect.txt', 'r') as inf:
        city_select.update(ast.literal_eval(inf.read()))

    with open('../CityCodes.txt', 'r') as inf:
        data_json = json.load(inf)

    with open('../headers.txt', 'r') as inf:
        headers.update(ast.literal_eval(inf.read()))
        
    # Avoid those city IDs (temporary fix since some cities have duplicate names)
    drop_cities = ['3249']

    city_list = [value[3:] for value in city_select.values()]
    city_list.append('all')

    for x in range(0,len(data_json)):
        if data_json[x]['nome'] in city_list:

            print(f"{data_json[x]['uf']}, {data_json[x]['nome']},  {data_json[x]['city_id']}")

            if not data_json[x]['city_id'] in drop_cities:
                states[data_json[x]['uf']] = data_json[x]['nome']
                cities[data_json[x]['nome']] = data_json[x]['city_id']
        
    return city_select, cities, states, headers
