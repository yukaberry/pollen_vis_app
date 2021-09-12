import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import base64
import time
import os

from utils import clean_df
from utils import choose_pollenype
from utils import choose_year
from utils import choose_period_month

# Show screencast --------------------------------------------------------------------------------
# video_file = open("screencast/linechart_screencast.webm", 'rb')
# video_bytes = video_file.read()
# st.video(video_bytes, start_time=0)



# ---------------------------------------------------with Stephan

# mymidia_placeholder = st.empty()

# mymidia_str = "data:video/ogg;base64,%s"%(base64.b64encode(video_bytes).decode())
# mymidia_html = """
#                 <video controls autoplay>
#                 <source src="%s" type="video/ogg">
#                 Your browser does not support the audio element.
#                 </video>
#             """%mymidia_str

# mymidia_placeholder.empty()
# time.sleep(0)
# mymidia_placeholder.markdown(mymidia_html, unsafe_allow_html=True)

#------------------------------------------------------------------------------




# uploaded_file = st.sidebar.file_uploader("Choose a csv file")
# if uploaded_file is not None:
#     df= pd.read_csv(uploaded_file)
#     st.write("filename:", uploaded_file.name)
def app():

    # uploaded_file = st.sidebar.file_uploader("Choose a csv file")
    # if uploaded_file is not None:
    #     # Clean  dataframe
    #     df= pd.read_csv(uploaded_file)

    if 'new_main_data.csv' not in os.listdir('geo_data'):
        st.markdown("Please upload data through `Upload Data` page!")
    else:
        # df_analysis = pd.read_csv('data/2015.csv')
        df = pd.read_csv('geo_data/new_main_data.csv')

        df = clean_df(df)
        df['Date'] = pd.to_datetime(df['Date']).dt.date
        # User selects pollentype from sidebar
        pollen_types = df['Pollentype'].unique()
        pollen_selected = st.sidebar.multiselect('Select a pollen type', pollen_types)
        # Sort dataframe based on user's selection of pollentype
        df= choose_pollenype(df, "Pollentype", pollen_selected)




        year_choices = df.year.unique()
        year_selected = st.sidebar.multiselect('Select a year', year_choices)
        df = choose_year(df, "year",year_selected)


        start_time_period = df.month.unique()
        # index : set a default value from "start_time_period". (ex index11 : January)
        start_time_period_selected = st.sidebar.selectbox("choose the start of month",start_time_period,index=11)

        end_time_period = df.month.unique()
        # default value : May
        end_time_period_selected = st.sidebar.selectbox("choose the end of month",end_time_period,index=7)




        df_fil = choose_period_month(df,"month",start_time_period_selected,end_time_period_selected)
        # st.write(df_fil)


        df_1 = df.query("Pollenstation == 'DEAACH - Aachen'").Pollencount.sum()
        df_2 = df.query("Pollenstation == 'DEBER1 - Berlin Charite'").Pollencount.sum()
        df_3 = df.query("Pollenstation == 'DEBORS - Borstel'").Pollencount.sum()
        df_4 = df.query("Pollenstation == 'DEMOEN - Mönchengladbach'").Pollencount.sum()


        x = ['DEAACH - Aachen','DEBER1 - Berlin Charite','DEBORS - Borstel','DEMOEN - Mönchengladbach']
        y = [df_1, df_2, df_3,df_4]

        #st.write("Aachen station and annual selected pollen summary")
        #st.write(df_1)

        # combine user chosen dataframe 
        if df_fil is not None:

            fig = px.line(df_fil, x="Date", y="Pollencount", color='Pollenstation')
            st.write(fig)


            fig2 = go.Figure(data=[go.Bar(
                x=x, y=y,
                text=y,
                textposition='auto',
            )])
            st.write(fig2)

        
        #st.write(df_1)



