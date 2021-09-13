
import streamlit as st
import os
import numpy as np
from PIL import  Image

# Custom imports 
from utils import MultiPage

from pages import dashbord_app_multip, main_app_multip, pydeck_app_multip #folium_map_app_multip
from pages import gauge_app_multip, inactive_dates_app_multip,linechart_app_multip,data_upload_multip


# Create an instance of the app 
app = MultiPage()


#----------------------------
# def file_selector(folder_path='.'):
#     filenames = os.listdir(folder_path)
#     selected_filename = st.selectbox('Select a file', filenames)
#     return os.path.join(folder_path, selected_filename)

# filename = file_selector()
# st.write('You selected `%s`' % filename)
# https://discuss.streamlit.io/t/filenotfounderror-errno-2-no-such-file-or-directory-fsnm-png/7260
# https://stackoverflow.com/questions/22282760/filenotfounderror-errno-2-no-such-file-or-directory
# https://stackoverflow.com/questions/7783308/os-path-dirname-file-returns-empty
#----------------------------



display = Image.open("images/PIDlogo.PNG")
display = np.array(display)
col1, col2 = st.beta_columns(2)
col1.image(display, width = 350)
col2.title("Data Visualisation Application")

# Add all your applications (pages) here
app.add_page("1. Data upload page", data_upload_multip.app)
app.add_page("2. Main chart page", main_app_multip.app)
app.add_page("3. Linechart (Comparing to multiple stations)",linechart_app_multip.app)
app.add_page("4. Pollencount on map", pydeck_app_multip.app)
app.add_page("5. Gauge chart", gauge_app_multip.app)
app.add_page("6. Inactive and Missing dates",inactive_dates_app_multip.app)

app.add_page("7. Dashboard page", dashbord_app_multip.app)
#app.add_page("folium map", folium_map_app_multip.app)




# The main app
app.run()
