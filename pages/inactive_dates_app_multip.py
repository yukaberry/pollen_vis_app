import numpy as np
import pandas as pd
import streamlit as st
#from streamlit_echarts import st_echarts

#import datetime
#from datetime import datetime
import calplot
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
import os

from utils import clean_df
from utils import choose_pollenstation
from utils import choose_pollenype
from utils import add_german_cl, add_latin_cl
from utils import calculate_inactivated_rates
from utils import get_dfs_CalendarHeatmap
from utils import split_months
from utils import create_year_calendar

def app():
    # uploaded_file = st.sidebar.file_uploader("Choose a csv file")
    # if uploaded_file is not None:
    #     df=pd.read_csv("export_Yuka_20210519.csv")

    if 'new_main_data.csv' not in os.listdir('geo_data'):
        st.markdown("Please upload data through `Upload Data` page!")
    else:
        # df_analysis = pd.read_csv('data/2015.csv')
        df = pd.read_csv('geo_data/new_main_data.csv')

        df = clean_df(df)

        df.loc[(df["dummy_pollen"]>=1),"dummy_calp"]=1
        df.loc[(df["dummy_pollen"]==0),"dummy_calp"]=0
        df.loc[(df["dummy_pollen"]==-100),"dummy_calp"]=-1


        df["german_name"] = df.apply(lambda df:add_german_cl(df),axis=1)
        df["latin_name"] = df.apply(lambda df:add_latin_cl(df),axis=1)

        #st.write(df)

        # User selects pollenstation from sidebar --------------------------------------
        pollen_stations = df["Pollenstation"].unique()
        station_selected = st.sidebar.multiselect('Select a pollen station', pollen_stations)
        df= choose_pollenstation(df, "Pollenstation", station_selected)

        pollen_types = df['latin_name'].unique()
        pollen_selected = st.sidebar.multiselect('Select a pollen type (latin name)', pollen_types)
        # Sort dataframe based on user's selection of pollentype
        df= choose_pollenype(df, "latin_name", pollen_selected)

        #st.write(df)

        # return inacative rates of every month from 2014 to current year ---------------------------
        dict_persentages_df = calculate_inactivated_rates(df).transpose()

        # dict_persentages_df = calculate_inactivated_rates(df)
        #st.write(dict_persentages_df)

        # preapare values for visualization ----------------------------------------------------------
        # z = values
        z = np.round_(dict_persentages_df.values,decimals=3)
        # y = yaxis 
        y = dict_persentages_df.index.tolist()
        # x = xaxis
        x = dict_persentages_df.columns.tolist()

        # plot a figure ---------------------------------------------------------------------------------------
        fig = ff.create_annotated_heatmap(z, x=x, y=y,showscale=True,font_colors=["black","white"])#reversescale=True,)#font_colors=["black","white"])
        fig.update_traces(colorscale="burg", selector=dict(type='heatmap'))
        fig.update_traces(hoverlabel_font_color="pink", selector=dict(type='heatmap'))
        st.markdown("# Inactive rates per month")
        st.markdown("The chart shows inactivate days of a staion you choose by the rate between 0.0 ~ 1.0. The higher the number is, the more missing data ")
        st.write(fig)

        # ----------------------------------------------------------------------------------------------

        dt_s = get_dfs_CalendarHeatmap(df)

        year_choices = list(dt_s)
        year_selected  = st.sidebar.selectbox('Select a year', year_choices)
        #st.write(dt_s[year_selected])
        dt_s_selected =dt_s[year_selected].sort_index(ascending=True)



        # Plot calendar heatmaps for the entire year a user choses ----------------------------------------------
        day_nums, day_vals = split_months(dt_s_selected)
        fig = create_year_calendar(day_nums, day_vals)
        st.markdown("# Daily Deatils of inactive and missing days")
        st.markdown("This calendar shows 3 categories of station status. Green is active and collect pollen, Blue is active and collect zero pollen, Gray is inactive and does not count pollen.")

        st.pyplot(fig)


        # show data process----------------------------------------------
        st.write(df.head())
        st.write(dict_persentages_df)
        st.write(dt_s[year_selected])









# If calplot is supported, these codes would work ---------------------------------------------

# all_days2 = df["Date"].values
# events2 = pd.Series(df["dummy_calp"].values, index=all_days2)
# events3 = pd.Series(df["Pollencount"].values, index=all_days2)

# if events2 is not None:
#     st_echarts(calplot.calplot(events2,textformat='{:.0f}'))


    # # d_in_month = counted each categories (0,1,-1) for each month
    # d_in_month =  year_month_gb_df.xs(y, level="year")[0:1].values
    # # d_in_month_sum = sum of each months' dates. ex, Jan is 31, Feb is 28(29) etc... 
    # d_in_month_sum = year_month_gb_df.xs(y, level="year")[0:1].values.sum()

    # # calculate inactive dates persentages
    # persentages = inactivated_d/d_in_month_sum

    # # store persantages with dictonary keys
    # dict_persentages[y] = persentages

    # # create a dataframe
    # # columns year
    # # index month
    # dict_persentages_df = pd.DataFrame.from_dict(dict_persentages)


    
#st.write(dict_persentages_df)
