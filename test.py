
import streamlit as st
import folium
import geopandas as gpd
import pandas as pd
from streamlit_folium import folium_static
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import requests
import json
import plotly.figure_factory as ff
import statsmodels.api as sm


st.title("Dashboard over elektrische auto's en laadpalen")
st.text('''Welkom op ons dashboard! Op ons dashboard is te zien hoe een gemiddelde bezetting 
van een laadpaal eruit ziet. Daarnaast zijn er nog veel meer interessante dingen
over laadpalen en elektrische voertuigen.''')
st.header('Laadpaaldata')
st.subheader('Histogram van de laadtijd')
st.text('''hallo''')

#https://www.kaggle.com/cityapiio/world-cities-average-internet-prices-2010-2020
internet = pd.read_csv('cities_internet_prices_historical.24-10-2021.csv')
#https://www.kaggle.com/sansuthi/gapminder-internet
gap = pd.read_csv('gapminder_internet.csv')
internet_long=internet.melt(id_vars = ['City', 'Region', 'Country'], var_name = "Year", value_name = "Price")
internet_long1 = internet_long[internet_long['Price'] > 0]
internet_long2 = internet_long1[internet_long1['Price'] < 150]

fig = px.histogram(internet_long2, x="Year",y='Price', color='Year')

my_buttons = [{'label': "Histogram", 'method': "update", 'args': [{"type": 'histogram'}]},
  {'label': "Boxplot", 'method': "update", 'args': [{"type": 'box', 'mode': 'markers'}]}]

fig.update_layout({
    'updatemenus': [{
      'type':'buttons','direction': 'down',
      'x': 1.15,'y': 0.5,
      'showactive': True, 'active': 0,
      'buttons': my_buttons}]})

fig.update_layout(height=1000, width=1000, title ='Internet prices')
fig.show()

