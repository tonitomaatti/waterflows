import streamlit as st
import datetime

st.title('WaterFlows')

st.date_input("Select Date", min_value=datetime.date.today(), max_value=datetime.date.today()+datetime.timedelta(days=365))