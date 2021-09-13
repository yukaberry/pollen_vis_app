import pandas as pd
import numpy as np
import streamlit as st
import openpyxl
import requests

import matplotlib.pyplot as plt
from unicodedata import normalize

# Pollen types --------------------------------------------------------
def get_risk_level():

    allergy = pd.read_excel("data/Pollen types in German and Latin for Yuka.xlsx")
    group1 = allergy[allergy["Pollentypgruppe"]==1.0].reset_index(drop=True)
    #st.write(group1)

    # scraping a table from dwd --------------------------------------------------
    dwd_tb = pd.read_html('https://www.dwd.de/DE/leistungen/gefahrenindizespollen/erklaerungen.html;jsessionid=E201222435043CC5769939BFDB96011C.live11041?nn=16102&lsbId=463856')
    #print(f'Total tables: {len(dwd_tb)}')
    risk_level_df = dwd_tb[0]
    # print(risk_level_df)
    # print(type(risk_level_df))
    risk_level_df.to_csv('geo_data/risk_level_from_dwd.csv')

    # print(risk_level_df.iloc[0]["geringe Belastung"]) # access a cell's value
    risk_level_df["geringe Belastung"].replace(' - ', ',',regex=True, inplace=True)
    risk_level_df["hohe Belastung"].replace('Über ', '',regex=True, inplace=True)
    risk_level_df["mittlere Belastung"].replace(' - ', ',',regex=True, inplace=True)


    risk_level_df.to_csv('geo_data/risk_level_from_dwd_cleaned.csv',index=False)
    risk_level_df_new = pd.read_csv("geo_data/risk_level_from_dwd_cleaned.csv")

    print(risk_level_df_new)


# MEMO : Risk level email from barbora -----------------------------------------------------------

# Risk Level:
# Hazel (in German: Hasel, in Latin: Corylus).
# none = 0 pollen grain/m3 of air (no exposure)

# low = 1-10 (low exposure)
# medium = 11-100 (medium exposure)
# high = > 100 (high exposure)


# Alder (German: Erle, in Latin: Alnus)
# none = 0 (no exposure)
# low = 1-10 (low exposure)
# medium = 11-100 (medium exposure)
# high = > 100 (high exposure)

