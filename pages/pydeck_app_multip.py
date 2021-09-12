import pandas as pd
import pydeck
import numpy as np
import streamlit as st
import plotly.express as px
import os

# from pages import utils_multip
from utils import clean_df
from utils import choose_pollenype
from utils import choose_year
from utils import sum_pollen_w_coordinate
from utils import cal_pollen_sum

st.set_page_config(layout="wide")



def app():
    # uploaded_file = st.file_uploader("Choose a csv file")
    # if uploaded_file is not None:
    #     df_all= pd.read_csv(uploaded_file)
    #     st.write("File name:", uploaded_file.name)

    if 'new_main_data.csv' not in os.listdir('geo_data'):
        st.markdown("Please upload data through `Upload Data` page!")
    else:
        # df_analysis = pd.read_csv('data/2015.csv')
        df = pd.read_csv('geo_data/new_main_data.csv')


        # Clean  dataframe
        df = clean_df(df)
        df['Date'] = pd.to_datetime(df['Date']).dt.date

        # User selects pollentype from sidebar
        pollen_types = df.Pollentype.unique()
        pollen_selected = st.sidebar.multiselect('Select a pollen type', pollen_types)
        df_sel_p= choose_pollenype(df, "Pollentype", pollen_selected)
        

        year_choices = df_sel_p.year.unique()
        year_selected = st.sidebar.multiselect('Select a year', year_choices)
        df_sel_p_y = choose_year(df_sel_p, "year",year_selected)


        #df_sel_p_y['Pollenstation'] = df_sel_p_y['Pollenstation'].str.replace(" ","")


        pollen_sum_dict = cal_pollen_sum(df_sel_p_y)
        pollen_sum_dict_df = pd.DataFrame.from_dict(pollen_sum_dict,orient='index',columns=["Pollencount"])
        pollen_sum_dict_df["Station"] = pollen_sum_dict_df.index
        pollen_sum_dict_df.reset_index(drop=True,inplace=True)
        pollen_sum_dict_df = pollen_sum_dict_df[["Station","Pollencount"]]


        d = {"DEBER1-BerlinCharite" :{"lat":52.52673655020027,"lon":13.376722305466584},
        "DEAACH-Aachen":{"lat":50.775345,"lon":6.083887},
        #"Gross_Glienicke_Potsdam":{"lat":52.485183141189,"lon": 13.108758170536294},
        "DEBORS-Borstel":{"lat":52.669842,"lon":8.970460},
        "DEMOEN-Mönchengladbach":{"lat":51.192230,"lon":6.439590}}
        coordinates = pd.DataFrame(data=d)
        coordinates = coordinates.swapaxes("index", "columns")
        
        if pollen_sum_dict and d is not None:

            pydeck_df = sum_pollen_w_coordinate(pollen_sum_dict,d)

            st.write(pollen_sum_dict_df)


            # Plotly bar chart -----------------------------------------------------------------
            fig = px.bar(pollen_sum_dict_df, y='Pollencount', x='Station', text='Pollencount')
            fig.update_traces(textposition='outside')
            fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
            st.plotly_chart(fig,use_container_width=True)

        
        
            # Pydeck map ------------------------------------------------------------------------
            st.pydeck_chart(pydeck.Deck(
                map_style="mapbox://styles/mapbox/light-v9",
                initial_view_state=pydeck.ViewState(
                    longitude=12.40068845254159,
                    latitude=50.52007886722756,
                    zoom=5,
                    min_zoom=5,
                    max_zoom=15,
                    pitch=40.5,
                    bearing=-27.36
                ),
                layers=[pydeck.Layer('HexagonLayer',
                    pydeck_df,
                    get_position="[lon,lat]",
                    auto_highlight=True,
                    elevation_scale=10,
                    pickable=True,
                    elevation_range=[0, 5000],
                    extruded=True,
                    coverage=15)]
            ))



    #r = pydeck.Deck(layers=[layer], initial_view_state=view_state)
    # r = pydeck.Deck(map_style="mapbox://styles/mapbox/light-v9",
    # layers=[layer],initial_view_state=view_state,tooltip={"html": "<b>Elevation Value:</b> {elevationValue}",
    # "style": {"color": "white"}})


    # r.to_html('test_station2.html')
    # st.pydeck_chart(r)
