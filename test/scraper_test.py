import pyuser_agent
import requests


def test_request_url():
    
    pua = pyuser_agent.UA()


    headers = {'User-Agent': pua.mozilla,
               'X-CSRF-TOKEN': '',
               'X-XSRF-TOKEN': ''
            }
    
    URL = f"https://transparencia.registrocivil.org.br/api/covid-cardiaco?start_date=2019-01-01&end_date=2019-01-01&state=SP&city_id=1&chart=chartCardiac1&places[]=HOSPITAL&places[]=DOMICILIO&places[]=VIA_PUBLICA&places[]=OUTROS&diffCity=false&cor_pele=I"
    
    page = requests.get(URL, headers = headers)
    
    assert page.status_code == 200

