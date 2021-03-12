import datetime
import pandas as pd
import random as rd
import requests, os, glob, ast, json, shutil, time

# Utility Functions

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