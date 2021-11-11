
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

fig = plt.subplots()
ax.boxplot([internet_long["Price"]])
#ax.set_xticklabels(["Pijs])
ax.set_ylabel("Internet prijs")
ax.set_title("Verdeling van internetprijs")
plt.show()

internet_long['Price'].hist()
plt.title('Internet prijzen')
plt.xlabel('Internet prijs')
plt.ylabel('Frequentie')
plt.show()
