import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import datetime
from datetime import date
import os



from utils import find_pollencount_by_date
from utils import clean_df_dt,add_german_cl, add_latin_cl,choose_pollenype,choose_pollenstation
#from risk_level import get_risk_level
import risk_level

def app():
    # load csv file ---------------------------------------------------------------------
    # alnu20 = pd.read_csv("to_bin/alnu20.csv")
    # st.write(alnu20)
    # # convert data type to datetime 
    # alnu20['Date'] = pd.to_datetime(alnu20['Date'],dayfirst=True)

    if 'new_main_data.csv' not in os.listdir('geo_data'):
        st.markdown("Please upload data through `Upload Data` page!")
    else:
        # df_analysis = pd.read_csv('data/2015.csv')
        df = pd.read_csv('geo_data/new_main_data.csv')
        
        df = clean_df_dt(df)
        #df['Date'] = pd.to_datetime(df['Date'],format='%Y-%m-%d').dt.date
        df["german_name"] = df.apply(lambda df:add_german_cl(df),axis=1)
        df["latin_name"] = df.apply(lambda df:add_latin_cl(df),axis=1)

        pollen_types = df['latin_name'].unique()
        pollen_selected = st.sidebar.multiselect('Select a pollen type (latin name)', pollen_types)
        # Sort dataframe based on user's selection of pollentype
        df= choose_pollenype(df, "latin_name", pollen_selected)


        pollen_stations = df["Pollenstation"].unique()
        station_selected = st.sidebar.multiselect('Select a pollen station', pollen_stations)
        df= choose_pollenstation(df, "Pollenstation", station_selected)

        st.write(df)







        # Wedget ------------------------------------------------------------------------------
        # Set a default date as 2020, 10th Feb (datetime type) 
        today = date(2020, 2, 10)
        # Choose a date from Calendar
        date_picked = st.sidebar.date_input('Choose a date', today)
        # convert date_picked datatype to datetime
        date_picked =  date_picked.strftime("%Y/%m/%d")

        # Get pollencount for user chosen day and the previous day
        today_pollen ,previous_pollen = find_pollencount_by_date(df,date_picked)
        #st.write(today_pollen, previous_pollen)

        # show title on graph
        title_name = df.iloc[0]["Pollentype"]

        # set up max value of graoh range
        max_value = df["Pollencount"].max()
        max_value_gauge = max_value + 50

        risk_level_df_new = pd.read_csv("geo_data/risk_level_from_dwd_cleaned.csv")
        # low = risk_level_df_new.iloc[0]["geringe Belastung"]
        # med  = risk_level_df_new.iloc[0]["mittlere Belastung"]
        # high = risk_level_df_new.iloc[0]["hohe Belastung"]

        low = list(map(int, risk_level_df_new["geringe Belastung"][0].split(",")))
        med = list(map(int, risk_level_df_new["mittlere Belastung"][0].split(",")))
        high = risk_level_df_new["hohe Belastung"][0]


        # Visualization --------------------------------------------------------------------------
        fig = go.Figure(go.Indicator(
                mode = "number+gauge+delta",

                value = today_pollen, # Today's value
                title = {'text' : title_name}, #"<b>Alnu</b>"
                delta = {'reference': previous_pollen}, # Previous day value
                domain = {'x': [0, 1], 'y': [0, 1]},
                gauge = {'shape': "bullet",
                        'axis': {'range': [None, max_value_gauge]},
                        'threshold': {
                            'line': {'color': "red", 'width': 2},
                            'thickness': 0.75,
                            'value': 100},
                        'steps': [
                        {'range': low,'color': "lightgray"}, #,[0, 10], 
                        {'range': med, 'color': "lightyellow"}, # [11, 100],
                        {'range': [high, max_value_gauge], 'color': "pink"}]})) # [100, max_value_gauge],

        fig.update_layout(height = 250)

        st.write(fig)


if __name__ == '__main__':
    risk_level.get_risk_level()
    app()
    