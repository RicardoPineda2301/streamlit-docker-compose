import streamlit as st
import pandas as pd
import numpy as np
from streamlit import cache
import altair as alt
import pydeck as pdk
import altair as alt

from sqlalchemy import create_engine

# create sqlalchemy engine
engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                       .format(user="root",
                               pw="Bruno14",
                               db="finaldp"))


#df = pd.read_csv("proyecto/time_series_covid19_confirmed_global.csv").rename(columns= {'Lat': 'lat', 'Long': 'lon'})

df = pd.read_sql_table('confirmado', engine).rename(columns= {'Lat': 'lat', 'Lon': 'lon'})
df2 = pd.read_sql_table('muertes', engine).rename(columns= {'Lat': 'lat', 'Lon': 'lon'})
df3 = pd.read_sql_table('recuperados', engine).rename(columns= {'Lat': 'lat', 'Lon': 'lon'})

#data = df.melt(id_vars=['Provincia', 'Pais', 'lat', 'lon'], var_name='Fecha', value_name='Casos')
data = df.copy()
data2 = df2.copy()
data3 = df3.copy()

data['Fecha'] =  pd.to_datetime(data['Fecha'])
data2['Fecha'] =  pd.to_datetime(data2['Fecha'])
data3['Fecha'] =  pd.to_datetime(data3['Fecha'])
# Variables
DATE_TIME = "Fecha"


st.title("Casos de coronavirus")

hour_selected = st.date_input("Seleccione fecha",data['Fecha'].min(),  data['Fecha'].min(), data['Fecha'].max())

paises = st.multiselect(
     '¿Qué países es?',
     df['Pais'].unique())




st.write(
    """Gráfica de casos confirmados de coronavirus en el mundo
    """)


    
mostrar = data[data[DATE_TIME] == hour_selected.isoformat()]
if len(paises) > 0:
    mostrar = mostrar[mostrar.Pais.isin(paises)]


# Set viewport for the deckgl map
view = pdk.ViewState(latitude=0, longitude=0, zoom=0.2,)

# Create the scatter plot layer
covidLayer = pdk.Layer(
        "ScatterplotLayer",
        data=mostrar[['Casos', 'lat', 'lon']],
        pickable=False,
        opacity=0.3,
        stroked=True,
        filled=True,
        radius_scale=10,
        radius_min_pixels=2,
        radius_max_pixels=25,
        line_width_min_pixels=1,
        get_position=["lon", "lat"],
        get_radius='Casos',
        get_fill_color=[252, 136, 3],
        get_line_color=[255,0,0],
        tooltip="test test"
    )



# Create the deck.gl map
r = pdk.Deck(
    layers=[covidLayer],
    initial_view_state=view,
    map_style="mapbox://styles/mapbox/light-v10",
)


map = st.pydeck_chart(r)

# Create a subheading to display current date
subheading = st.subheader("Tendencia de casos confirmados")

# Render the deck.gl map in the Streamlit app as a Pydeck chart 



mostrar2 = data.copy()
if len(paises) > 0:
    mostrar2 = mostrar2[mostrar2.Pais.isin(paises)]
    
c = alt.Chart(mostrar2.groupby(by=['Pais', 'Fecha'], as_index=False).agg({'Casos': 'sum'})).mark_circle().encode(y='Pais', x='Fecha', size='Casos', color='Pais', tooltip=['Pais', 'Fecha', 'Casos'])

st.altair_chart(c, use_container_width=True)

#st.line_chart(data.groupby(by=['Pais', 'Fecha'], as_index=False).agg({'Casos': 'sum'}))
st.write(
    """Gráfica de muertes por coronavirus en el mundo
    """)

mostrar3 = data2[data2[DATE_TIME] == hour_selected.isoformat()]
mostrar4 = data3[data3[DATE_TIME] == hour_selected.isoformat()]
if len(paises) > 0:
    mostrar3 = mostrar3[mostrar3.Pais.isin(paises)]
    mostrar4 = mostrar4[mostrar4.Pais.isin(paises)]

# Create the scatter plot layer
covidLayer2 = pdk.Layer(
        "ScatterplotLayer",
        data=mostrar3[['Casos', 'lat', 'lon']],
        pickable=False,
        opacity=0.3,
        stroked=True,
        filled=True,
        radius_scale=10,
        radius_min_pixels=1,
        radius_max_pixels=25,
        line_width_min_pixels=1,
        get_position=["lon", "lat"],
        get_radius='Casos',
        get_fill_color=[220, 20, 60],
        get_line_color=[222,20,60],
        tooltip="test test"
    )

covidLayer3 = pdk.Layer(
        "ScatterplotLayer",
        data=mostrar4[['Casos', 'lat', 'lon']],
        pickable=False,
        opacity=0.3,
        stroked=True,
        filled=True,
        radius_scale=10,
        radius_min_pixels=1,
        radius_max_pixels=25,
        line_width_min_pixels=1,
        get_position=["lon", "lat"],
        get_radius='Casos',
        get_fill_color=[50,205,50],
        get_line_color=[0,128,0],
        tooltip="test test"
    )


# Create the deck.gl map
r2 = pdk.Deck(
    layers=[covidLayer2, covidLayer3],
    initial_view_state=view,
    map_style="mapbox://styles/mapbox/light-v10",
)

map = st.pydeck_chart(r2)



