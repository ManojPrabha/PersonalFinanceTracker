import streamlit as st
import app
import settings



###############################################################################
##Webpage Setup
# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Personal Finance Tracker",
	page_icon="🦈",
	layout="wide")

# Define functions for each page
def page_one():
    app.main()

def page_two():
    settings.main()


# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Upload & Analyze", "Settings"])

# Render the selected page
if page == "Upload & Analyze":
    page_one()
elif page == "Settings":
    page_two()