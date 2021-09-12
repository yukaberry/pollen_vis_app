import numpy as np
import pandas as pd
import streamlit as st

# image1,image2,image3 = st.beta_columns(3)

# with image1:
#     st.header("cereale")
#     st.image("images/cereale_secale.jpg")

# with image2:
#     st.header("grass")
#     st.image("images/grass_poaceae.jpg")

# with image3:
#     st.header("herb")
#     st.image("images/herb_artemisia.png")    
def app():

    st.write('')
    row1_space1, row1_1, row1_space2, row1_2, row1_space3 = st.beta_columns(
    (.15, 1, .3, 1, .00000001))

    with row1_1:
        st.subheader("Pollen Info")
        st.image("images/herb_artemisia.png",width=300)

    with row1_2:
        lname="Artemisia"
        gname ="Beifuß"
        risk = "200-300 medium risk\n300-400 high risk"
        season = "Spring"
        ptype = "Grass"


        st.subheader(' ')
        st.text(' ')
        st.text(
            f"Latin Name: {lname}"
        )
        st.text(
            f"German Name: {gname}"
        )
        st.text(
            f"Risk Level: {risk}"
        )
        st.text(
            f"High Season: {season}"
        )
        st.text(
            f"Types: {ptype}"
        )


