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