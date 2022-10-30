import streamlit as st
import datetime
from streamlit_folium import st_folium
import folium
import pandas as pd
import coordinates

st.title('WaterFlows')

with st.sidebar:
    date_picker = st.date_input("Select Date", min_value=datetime.date.today(), max_value=datetime.date.today()+datetime.timedelta(days=365))

m = folium.Map([60.249999, 24.499998], zoom_start=10)

#Draw Lines
points = [(60.181733310424505, 24.927388429641727), (60.18644904112918, 24.927141666412357)]
folium.PolyLine(points, color="red", weight=3).add_to(m)

#Add route markers
df = pd.read_csv("Waterflow Data.csv")
coords = df[["Route Start GPS N", "Route Start GPS E"]].rename(columns={"Route Start GPS N": "N", "Route Start GPS E": "E"}).to_dict("records")

for coord in coords:
    coords_wgs84 = coordinates.ETRSTM35FINxy_to_WGS84lalo(coord)
    folium.Marker(
        [coords_wgs84["La"], coords_wgs84["Lo"]]
    ).add_to(m)

# call to render Folium map in Streamlit
st_data = st_folium(m, width = 800)

st.write(st_data)

#st.write("Picked Date: ", date_picker)
#st.write("Conda Forge version")