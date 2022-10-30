import streamlit as st
import datetime
from streamlit_folium import st_folium
import folium

st.title('WaterFlows')

with st.sidebar:
    date_picker = st.date_input("Select Date", min_value=datetime.date.today(), max_value=datetime.date.today()+datetime.timedelta(days=365))

m = folium.Map([60.249999, 24.499998], zoom_start=10)

# call to render Folium map in Streamlit
st_data = st_folium(m, width = 1500, height=800)


st.write("Picked Date: ", date_picker)
st.write("Conda Forge version")