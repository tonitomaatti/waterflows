import streamlit as st
import datetime

st.title('WaterFlows')

with st.sidebar:
    date_picker = st.date_input("Select Date", min_value=datetime.date.today(), max_value=datetime.date.today()+datetime.timedelta(days=365))

st.write("Picked Date: ", date_picker)
st.write("Conda Forge version")
