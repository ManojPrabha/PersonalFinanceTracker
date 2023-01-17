###############################################################################
###############################################################################
# Manoj's Personal Finance Tracker
# Created: January 15, 2023
# Last Updated: January 15, 2023
# Version: 1.0
# Changes:
# v1.0 - added multi-page support
###############################################################################
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
import matplotlib.pyplot as plt
import xlrd
import time

st.title ("this is the app title")
st.header("this is the markdown")
st.markdown("this is the header")
st.subheader("this is the subheader")
st.caption("this is the caption")
st.code("x=2021")
st.latex(r''' a+a r^1+a r^2+a r^3 ''')

st.subheader("Image:")
st.image("Peronal.jpg")
st.subheader("Audio:")
st.audio("Jubin Nautiyal New Supehit Songs 2021 Audio Jukebox Jubin Nautiyal All Hindi Nonstop Songs New Song.mp3")
st.subheader("Video:")
st.video("saedar.mkv")

st.checkbox('yes')
st.button('Click')
st.radio('Pick your gender',['Male','Female'])
st.selectbox('Pick your gender',['Male','Female'])
st.multiselect('choose a planet',['Jupiter', 'Mars', 'neptune'])
st.select_slider('Pick a mark', ['Bad', 'Good', 'Excellent'])
st.slider('Pick a number', 0,50)

st.number_input('Pick a number', 0,10)
st.text_input('Email address')
st.date_input('Travelling date')
st.time_input('School time')
st.text_area('Description')
st.file_uploader('Upload a photo')
st.color_picker('Choose your favorite color')

st.balloons()
st.progress(10)
with st.spinner('Wait for it...'):
    time.sleep(1)


st.success("You did it !")
st.error("Error")
st.warning("Warning")
st.info("It's easy to build a streamlit app")
st.exception(RuntimeError("RuntimeError exception"))

st.sidebar.title("title")
#st.sidebar.button("Click")
st.sidebar.radio("Pick",["male","femalefemale"])

container = st.container()
container.write("Container context")
st.write("outside")

rand=np.random.normal(1, 2, size=20)
fig, ax = plt.subplots()
ax.hist(rand, bins=15)
st.pyplot(fig)