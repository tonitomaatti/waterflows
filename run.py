import streamlit as st
import datetime
from streamlit_folium import st_folium
import folium
import pandas as pd
import coordinates
from folium.plugins import Draw
import json

preds_df = pd.read_csv("Data/year_predictions.csv", sep=",")
waterflow_df = pd.read_csv("Data/Waterflow Data.csv")

with st.sidebar:
    st.title('WaterFlows')
    date_picker = st.date_input("Select Date", min_value=datetime.date.today(), max_value=datetime.date.today()+datetime.timedelta(days=365))
    toggle_map = st.radio(
        "Map Type",
        ('Color', 'Grey'),
        index=1,
        horizontal=True
    )

if toggle_map == "Color":
    map_tiles = "OpenStreetMap"
else:
    map_tiles = "CartoDB Positron"

m = folium.Map([60.30246404560092, 24.85931396484375], zoom_start=9, tiles=map_tiles)


Draw(export=True).add_to(m)

day_prediction = preds_df[preds_df["date"]==str(date_picker)]["predicted_mean"].values[0]

routes = []
for i in range(0,5):
    with open("Data/Routepoints/routepoints_" + str(i)+ ".geojson") as f:
        routepoints_json = json.load(f)

    color = "grey"
    if day_prediction >= waterflow_df.at[i, "Treshold Easy"]:
        color = "green"
    elif day_prediction >= waterflow_df.at[i, "Treshold Doable"]:
        color = "yellow"
    else:
        color = "red"

    route = folium.GeoJson(routepoints_json, style_function= lambda x: {"color":color, "weight":"5"}).add_to(m)
    routes.append(route)

#st.write(routes[0].data)


#Add route markers

start_coords = waterflow_df[["Route Start GPS N", "Route Start GPS E", "Route Start"]].rename(
    columns={"Route Start GPS N": "N", "Route Start GPS E": "E", "Route Start": "Name"}
    ).to_dict("records")

end_coords = waterflow_df[["Route End GPS N", "Route End GPS E", "Route End"]].rename(
    columns={"Route End GPS N": "N", "Route End GPS E": "E", "Route End": "Name"}
    ).to_dict("records")

coords = start_coords + end_coords

for coord in coords:
    route_name = coord.pop("Name", None)
    coords_wgs84 = coordinates.ETRSTM35FINxy_to_WGS84lalo(coord)
    folium.vector_layers.Circle(
        location=(coords_wgs84["La"], coords_wgs84["Lo"]),
        radius=1,
        popup=None,
        tooltip=route_name,
        weight=5,
        color="black",
        fill_color="purple",
        fill_opacity=1.0
    ).add_to(m)

# call to render Folium map in Streamlit
st_data = st_folium(m)

st.write("Predicted Waterflow: " + str(day_prediction))
st.write("Picked Date: " + str(date_picker))

st.write(waterflow_df[["River","Route Start","Route End", "Treshold Easy", "Treshold Doable"]][0:5])

#if st_data["last_object_clicked"]:
#    st.write("CLICKED OBJECT")

#st.write(st_data)

#st.write("Picked Date: ", date_picker)