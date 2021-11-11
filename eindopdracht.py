
 #!/usr/bin/env python
 # coding: utf-8

 # # Importeren van de packages en files

 # In[1]:
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


 #https://www.kaggle.com/cityapiio/world-cities-average-internet-prices-2010-2020
internet = pd.read_csv('cities_internet_prices_historical.24-10-2021.csv')
 #https://www.kaggle.com/sansuthi/gapminder-internet
gap = pd.read_csv('gapminder_internet.csv')



internet_long=internet.melt(id_vars = ['City', 'Region', 'Country'], var_name = "Year", value_name = "Price")
internet_long.head()



internet_long1 = internet_long[internet_long['Price'] > 0]
internet_long2 = internet_long1[internet_long1['Price'] < 150]


internet_long2.sort_values('Price', ascending = False).head(30)



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

st.plotly_chart(fig)
internet_gap=internet_long2.merge(gap, left_on='Country', right_on='country', how='inner')

fig = px.scatter(data_frame=internet_gap,
                x='incomeperperson',
                y='Price',
                #color='Year',
                trendline='ols',
                #labels={'ChargeTime':'Oplaad tijd [h]', 'TotalEnergy':'Totaal verbruikte energie [Wh]'}, 
                height=600,
                width=1000, 
                title='Relation between price and income'
                )

fig.show()

st.plotly_chart(fig)
fig = px.scatter(data_frame=gap,
                x='incomeperperson',
                y='internetuserate',
                #color='Year',
                trendline='ols',
                #labels={'ChargeTime':'Oplaad tijd [h]', 'TotalEnergy':'Totaal verbruikte energie [Wh]'}, 
                height=600,
                width=1000, 
                title='Relation between income and internet use rate'
                )

fig.show()


fig = px.scatter(data_frame=internet_gap,
                x='internetuserate',
                y='Price',
                color='Country',
                trendline='ols',
                #labels={'ChargeTime':'Oplaad tijd [h]', 'TotalEnergy':'Totaal verbruikte energie [Wh]'}, 
                height=600,
                width=1000, 
                title='Relation between income and internet use rate'
                )

fig.show()


st.plotly_chart(fig)
st.title("Internet prijzen tussen 2010 en 2020")
st.text('''Welkom op ons dashboard! ???????''')
st.header('Internet')
st.subheader('Internet prijzen')
st.text('''In dit figuur is een histogram te zien. In het andere figuur is een boxplot te zien. Met behulp van het dropdown menu is het mogelijk om makkelijk tussen de twee figuren te switchen. De staven van het histogram en de verschillende boxplots zijn van simpel van elkaar te onderscheiden door de diverse kleuren, die gebruikt zijn. Voor beide figuren is gebruik gemaakt van de dataset met gemiddelde internetprijzen per maand per jaar. In deze dataset gaat het om een bereik van heel veel landen, verspreid over de hele wereld. De dataset moest eerst opgeschoond worden, hierbij hebben we de outliers verwijderd en alleen maar naar relevante waarden gekeken.
In het eerste figuur, namelijk de histogram, zijn op de x-as de jaren van 2010 t/m 2020 te zien. Elk jaar heeft een eigen staaf om goed het onderscheid te maken. De y-as geeft de som van de internetprijzen weer. Het valt hierbij op, dat de staven vanaf 2015 aanzienlijk groter zijn, dan van de jaren ervoor. Zo is de staaf van 2018 bijna zeven keer zo groot als de staaf van 2010. Waar het in 2010 ging om een som van 3.500 dollar, gaat het in 2018 om een som van meer dan 24.000 dollar. Waar ligt dit dan aan? Zijn ze internetprijzen zo erg gestegen? Dit enorme verschil komt door het aantal metingen. In de latere jaren zijn simpelweg meer metingen gedaan. Uit deze histogram kunnen we dus geen conclusies trekken. Om een conclusie te kunnen trekken, zouden we de waarden moeten delen door het aantal metingen en dit gemiddelde vergelijken met alle jaren.
In het tweede figuur (te selecteren met de dropdown menu) is de boxplot te zien. Op de x-as zijn de jaren van 2010 t/m 2020 weer af te lezen. Elk jaar heeft een eigen boxplot. Op de y-as is de gemiddelde internetprijs per maand per jaar te zien. Hierbij is te zien, dat de gemiddelde internetprijs door de jaren heen eigenlijk niet echt is gestegen of gedaald. De mediaan van de boxplots komen namelijk overeen met elkaar. Wel is de spreiding gestegen door de jaren heen. Dit geeft aan, dat er aanbieders zijn met hogere en iets lagere internetprijzen. Het maximum is dus gestegen.
'')
