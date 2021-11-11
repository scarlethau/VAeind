
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

st.title("Internetprijzen in verschillende landen tussen 2010 en 2020")
st.text('''Welkom op ons dashboard! Op ons dashboard is te zien wat 
de correlatie is tussen verschillende variabelen en de gemiddelde
internetprijzen in verschillende landen zijn tussen 2010 en 2020.''')
st.header('Internet prijzen')
st.subheader('Histogram en boxplot van de prijzen per jaar')
st.text('''In dit figuur is een histogram te zien. In het andere figuur is een boxplot 
te zien. Met behulp van het dropdown menu is het mogelijk om makkelijk tussen 
de twee figuren te switchen. De staven van het histogram en de verschillende 
boxplots zijn van simpel van elkaar te onderscheiden door de diverse kleuren, 
die gebruikt zijn. Voor beide figuren is gebruik gemaakt van de dataset met
gemiddelde internetprijzen per maand per jaar. In deze dataset gaat het om 
een bereik van heel veel landen, verspreid over de hele wereld. De dataset 
moest eerst opgeschoond worden, hierbij hebben we de outliers verwijderd
en alleen maar naar relevante waarden gekeken.
In het eerste figuur, namelijk de histogram, zijn op de x-as de jaren van 
2010 t/m 2020 te zien. Elk jaar heeft een eigen staaf om goed het 
onderscheid te maken. De y-as geeft de som van de internetprijzen weer. 
Het valt hierbij op, dat de staven vanaf 2015 aanzienlijk groter zijn, 
dan van de jaren ervoor. Zo is de staaf van 2018 bijna zeven keer zo groot 
als de staaf van 2010. Waar het in 2010 ging om een som van 3.500 dollar, 
gaat het in 2018 om een som van meer dan 24.000 dollar. Waar ligt dit dan 
aan? Zijn ze internetprijzen zo erg gestegen? Dit enorme verschil komt 
door het aantal metingen. 
In de latere jaren zijn simpelweg meer metingen gedaan. Uit deze histogram 
kunnen we dus geen conclusies trekken. Om een conclusie te kunnen trekken, 
zouden we de waarden moeten delen door het aantal metingen en dit gemiddelde 
vergelijken met alle jaren.In het tweede figuur (te selecteren met de dropdown)
is de boxplot te zien. Op de x-as zijn de jaren van 2010 t/m 2020 weer af te
lezen. Elk jaar heeft een eigen boxplot. Op de y-as is de gemiddelde 
internetprijs per maand per jaar te zien. Hierbij is te zien, dat de 
gemiddelde internetprijs door de jaren heen eigenlijk niet echt is gestegen
of gedaald. De mediaan van de boxplots komen namelijk overeen met elkaar.
Wel is de spreiding gestegen door de jaren heen. Dit geeft aan, dat er 
aanbieders zijn met hogere en iets lagere internetprijzen.
Het maximum is dus gestegen.
''')

 #https://www.kaggle.com/cityapiio/world-cities-average-internet-prices-2010-2020
internet = pd.read_csv('cities_internet_prices_historical.24-10-2021.csv')
 #https://www.kaggle.com/sansuthi/gapminder-internet
gap = pd.read_csv('gapminder_internet.csv')
#https://www.kaggle.com/i2i2i2/cities-of-the-world

internet = internet.rename(columns={"Internet Price, 2010": "2010", 
                                    "Internet Price, 2011": "2011",
                                    "Internet Price, 2012": "2012", 
                                    "Internet Price, 2013": "2013",
                                    "Internet Price, 2014": "2014", 
                                    "Internet Price, 2015": "2015",
                                    "Internet Price, 2016": "2016", 
                                    "Internet Price, 2017": "2017",
                                    "Internet Price, 2018": "2018", 
                                    "Internet Price, 2019": "2019",
                                    "Internet Price, 2020": "2020"})

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

st.header('Verband tussen het inkomen en de prijzen per BNP per hoofd ')
st.text('''In het onderstaande figuur is een scatterplot te zien. Deze 
scatterplot is tot stand gekomen door een nieuwe dataset in ons bestand
toe te voegen en deze te mergen (samenvoegen) met onze andere dataset,
namelijk die over de internetprijzen. De nieuwe dataset laat onder andere
het gemiddelde inkomen per persoon per jaar zien. We zijn hierop gekomen,
omdat we een correlatie tussen het gemiddelde inkomen per persoon en de 
gemiddelde internetprijs wilden maken. Op de x-as van dit figuur is het 
gemiddelde inkomen per persoon per jaar te zien. Op de y-as is de 
gemiddelde internetprijs per maand per jaar te zien. Ondanks, dat dit
niet de meest overzichtelijke scatterplot is, kunnen we dankzij de 
trendlijn wel een correlatie eruit halen. Hoe hoger het inkomen is, 
hoe hoger de internetprijs. Over het algemeen gezien dan. Zo heb je bij 
het gemiddelde inkomen tussen de 20.000 en 40.000 dollar alsnog mensen
die het duurste internetpakket hebben. De correlatie zegt dus niet alles.''') 


fig = go.Figure()
for col in ['incomeperperson', 'internetuserate']:
    fig.add_trace(go.Scatter(x=internet_gap[col], y=internet_gap['Price'], mode='markers'))

my_buttons = [{'label': 'Income - Price', 'method': 'update',
    'args': [{'visible': [True, False]},
            {'title': 'Verband tussen inkomen en prijs'}]},
    {'label': 'Usage - Price', 'method': 'update',
    'args': [{'visible': [False, True]},
            {'title': 'Verband tussen internet gebruik en prijs'}]}]

fig.update_layout({
    'updatemenus': [{
      'type':'buttons','direction': 'down',
      'x': 1.3,'y': 0.5,
      'showactive': True, 'active': 0,
      'buttons': my_buttons}]})    
fig.update_layout(xaxis_title='BNP per hoofd [USD]',
                  yaxis_title="Prijs [USD]",
                  title = 'Verband tussen inkomen en prijs')
fig.data[1].visible=False
fig.show()   


st.plotly_chart(fig)




fig = px.scatter(data_frame=internet_gap,
                x='incomeperperson',
                y='Price',
                #color='Country',
                trendline='ols', 
                height=600,
                width=1000, 
                )

fig.update_layout(xaxis_title='BNP per hoofd [USD]',
                  yaxis_title="Prijs [USD]",
                  title = 'Verband tussen inkomen en prijs')
                
fig.show()
st.plotly_chart(fig)


st.header('Verband tussen het inkomen en de prijzen per BNP per hoofd ')
st.text('''In''')


fig = px.scatter(data_frame=internet_gap,
                x='internetuserate',
                y='Price',
                #color='Country',
                trendline='ols',
                #labels={'ChargeTime':'Oplaad tijd [h]', 'TotalEnergy':'Totaal verbruikte energie [Wh]'}, 
                height=600,
                width=1000, 
                title='Relation between income and internet use rate'
                )

fig.update_layout(xaxis_title='Internet gebruikers per 100 inwoners',
                  yaxis_title="Prijs [USD]",
                  title = 'Internet gebruiker per 100 inwoners en prijs')
                
fig.show()
st.plotly_chart(fig)

st.header('Verband tussen het inkomen en de prijzen per BNP per hoofd ')
st.text('''In''')


fig = px.scatter(data_frame=internet_gap,
                x='internetuserate',
                y='incomeperperson',
                trendline='ols', 
                height=600,
                width=1000, 
                title='Relation between income and internet use rate'
                )

fig.update_layout(xaxis_title='Internet gebruikers per 100 inwoners',
                  yaxis_title="BNP per hoofd [USD]",
                  title = 'Verband tussen internetgebruik en inkomen')
                
fig.show()
st.plotly_chart(fig)

