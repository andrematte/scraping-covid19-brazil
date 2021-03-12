    """
     Brazilian Civil Registry Death Data Scraper Terminal App

    Author: André Mattos - carlos.mattos@itec.ufpa.br
    
    Terminal app to run web scraper functions.
    Scrapes daily data from https://transparencia.registrocivil.org.br/registral-covid.
    Need to setup headers and city selection file.
    Run the app via termial by calling 'python scraper-terminal.py'.
    """

# ---------------------------- Importing Libraries --------------------------- #

import pandas as pd
import random as rd

from source.utils import *


    