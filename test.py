
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
st.text('''Hier zie je een aantal observaties op de y-as en de tijd in uren op de x-as van de 
verbonden tijd. Hierbij zie je dat de meeste observaties onder de 5 uur zitten, dus 
een verbonden tijd van minder dan 5 uur hebben. Dit klopt, want het gemiddelde van 
de verbonden tijd is 5,2 uren. De mediaan ligt ook onder de 5 uren. Aan de 
rechterkant is het mogelijk om met de check box tussen de twee histogrammen 
te switchen. Dit kan voor de verbonden tijd en de oplaadtijd. Bij de histogram 
van de oplaadtijd zie je dat de hoogste piek iets na 2 ligt en dat de meeste 
waarden ook daarvoor liggen. Dit komt ook overeen met de mediaan en het 
gemiddelde. Ook zien we dat de verbonden tijd meer tijd in uren nodig heeft 
dan de oplaadtijd.
Gemiddeld in deze dataset is het zo dat in 65,7% van de tijd de auto's echt aan het 
laden zijn terwijl ze aan de laadpaal staan. Dit betekend dat ongeveer 35% van de tijd
de auto aan de laadpaal staat terwijl deze niet meer oplaad. Dit percentage zou naar 
beneden kunnen om te zorgen dat er meer laadpaal capaciteit is voor andere bestuurders
van elektrische auto's''')

#https://www.kaggle.com/cityapiio/world-cities-average-internet-prices-2010-2020
internet = pd.read_csv('cities_internet_prices_historical.24-10-2021.csv')
#https://www.kaggle.com/sansuthi/gapminder-internet
gap = pd.read_csv('gapminder_internet.csv')

fig, ax = plt.subplots()
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
