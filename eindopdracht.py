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
