import numpy as np
import pandas as pd
import datetime 
from datetime import datetime
import streamlit as st
import os
import base64
import plotly.express as px
import plotly.graph_objects as go

from io import StringIO, BytesIO


#from utils_multip import clean_df
# from pages import utils_multip
from utils import choose_pollenype
from utils import choose_pollenstation
from utils import simple_moving_ave
from utils import split_by_year
from utils import add_luna
from utils import create_pollencount_year
from utils import add_german_cl
from utils import add_latin_cl
from utils import cleaning_current_year
from utils import calcualte_n_yr_avg_SMA
from utils import clean_df_dt
from utils import remove_rename_cols


def app():
    #breakpoint()
    if 'new_main_data.csv' not in os.listdir('temp_data'):
        st.markdown("Please upload data through `Upload Data` page!")
    else:
        # df_analysis = pd.read_csv('data/2015.csv')
        df = pd.read_csv('temp_data/new_main_data.csv')
        

    # uploaded_file = st.file_uploader("Choose a csv file")
    # if uploaded_file is not None:
    #     df= pd.read_csv(uploaded_file)
    #     st.write("filename:", uploaded_file.name)

        # Clean  dataframe ---------------------------------------------------------
        df = clean_df_dt(df)
        #df['Date'] = pd.to_datetime(df['Date'],format='%Y-%m-%d').dt.date
        df["german_name"] = df.apply(lambda df:add_german_cl(df),axis=1)
        df["latin_name"] = df.apply(lambda df:add_latin_cl(df),axis=1)

        # User selects pollentype from sidebar ----------------------------------------
        pollen_types = df['latin_name'].unique()
        pollen_selected = st.sidebar.multiselect('Select a pollen type (latin name)', pollen_types)
        # Sort dataframe based on user's selection of pollentype
        df= choose_pollenype(df, "latin_name", pollen_selected)


        # User selects pollenstation from sidebar --------------------------------------
        pollen_stations = df["Pollenstation"].unique()
        station_selected = st.sidebar.multiselect('Select a pollen station', pollen_stations)
        df= choose_pollenstation(df, "Pollenstation", station_selected)


        dfs = split_by_year(df)

        # cleaning current year df ----------------------------------------------------------------
        # Defining the current year by using dictonary's order. **from python 3.7, dict preserves the order
        first_key = list(dfs)[0]
        df_completed = cleaning_current_year(dfs,first_key)
        # Cleaning dfs except current year ----------------------------------------------------------
        # Removing Remove "Date" column and rename "Date_dummy" to "Date_new"
        remove_rename_cols(dfs)

        # Put current year's df to dsf dictonary -------------------------------------------------
        dfs[list(dfs)[0]] = df_completed
        #st.write(dfs[list(dfs)[0]])

        # ----------------------------------------------------------------------------

        luna_dfs = add_luna(dfs)


        luna_dfs_dict= {}
        for key in dfs.keys():
            for value in luna_dfs:
                luna_dfs_dict[key] = value
                luna_dfs.remove(value)
                break 
        # -----------------------------------------------------------------------------

        pollencount_df = create_pollencount_year(df,luna_dfs_dict)
        pollencount_df = calcualte_n_yr_avg_SMA(pollencount_df)
        avg_years = pollencount_df[["years_avg","years_SMA"]]


    # ------------------------------------------------------------------------------

        user_choices_year = list(luna_dfs_dict)
        user_chosen_year = st.sidebar.selectbox('Select a year for visualising a chart.', user_choices_year)
        
        # -------------------------------------------------------------------------------

        if user_chosen_year is not None:

            user_chosen_df = pd.concat([luna_dfs_dict[user_chosen_year],avg_years], axis=1)
            # add 7days moving average columns
            user_chosen_df = simple_moving_ave(user_chosen_df)
            #st.write(user_chosen_df)

        
            # Make a list of indices for next step 
            ind_list = []
            for ind in range(1,13):
                index = user_chosen_df[(user_chosen_df["month"]==ind) & (user_chosen_df["day"]==1)].index
                ind_list.append(index)

        
            # make a list of 01 Jan to 01 Dec current year. Use indices from previous step in order to access df value
            date_index = []
            for index in ind_list:
                ind = user_chosen_df.loc[index].Date_new
                ind = ind.values
                date_index.append(ind)

            # 12D array to 1D array
            date_index = np.concatenate(date_index)

    # ----------------------------------------------------------------------------
        #st.write(user_chosen_df)

            fig = go.Figure()
            # fig.add_trace(go.Scatter(x=user_chosen_df["Date_new"], y=user_chosen_df["years_SMA"], fill='tozeroy',
            #                     mode='none',name="7 years' (2014-2020) SMA average" # override default markers+lines
            #                     ))

            fig.add_trace(go.Scatter(x=user_chosen_df["Date_new"], y=user_chosen_df["years_avg"], fill='tozeroy',
                                mode='none',name="7 years' (2014-2020) average" # override default markers+lines
                                ))

            fig.add_trace(go.Scatter(x=user_chosen_df["Date_new"],y=user_chosen_df["7days_curv_sma"],
                                    mode='lines', name="7days SMA"))
            
            # fig.add_trace(go.Scatter(x=user_chosen_df["Date_new"],y=user_chosen_df["Pollencount"],
            #                         mode='lines', name="Actual pollen count"))
            
    

            # asterisk before list's name so it will be printed without"" and []
            titles ="Pollen Type : " + str(*pollen_selected) + "   Year : " + str(user_chosen_year) + "   Station : " +  str(*user_chosen_df["Pollenstation"].unique())
            fig.update_layout(title= titles,height=500,width=1100,annotations=[
                                        go.layout.Annotation(
                                            x=0.999,
                                            y=0.95,
                                            showarrow=False,
                                            text=u"\u00A9"+"Stiftung Deutscher Polleninformationsdienst ",
                                            xref="paper",
                                            yref="paper"
                                        )
                                    ])



            fig.update_xaxes(ticks="inside",
            ticktext=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],
            tickvals=date_index,)

            
            # mybuff = StringIO()
            # fig.write_html(mybuff, include_plotlyjs='cdn')
            # mybuff = BytesIO(mybuff.read().encode('utf8'))
            # #import pdb; pdb.set_trace()
            # b64 = base64.b64encode(mybuff.read()).decode()
            # href = f'<a href="data:text/html;charset=utf-8;base64, {b64}" download="plot.html">Download plot</a>'

            # #st.markdown(href, unsafe_allow_html=True)
            # st.markdown(href,unsafe_allow_html=True)

            st.plotly_chart(fig)

            # NEDD TO BE FIXED -----------------------------------------------------
            # images is not dowloaded, maybe because of private repo, worked in local env
            mybuff = StringIO()
            fig.write_html(mybuff, include_plotlyjs='cdn')
            mybuff = BytesIO(mybuff.read().encode('utf8'))
            #import pdb; pdb.set_trace()
            b64 = base64.b64encode(mybuff.read()).decode()
            href = f'<a href="data:text/html;charset=utf-8;base64, {b64}" download="plot.html">Download plot</a>'
            

            
            st.markdown(href,unsafe_allow_html=True)
        


        st.dataframe(user_chosen_df)
            

