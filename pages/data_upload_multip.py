import streamlit as st
import numpy as np
import pandas as pd
from PIL import  Image


def app():
    #st.markdown("## Data Upload")

    # Upload the dataset and save as csv
    st.markdown("# Upload a csv file for analysis here") 

    # Code to read a single file 
    uploaded_file = st.file_uploader("Choose a file", type = ['csv'])#, 'xlsx'])
    global data # To create a global variable inside a function
    
    #breakpoint()
    if uploaded_file is not None:
        #try:
            data = pd.read_csv(uploaded_file)
            data.to_csv('temp_data/new_main_data.csv', index=False)
        # except Exception as e:
        #     print(e)
        #     data = pd.read_excel(uploaded_file)
            # save data
            #st.write(data)
            #data.to_csv('geo_data/new_main_data.csv', index=False)
    

    st.markdown("Please note that there is a format of data files you can upload for data anaysis.")
    st.markdown("File type : csv, The numer of columns : 8, The number of Pollenstation/Pollentype : unlimited")

    img = Image.open("images/CSVsample.PNG")
    st.image(img)


    # if st.button("Load Data"):
        
    #     # Raw data 
    #     st.dataframe(data)
    #     data.to_csv('geo_data/new_main_data.csv', index=False)
    
    