

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




internet = pd.read_csv('cities_internet_prices_historical.24-10-2021.csv')

gap = pd.read_csv('gapminder_internet.csv')

city = pd.read_csv('cities15000.csv')


internet.isna().sum().loc[lambda x:x > 0]


gap.isna().sum().loc[lambda x:x > 0]



city.drop(city.iloc[:, 6:20], inplace = True, axis = 1)
city.drop(city.columns[[0,1,3]], axis = 1, inplace = True)


city.isna().sum().loc[lambda x:x > 0]


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


st.plotly_chart(fig)


internet_gap=internet_long2.merge(gap, left_on='Country', right_on='country', how='inner')


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
 
st.plotly_chart(fig)



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
                  title = 'Internet gebruikers per 100 inwoners en prijs')

st.plotly_chart(fig)


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


st.plotly_chart(fig)



internet_wide = internet_long2.pivot(index=['City', 'Region', 'Country'], columns='Year', values='Price')
internet_wide.reset_index(level=0, inplace=True)



internet_city= internet_wide.merge(city, left_on='City', right_on='asciiname', how='inner')


internet_city2=internet_city.dropna(subset= ['latitude' , 'longitude', '2010', '2020'])

internet_city2['Verschil'] = internet_city2["2020"] - internet_city2["2010"]


