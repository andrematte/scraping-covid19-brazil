import pyuser_agent

pua = pyuser_agent.UA()


headers = {'User-Agent': pua.mozilla,
           'X-CSRF-TOKEN': '',
           'X-XSRF-TOKEN': ''
           }
           
