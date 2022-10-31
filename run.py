import streamlit as st
import datetime
from streamlit_folium import st_folium
import folium
import pandas as pd
import coordinates
from folium.plugins import Draw
import json

st.title('WaterFlows')

with st.sidebar:
    date_picker = st.date_input("Select Date", min_value=datetime.date.today(), max_value=datetime.date.today()+datetime.timedelta(days=365))

m = folium.Map([60.30246404560092, 24.85931396484375], zoom_start=9)

#Draw Lines
#points = [(60.181733310424505, 24.927388429641727), (60.18644904112918, 24.927141666412357)]
#folium.PolyLine(points, color="red", weight=3).add_to(m)
#Draw(export=True).add_to(m)
with open("Data/Routepoints/routepoints_1.geojson") as f:
    routepoints_json = json.load(f)

#Add all coordinates together
routepoints = []
for points in routepoints_json["features"]:
    routepoints = routepoints + [(point[1], point[0]) for point in points["geometry"]["coordinates"]]

folium.PolyLine(routepoints, color="red", weight=10).add_to(m)


#Add route markers
df = pd.read_csv("Data/Waterflow Data.csv")
start_coords = df[["Route Start GPS N", "Route Start GPS E", "Route Start"]].rename(
    columns={"Route Start GPS N": "N", "Route Start GPS E": "E", "Route Start": "Name"}
    ).to_dict("records")

end_coords = df[["Route End GPS N", "Route End GPS E", "Route End"]].rename(
    columns={"Route End GPS N": "N", "Route End GPS E": "E", "Route End": "Name"}
    ).to_dict("records")

coords = start_coords + end_coords

for coord in coords:
    route_name = coord.pop("Name", None)
    coords_wgs84 = coordinates.ETRSTM35FINxy_to_WGS84lalo(coord)
    folium.Marker(
        [coords_wgs84["La"], coords_wgs84["Lo"]], popup=None, tooltip=route_name
    ).add_to(m)

# call to render Folium map in Streamlit
st_data = st_folium(m, width = 1200, height = 1000)

st.write(st_data)

#st.write("Picked Date: ", date_picker)
#st.write("Conda Forge version")