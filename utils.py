
import numpy as np
import pandas as pd
import datetime
from datetime import datetime
import base64
import plotly
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import streamlit as st
#from io import BytesIO

  

# Define the multipage class to manage the multiple apps in our program 
class MultiPage: 
    """Framework for combining multiple streamlit applications."""

    def __init__(self) -> None:
        """Constructor class to generate a list which will store all our applications as an instance variable."""
        self.pages = []
    
    def add_page(self, title, func) -> None: 
        """Class Method to Add pages to the project
        Args:
            title ([str]): The title of page which we are adding to the list of apps 
            
            func: Python function to render this page in Streamlit
        """

        self.pages.append({
            "title": title,
            "function": func
            })

    def run(self):
        # Drodown to select the page to run  
        page = st.sidebar.selectbox(
            'App Navigation', 
            self.pages, 
            format_func=lambda page: page['title']
        )

        # run the app function 
        page['function']()

def clean_df(df):
    """
    param: dataframe
    returns: Convert data type to 'datetime'.
             Drop columns.
             Replace '-1' in 'pollencount' as 'Nan'. 
             Create a 'dummy_pollen'.

    """
    # Convert data type to datetime 
    df['Date'] = pd.to_datetime(df['Date'],dayfirst=True)
    # split year, month, day
    df['day'] = df['Date'].dt.day
    df['month'] = df["Date"].dt.month
    df['year'] = df['Date'].dt.year
    
    # Remove time(00:00:00) from "Date"
    #df["Date"]= df["Date"].dt.date
    # Drop columns
    df.drop(columns=["Operator","Recount","Comment","Daycount"],inplace=True)
    
    # Preprocessing
    # Replace "-1" as "Nan" in Pollencount.
    # -1 represent as missing value in order to distiguish ZERO pollencount.
    df["Pollencount"].replace(-1, np.nan, inplace=True)
    # Replace "Nan" as dummy numbers I came up with "-100"
    df["dummy_pollen"]=df["Pollencount"].replace(np.nan,-100)
    
    return df


def clean_df_dt(df):
    """
    param: dataframe
    returns: Convert data type to 'datetime'.
             Drop columns.
             Replace '-1' in 'pollencount' as 'Nan'. 
             Create a 'dummy_pollen'.

    """
    # Convert data type to datetime 
    df['Date_dummy'] = pd.to_datetime(df['Date'],dayfirst=True)
    # split year, month, day
    df['day'] = df['Date_dummy'].dt.day
    df['month'] = df["Date_dummy"].dt.month
    df['year'] = df['Date_dummy'].dt.year
    
    # Remove time(00:00:00) from "Date"
    #df["Date"]= df["Date"].dt.date
    # Drop columns
    df.drop(columns=["Operator","Recount","Comment","Daycount"],inplace=True)
    
    # Preprocessing
    # Replace "-1" as "Nan" in Pollencount.
    # -1 represent as missing value in order to distiguish ZERO pollencount.
    df["Pollencount"].replace(-1, np.nan, inplace=True)
    # Replace "Nan" as dummy numbers I came up with "-100"
    df["dummy_pollen"]=df["Pollencount"].replace(np.nan,-100)
    
    return df

def add_german_cl(df):
    
    """
    return : DataFrame: German name of pollentype
    params: DataFrame must have ["Pollentype"] colunm
    """
    
    if df["Pollentype"] == "ALNU":
        return "Erle"
    elif df["Pollentype"] == "AMBR":
        return "Traubenkraut"
    elif df["Pollentype"] == "ARTE":
        return "Beifuß"
    elif df["Pollentype"] == "BETU":
        return "Birke"
    elif df["Pollentype"] == "CORY":
        return "Hasel"
    elif df["Pollentype"] == "FRAX":
        return "Esche"
    elif df["Pollentype"] == "POAC":
        return "Gräser"
    elif df["Pollentype"] == "SECA":
        return "Roggen"
    else :
        return "others"

def add_latin_cl(df):
    
    """
    return : DataFrame: Latin name of pollentype
    params: DataFrame must have ["Pollentype"] colunm
    """
    
    if df["Pollentype"] == "ALNU":
        return "Alnus"
    elif df["Pollentype"] == "AMBR":
        return "Ambrosia"
    elif df["Pollentype"] == "ARTE":
        return "Artemisia"
    elif df["Pollentype"] == "BETU":
        return "Betula"
    elif df["Pollentype"] == "CORY":
        return "Corylus"
    elif df["Pollentype"] == "FRAX":
        return "Fraxinus"
    elif df["Pollentype"] == "POAC":
        return "Poaceae"
    elif df["Pollentype"] == "SECA":
        return "Secale"
    else :
        return "others"


def choose_pollenype(df, col_name,df_pollen_selected):
    
    """
    params : df = dataframe
             col_name = columns name
             df_pollen_selected = user chooses pollentype
    returns: df of chosen pollentype
    """
    # df = df[df[col_name] == pollen]
    df = df[df[col_name].isin(df_pollen_selected)]
    # reset index
    df.reset_index(drop=True,inplace=True)
    
    return df

def choose_pollenstation(df, col_name,station):
    # 
    df = df[df[col_name].isin(station)]
    
    # reset index
    df.reset_index(drop=True,inplace=True)
    
    return df


def choose_year(df, col_name,year):
    df = df[df[col_name].isin(year)]
    df.reset_index(drop=True,inplace=True)
    return df


def df_select_by_year2(dfs,df_year):

    #df = dfs[dfs[col_name].isin(df_year)]
    #df = dfs[df_year].isin(df_year)
    #df = dfs[dfs[df_year]]
    df = dfs[df_year]

    df.reset_index(drop=True,inplace=True)

    return df
import pdb

def cleaning_current_year(dfs,first_key):
    
        """
        Return : Dataframe of current year, filled with 

        """
        # get current year df's index (pd series)
        #series_date_current_year = dfs[first_key].Date.dt.date

        df_current_year = dfs[first_key]
        series_date = df_current_year['Date_dummy']
        series_date_current_year = pd.to_datetime(series_date).dt.date
        
        series_date_current_year = series_date_current_year.rename("Date2")
        df_current = pd.concat([df_current_year,series_date_current_year],axis=1)


        # concat current df and current year index
        
        #df_current = pd.concat([dfs[first_key],series_date_current_year],axis=1)
        df_current = pd.concat([df_current_year,series_date_current_year],axis=1)
        #pdb.set_trace()


        # set 'Date' column as index
        df_current['Date_dummy2'] = df_current.loc[:, 'Date_dummy']
        df_d_ind = df_current.set_index('Date_dummy')
        df_d_ind_Date_dt64 = pd.to_datetime(df_d_ind.Date)

        
        # create DatetimeIndex. range from 01 Jan current year till 31 Dec current year, eeryday, Descending order
        idx = pd.date_range(df_d_ind_Date_dt64.min(), df_d_ind_Date_dt64.max().to_period('Y').to_timestamp('Y'))
        idx = idx.sort_values(ascending=False)
        
        # Reindex df_d_ind with idx
        # created new rows filled with "NaN"
        df_till_end_year = df_d_ind.reindex(idx, method='ffill')
        
        # Change data type to "datetime64[ns]"
        df_till_end_year['Date2'] = pd.to_datetime(df_till_end_year.index,dayfirst=True)
        df_till_end_year['day'] = df_till_end_year["Date2"].dt.day
        df_till_end_year['month'] = df_till_end_year["Date2"].dt.month
        df_till_end_year['year'] = df_till_end_year["Date2"].dt.year
        
        # Prepare dictonary type of data which you want to fill in for df_till_end_year's "NaN"
        # item() contains "NaN" and a value. item(1) indecate a value such as "Berlin Charite" in "Pollenstation" column 
        filing_values = {df_till_end_year.columns[0]: df_till_end_year.Pollenstation.unique().item(1),
                        df_till_end_year.columns[1]: df_till_end_year.Pollentype.unique().item(1),
                        df_till_end_year.columns[8]: df_till_end_year.german_name.unique().item(1),
                        df_till_end_year.columns[9]: df_till_end_year.latin_name.unique().item(1)}

        # Imputate "NaN" with filling_values
        df_completed = df_till_end_year.fillna(value=filing_values)
        
        # remove DatetimeIndex and add normal numeric index
        df_completed  = df_completed.reset_index(drop=True)
        
     
        
        # Change the order of columns
        df_completed = df_completed[['Pollenstation', 'Pollentype', 'Pollencount','Date2','day', 'month',
                                   'year', 'dummy_pollen', 'german_name', 'latin_name']]

        # Rename columns
        df_completed = df_completed.rename(columns={"Date2":"Date_new"})

        return df_completed

def remove_rename_cols(dfs):

    """
    return : a dictonary of DataFrames. Remove "Date" column and rename "Date_dummy" to "Date_new"
    params : a dictonary of DataFrames
    """
    df_keys_list = list(dfs.keys())
    for k in df_keys_list:
        df = dfs[k]
        if "Date" in df and "Date_dummy" in df:
            df = df.drop(['Date'], axis=1)
            df = df.rename(columns={"Date_dummy":"Date_new"})
            dfs[k] = df


def simple_moving_ave(df):

    """
    params: dataframe
    returns:7 days average window calculation
    """
    # Centre = True : calculate k window with a centred point in the middle. (ex:day1-3 + day4(centred) + day5-7 = 7days window)
    # first 3 rows' result are not avaible because they need 3 rows before . 
    # min_period =1 : from 1 sample, SMA will be acclcated. (capable of avoiding having "NAN" value)

    df["7days_curv_sma"] =df.Pollencount.rolling(window=7,min_periods=1,center = True).mean()
    return df



def split_by_year(df):

    """
    params : a DataFrame contains ["year"] column. This col contains many consective years.
    return : dict of DataFrames. split df by each year. Reset all dfs index
    """

    years = df.year.unique()
    dfs = {}
    
    for y in years:
        name = "{0}".format(y)
        dfs[name] = df[df["year"]==y]
        dfs[name].reset_index(drop=True,inplace=True)
    return dfs


def add_luna(dfs):

    """
    params :dictonary of dfs. key : name of df / values: df
    Return :a list of dfs. each df has dummy luna days when it is not a luna year
    """

    luna_dfs =[]
    for d in dfs.values():
        if len(d) !=366:
        
            # create a row (df)
            row = pd.DataFrame({"Pollenstation":d.Pollenstation[0],"Pollentype":d.Pollentype[0],
                                 "Pollencount": np.nan, "Date":(str(d.year[0])+"-02-29"),"day": "29","month":"2","year":d.year[0]}, index=[305])

            # concat a new row and exsiting df
            d = pd.concat([d.iloc[:306], row, d.loc[306:]]).reset_index(drop=True)

            # IMPORTANT: errors="ignore" 29 feb 2019 does not exist it will return error otherwise.
            d['Date'] = pd.to_datetime(d['Date'],dayfirst=True,errors="ignore")
            luna_dfs.append(d)
        else:
            luna_dfs.append(d)
    
    return luna_dfs



def add_luna_year(df):

    """
    params :dataframe
    Return :dataframe has dummy luna days when it is not a luna year
    """
    if len(df) !=366:
        # create a row (df)
            row = pd.DataFrame({"Pollenstation":df.Pollenstation[0],"Pollentype":df.Pollentype[0],
                                 "Pollencount": np.nan, "Date":(str(df.year[0])+"-02-29"),"day": "29","month":"2","year":df.year[0]}, index=[305])

            # concat a new row and exsiting df
            df = pd.concat([df.iloc[:306], row, df.loc[306:]]).reset_index(drop=True)
            # IMPORTANT: errors="ignore" 29 feb 2019 does not exist it will return error otherwise.
            df['Date'] = pd.to_datetime(df['Date'],dayfirst=True,errors="ignore")
    else:
        pass

    return df


def create_pollencount_year(df,luna_dfs_dict):
    
    """
    df : DataFrame
    dfs_dicct : a dictonary of Dataframe
    returns:  a DataFrame contains "Pollencount" from each dataframe from a list of Dataframes.
    
    """
    years = df.year.unique()
    dfs_pollen={}
    temp_list = list(luna_dfs_dict.values())
    
    for count, _ in enumerate(temp_list):
        name = "Pollencount{0}".format(years[count])
        dfs_pollen[name] = temp_list[count]["Pollencount"].rename(name)
    
    pollencount_df = pd.DataFrame.from_dict(dfs_pollen)
    
    return pollencount_df

def calcualte_7yr_avg(pollencount_df):
    """
    params: a Dataframe has columns of ["Pollencount"]
    returns: add new column ["7years_avg"] in df
    
    """
    # sum(axis=1) choose rows to calculate. if axis =0, calcualte columns
    pollencount_df["7years_avg"] = pollencount_df.sum(axis=1)/7
    
    return pollencount_df

def calcualte_n_years_SMA(pollencount_df):
    """
    params: a Dataframe has columns of ["Pollencount"]
    returns: simple moving average of n years "pollencount"
    
    """
    # sum(axis=1) choose rows to calculate. if axis =0, calcualte columns
    pollencount_df["n_years_sma"] = pollencount_df.Pollencount.rolling(window=7,min_periods=1,center = True).mean()
    return pollencount_df

def calcualte_n_yr_avg_SMA(pollencount_df):
    """
    params: a Dataframe has columns of ["Pollencount"]
    returns: 1. add 2 new columns:  ["years_avg"] and ["years_SMA"]in pollencount_df. 
    
    
    """
    # sum(axis=1) choose rows to calculate. if axis =0, calcualte columns
    pollencount_df["years_avg"] = pollencount_df.sum(axis=1)/7
    
    # SMA of ["years_avg"]
    pollencount_df["years_SMA"] =pollencount_df.years_avg.rolling(window=7,min_periods=1,center = True).mean()
    
    return pollencount_df

def df_select_by_year(dfs,year_key,user_chosen_year):

    """
    params :dfs = dict type dataframe
            year_key = 
    """
    #df = dfs[year_key]
    df = dfs[year_key].isin(user_chosen_year)
    #df = dfs[dfs.isin(df_pollen_selected)]
    df.reset_index(drop=True,inplace=True)
    return df


def download_link(object_to_download, download_filename, download_link_text):
    """
    Generates a link to download the given object_to_download.

    object_to_download (str, pd.DataFrame):  The object to be downloaded.
    download_filename (str): filename and extension of file. e.g. mydata.csv, some_txt_output.txt
    download_link_text (str): Text to display for download link.

    Examples:
    download_link(YOUR_DF, 'YOUR_DF.csv', 'Click here to download data!')
    download_link(YOUR_STRING, 'YOUR_STRING.txt', 'Click here to download your text!')

     """
    if isinstance(object_to_download,pd.DataFrame):
        object_to_download = object_to_download.to_csv(index=False)

    # some strings <-> bytes conversions necessary here
    b64 = base64.b64encode(object_to_download.encode()).decode()

    return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'


        # # Examples
        # df = pd.DataFrame({'x': list(range(10)), 'y': list(range(10))})
        # st.write(df)

        # if st.button('Download Dataframe as CSV'):
        #     tmp_download_link = download_link(df, 'YOUR_DF.csv', 'Click here to download your data!')
        #     st.markdown(tmp_download_link, unsafe_allow_html=True)

        # s = st.text_input('Enter text here')
        # st.write(s)

        # if st.button('Download input as a text file'):
        #     tmp_download_link = download_link(s, 'YOUR_INPUT.txt', 'Click here to download your text!')
        #     st.markdown(tmp_download_link, unsafe_allow_html=True)

def download_fig_link(object_to_download, download_filename, download_link_text):
    """
    Generates a link to download the given object_to_download.

    object_to_download (str, plotly.graph_objs._figure.Figure):  The object to be downloaded.
    download_filename (str): filename and extension of file. e.g. myfile.html
    download_link_text (str): Text to display for download link.

    Examples:
    download_fig_link(YOUR_fig, 'alnu2020.html', 'Click here to download data!')
    

    """
    if isinstance(object_to_download,plotly.graph_objs._figure.Figure):
        object_to_download = object_to_download.write_html("download_filename.html")
    
    #some strings <-> bytes conversions necessary here
    b64 = base64.b64encode(object_to_download.encode()).decode()

    return f'<a href="data:image/png;base64,{b64}" download="{download_filename}">{download_link_text}</a>'





def sum_pollen_w_coordinate(pollen_sum_dict,d):
    
        """
        Returns: a dataframe. The number of coordinates
        (ex, aachen has 4 BETU pollen in year of 2020. data will be 4 coordinates of aachen)
        to visualise hexagonlayer on map.
        Params: 
        d: dictonary. keys : staions,  values: corrdinates
        pollen_sum_dict : dictonary. keys : staions,  values: the anual sum of pollen 
        """
        temp_dfs_list =[]
        for station_name in pollen_sum_dict.keys():
            temp_df = pd.DataFrame(index=range(int(pollen_sum_dict[station_name])),data=d[station_name])
            temp_dfs_list.append(temp_df)
        
        # make
        pydeck_df = pd.concat(temp_dfs_list)
        pydeck_df = pydeck_df.reset_index(drop=True)
        
        return pydeck_df

def cal_pollen_sum(df):
        
        """
        Returns: dictonary.keys: station names values: sum of pollen
        param : dataframe. a pollen type and a year are specified by users
        
        """
    
        # Clean string value, delete space 
        df["Pollenstation"] = df["Pollenstation"].str.replace(" ","")
        # lsit of pollenstations
        sta_list = df.Pollenstation.unique().tolist()

        # empty list and dictonary
        sum_pollen=[]
        pollen_sum_dict ={}

        # calculate the sum of each pollen staion's pollen
        # place data in a list "sum_pollen"
        for station in sta_list:
            count_sum = df[df["Pollenstation"]==station].Pollencount.sum()
            sum_pollen.append(count_sum)

        # Pair up and make a dictornary "pollen_sum_dict"
        # key : pollen station
        # values: pollen sum of each stations 
        for count,sta_name in enumerate(sta_list):
            pollen_sum_dict[sta_name] =  sum_pollen[count]

        return pollen_sum_dict

def find_pollencount_by_date(df,selected_date):
    
    """
    return : 2 varibles. 1.selected day's pollen count 2. previous day's pollen count
    params : df : dataframe / selected_date strings ex "2020-02-10". the same data type as df's "Date" columns
    
    """
    
    # today
    pollen_selected_day = df[df.eq(selected_date).any(1)].Pollencount.values
    pollen_selected_day = pollen_selected_day.astype(float).item(0)
    
    # previous day
    selected_day_ind = df[df.eq(selected_date).any(1)].index
    previous_day_ind = selected_day_ind -1
    pollen_previous_day = df.iloc[previous_day_ind].Pollencount.values
    pollen_previous_day =  pollen_previous_day.astype(float).item(0)
    
    return pollen_selected_day, pollen_previous_day

def calculate_inactivated_rates(df):
    """
    params: dataframe has 'year','month', 'dummy_calp' columns. all years (2014-current)' data, selected one pollen station.(no mix of stations)
    return: dataframe, persantages of monthly persantages for each year 
    
    """
    
    # groupby df
    year_month_gb_df = df.groupby(['year','month', 'dummy_calp']).size().unstack(fill_value=0)
    
    # 2014-2021
    years =year_month_gb_df.xs(1, level="month").index
    
    # create an empty dictonary for storing series of persentages later
    dict_persentages ={}
    
    

    # pass "y" (y is a single value of a list, called "years") of as a index to get "-1" values 
    for y in years:
        
        # inactivated_d = pd.Series of the number of "-1"(inactivated day)days
        inactivated_d = year_month_gb_df.xs(y, level="year")[-1]
        # d_in_month = counted each categories (0,1,-1) for each month
        d_in_month =  year_month_gb_df.xs(y, level="year")[0:1].values
        # d_in_month_sum = sum of each months' dates. ex, Jan is 31, Feb is 28(29) etc... 
        d_in_month_sum = year_month_gb_df.xs(y, level="year")[0:1].values.sum()

        # calculate inactive dates persentages
        persentages = inactivated_d/d_in_month_sum

        # store persantages with dictonary keys
        dict_persentages[y] = persentages

        # create a dataframe
        # columns year
        # index month
        dict_persentages_df = pd.DataFrame.from_dict(dict_persentages)

    return dict_persentages_df

def get_dfs_CalendarHeatmap(df):
    
    """
    return : dictornary, key : years, values: pd.Series 
    params : df = dataframe has one pollen type, one pollen station and unseparated years(ex,2014-2021)
    
    """
    dfs = split_by_year(df)
    
    
    datetime_vals ={}
    for k in dfs.keys():
        name = "{0}".format(k)
        datetime_vals[name] = dfs[k].Date.values
    
    dt_s = {}
    for dt_k in datetime_vals.keys():
        dt_k_name = "{0}".format(dt_k)
        dt_s[dt_k_name] =pd.Series(dfs[dt_k]["dummy_calp"].values, index=datetime_vals[dt_k])
        
    return dt_s



def split_months(df):
    """
    Take a df, slice by year, and produce a list of months,
    where each month is a 2D array in the shape of the calendar
    :param df: dataframe or series
    :return: matrix for daily values and numerals
    """
    #df = df[df.index.year == year]


    # Empty matrices
    a = np.empty((6, 7))
    a[:] = np.nan

    day_nums = {m:np.copy(a) for m in range(1,13)}  # matrix for day numbers
    day_vals = {m:np.copy(a) for m in range(1,13)}  # matrix for day values

    # Logic to shape datetimes to matrices in calendar layout
    for d in df.iteritems():  # use iterrows if you have a DataFrame

        day = d[0].day
        month = d[0].month
        col = d[0].dayofweek

        if d[0].is_month_start:
            row = 0

        day_nums[month][row, col] = day  # day number (0-31)
        day_vals[month][row, col] = d[1] # day value (the heatmap data)
        
        if col == 6:
            row += 1

    return day_nums, day_vals



def create_year_calendar(day_nums, day_vals):


    weeks = [1, 2, 3, 4, 5, 6]
    days = ['M', 'T', 'W', 'T', 'F', 'S', 'S']
    month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
                'September', 'October', 'November', 'December']

    fig, ax = plt.subplots(3, 4, figsize=(14.85, 10.5))

    for i, axs in enumerate(ax.flat):
        
        
        # vmin. vmax is a range of colour.set (-1 ~ 1)  
        # cmap='ocean_r' is colour of the heatmap, more ptions
        # https://matplotlib.org/stable/tutorials/colors/colormaps.html
        axs.imshow(day_vals[i+1], cmap='ocean_r',  vmin=-1, vmax=1)  # heatmap
        axs.set_title(month_names[i])

        # Labels
        axs.set_xticks(np.arange(len(days)))
        axs.set_xticklabels(days, fontsize=10, fontweight='bold', color='#555555')
        axs.set_yticklabels([])

        # Tick marks
        axs.tick_params(axis=u'both', which=u'both', length=0)  # remove tick marks
        axs.xaxis.tick_top()

        # Modify tick locations for proper grid placement
        axs.set_xticks(np.arange(-.5, 6, 1), minor=True)
        axs.set_yticks(np.arange(-.5, 5, 1), minor=True)
        axs.grid(which='minor', color='w', linestyle='-', linewidth=2.1)

        # Despine
        for edge in ['left', 'right', 'bottom', 'top']:
            axs.spines[edge].set_color('#FFFFFF')

        # Annotate
        for w in range(len(weeks)):
            for d in range(len(days)):
                day_val = day_vals[i+1][w, d]
                day_num = day_nums[i+1][w, d]

                # Value label
                axs.text(d, w+0.3, f"{day_val:0.0f}",
                         ha="center", va="center",
                         fontsize=7, color="w", alpha=0.8)

                # If value is -1, draw a grey patch
                if day_val == -1:
                    patch_coords = ((d - 0.5, w - 0.5),
                                    (d - 0.5, w + 0.5),
                                    (d + 0.5, w + 0.5),
                                    (d + 0.5, w - 0.5))
                
                # If value is -1, draw a grey patch
                if day_val == -1:
                    patch_coords = ((d - 0.5, w - 0.5),
                                    (d - 0.5, w + 0.5),
                                    (d + 0.5, w + 0.5),
                                    (d + 0.5, w - 0.5))


                    square = Polygon(patch_coords, fc='#DDDDDD')
                    axs.add_artist(square)

                # If day number is a valid calendar day, add an annotation
                if not np.isnan(day_num):
                    axs.text(d+0.45, w-0.31, f"{day_num:0.0f}",
                             ha="right", va="center",
                             fontsize=6, color="#003333", alpha=0.8)  # day #color="#003333"

                # Aesthetic background for calendar day number
                patch_coords = ((d-0.1, w-0.5),
                                (d+0.5, w-0.5),
                                (d+0.5, w+0.1))

                triangle = Polygon(patch_coords, fc='w', alpha=0.7)
                axs.add_artist(triangle)

    # Final adjustments
    fig.suptitle('Calendar', fontsize=16)
    plt.subplots_adjust(left=0.04, right=0.96, top=0.88, bottom=0.04)

    # Save to file
    #plt.savefig('calendar_example.pdf')
    #plt.show()
    return fig


def choose_period_month(df,month,start,end):

    """
    return : Dataframe of chosen period of months. Start from 1st of chosen month and end at the end of month.
    paramns : df ; dataframe
            col_name ; "month"
            start ; user selected start month
            end ; user selected end month
    """

    df_filtered = df.loc[df[month].between(start,end)]
    return df_filtered


# def get_image_download_link(img):
# 	"""Generates a link allowing the PIL image to be downloaded
# 	in:  PIL image
# 	out: href string
# 	"""
# 	buffered = BytesIO()
# 	img.save(buffered, format="JPEG")
# 	img_str = base64.b64encode(buffered.getvalue()).decode()
# 	href = f'<a href="data:file/jpg;base64,{img_str}">Download result</a>'
# 	return href