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

# In[2]:


#https://www.kaggle.com/cityapiio/world-cities-average-internet-prices-2010-2020
internet = pd.read_csv('cities_internet_prices_historical.24-10-2021.csv')
#https://www.kaggle.com/sansuthi/gapminder-internet
gap = pd.read_csv('gapminder_internet.csv')


# # Datasets bekijken

# ### Internet dataset

# In[3]:


internet.head()
#per maand, per prijs, per land


# In[4]:


#internet.info()


# In[5]:


# zoeken naar kolommen met missing values
internet.isna().sum().loc[lambda x:x > 0]


# In[6]:


#internet.dropna(inplace=True) , niet nodig


# In[7]:


# Zoeken naar duplicates in kolom 'City'
internet.value_counts('City').loc[lambda s:s > 1].sort_values(ascending = False)


# In[8]:


# duplicate citys beter bekijken
print(internet.loc[internet.City == "London",["City","Region","Country"]])
#Alles mag blijven, geen duplicates gevonden


# In[9]:


#internet['Country'].nunique()


# ### gap dataset

# In[10]:


#gap.head()


# In[11]:


#gap.info()


# In[12]:


#gap.isna().sum().loc[lambda x:x > 0]
#word later d.m.v. een merge gefilterd


# In[13]:


gap['incomeperperson'].describe()


# # Outliers bekijken
#Namen van de kolommen aanpassen
internet = internet.rename(columns={"Internet Price, 2010": "2010", 
                                    "Internet Price, 2011": "2011",
                                    "Internet Price, 2012": "2012", 
                                    "Internet Price, 2013": "2013"})
#internet.head(1)
# In[14]:


#Naar long format omzetten
internet_long=internet.melt(id_vars = ['City', 'Region', 'Country'], var_name = "Year", value_name = "Price")
internet_long.head()


# In[15]:


#fig, ax = plt.subplots()
#ax.boxplot([internet_long["Price"]])
#ax.set_xticklabels(["Pijs])
#ax.set_ylabel("Internet prijs")
#ax.set_title("Verdeling van internetprijs")
#plt.show()


# In[16]:


#internet_long['Price'].hist()
#plt.title('Internet prijzen')
#plt.xlabel('Internet prijs')
#plt.ylabel('Frequentie')
#plt.show()


# In[17]:


internet_long1 = internet_long[internet_long['Price'] > 0]
internet_long2 = internet_long1[internet_long1['Price'] < 150]


# In[31]:


#gap.head()


# In[39]:


#fig, ax = plt.subplots()
#ax.boxplot([gap["incomeperperson"]])
#ax.set_xticklabels(["Pijs])
#ax.set_ylabel("Internet prijs")
#ax.set_title("Verdeling van internetprijs")
#plt.show()


# In[19]:


#gap['incomeperperson'].hist()
#plt.title('Internet prijzen')
#plt.xlabel('Internet prijs')
#plt.ylabel('Frequentie')
#plt.show()


# In[20]:


#print(internet_long2.shape)
internet_long2.sort_values('Price', ascending = False).head(30)


# # plots

# In[21]:


#internet_long2['Year'].value_counts()


# In[22]:


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


# In[23]:


internet_gap=internet_long2.merge(gap, left_on='Country', right_on='country', how='inner')
print(internet_gap.shape)
internet_gap.head()


# In[24]:


internet_gap["incomeperperson"].nunique()


# In[25]:


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


# In[26]:


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


# In[27]:


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


# In[40]:


def add_categorical_legend(folium_map, title, colors, labels):
    if len(colors) != len(labels):
        raise ValueError("colors and labels must have the same length.")

    color_by_label = dict(zip(labels, colors))
    
    legend_categories = ""     
    for label, color in color_by_label.items():
        legend_categories += f"<li><span style='background:{color}'></span>{label}</li>"
        
    legend_html = f"""
    <div id='maplegend' class='maplegend'>
      <div class='legend-title'>{title}</div>
      <div class='legend-scale'>
        <ul class='legend-labels'>
        {legend_categories}
        </ul>
      </div>
    </div>
    """
    script = f"""
        <script type="text/javascript">
        var oneTimeExecution = (function() {{
                    var executed = false;
                    return function() {{
                        if (!executed) {{
                             var checkExist = setInterval(function() {{
                                       if ((document.getElementsByClassName('leaflet-top leaflet-right').length) || (!executed)) {{
                                          document.getElementsByClassName('leaflet-top leaflet-right')[0].style.display = "flex"
                                          document.getElementsByClassName('leaflet-top leaflet-right')[0].style.flexDirection = "column"
                                          document.getElementsByClassName('leaflet-top leaflet-right')[0].innerHTML += `{legend_html}`;
                                          clearInterval(checkExist);
                                          executed = true;
                                       }}
                                    }}, 100);
                        }}
                    }};
                }})();
        oneTimeExecution()
        </script>
      """
   

    css = """

    <style type='text/css'>
      .maplegend {
        z-index:9999;
        float:right;
        background-color: rgba(255, 255, 255, 1);
        border-radius: 5px;
        border: 2px solid #bbb;
        padding: 10px;
        font-size:12px;
        positon: relative;
      }
      .maplegend .legend-title {
        text-align: left;
        margin-bottom: 5px;
        font-weight: bold;
        font-size: 90%;
        }
      .maplegend .legend-scale ul {
        margin: 0;
        margin-bottom: 5px;
        padding: 0;
        float: left;
        list-style: none;
        }
      .maplegend .legend-scale ul li {
        font-size: 80%;
        list-style: none;
        margin-left: 0;
        line-height: 18px;
        margin-bottom: 2px;
        }
      .maplegend ul.legend-labels li span {
        display: block;
        float: left;
        height: 16px;
        width: 30px;
        margin-right: 5px;
        margin-left: 0;
        border: 0px solid #ccc;
        }
      .maplegend .legend-source {
        font-size: 80%;
        color: #777;
        clear: both;
        }
      .maplegend a {
        color: #777;
        }
    </style>
    """

    folium_map.get_root().header.add_child(folium.Element(script + css))

    return folium_map


# In[41]:


#m = folium.Map()

#m = add_categorical_legend(m, 'prijsverschil',
                   #        colors = ["lightblue"],
                 #          labels = ['Verschil'])

#for row in internet_nieuw.iterrows():
  #  row_values = row[1]
   # location = [row_values['Latitude'], row_values['Longitude']]
   # marker = folium.Marker(location = location,
         #                popup = row_values['Verschil'])
   # marker.add_to(m)


#m

