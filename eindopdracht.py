#!/usr/bin/env python
# coding: utf-8

# # Importeren van de packages en files

# In[42]:

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
#https://www.kaggle.com/i2i2i2/cities-of-the-world
city = pd.read_csv('cities15000.csv')


# # Datasets bekijken

# ### Internet dataset

# In[3]:


#internet.head()
#per maand, per prijs, per land


# In[4]:


#internet.info()


# In[5]:


# zoeken naar kolommen met missing values
#internet.isna().sum().loc[lambda x:x > 0]


# In[6]:


#internet.dropna(inplace=True) , niet nodig


# In[7]:


# Zoeken naar duplicates in kolom 'City'
#internet.value_counts('City').loc[lambda s:s > 1].sort_values()


# In[8]:


# duplicate citys beter bekijken
#print(internet.loc[internet.City == "London",["City","Region","Country"]])
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


#gap['incomeperperson'].describe()


# ### City dataset

# In[14]:


#city.head()


# In[15]:


#city.info()


# In[16]:


#verwijderen van irrelevante kolommen
city.drop(city.iloc[:, 6:20], inplace = True, axis = 1)
city.drop(city.columns[[0,1,3]], axis = 1, inplace = True)
city.info()


# In[17]:


# zoeken naar kolommen met missing values
city.isna().sum().loc[lambda x:x > 0]


# # Outliers bekijken

# In[18]:


#Namen van de kolommen aanpassen
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
#internet.head(1)


# In[19]:


#Naar long format omzetten
internet_long=internet.melt(id_vars = ['City', 'Region', 'Country'], var_name = "Year", value_name = "Price")
internet_long.head()


# In[20]:


#fig, ax = plt.subplots()
#ax.boxplot([internet_long["Price"]])
#ax.set_xticklabels(["Pijs])
#ax.set_ylabel("Internet prijs")
#ax.set_title("Verdeling van internetprijs")
#plt.show()

#st.plotly_chart(fig)

# In[21]:


#internet_long['Price'].hist()
#plt.title('Internet prijzen')
#plt.xlabel('Internet prijs')
#plt.ylabel('Frequentie')
#plt.show()


# In[22]:


internet_long1 = internet_long[internet_long['Price'] > 0]
internet_long2 = internet_long1[internet_long1['Price'] < 150]


# In[23]:


#fig, ax = plt.subplots()
#ax.boxplot([gap["incomeperperson"]])
#ax.set_xticklabels(["Pijs])
#ax.set_ylabel("Internet prijs")
#ax.set_title("Verdeling van internetprijs")
#plt.show()


# In[24]:


#gap['incomeperperson'].hist()
#plt.title('Internet prijzen')
#plt.xlabel('Internet prijs')
#plt.ylabel('Frequentie')
#plt.show()


# In[25]:


#print(internet_long2.shape)
#internet_long2.sort_values('Price', ascending = False).head(30)


# In[26]:


internet_long2.isna().sum()


# # Plots

# In[27]:


#internet_long2['Year'].value_counts()


# In[28]:


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

# In[29]:


internet_gap=internet_long2.merge(gap, left_on='Country', right_on='country', how='inner')
#print(internet_gap.shape)
#internet_gap.head()


# In[30]:


#internet_gap["incomeperperson"].nunique()


# In[31]:


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

# In[32]:


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

# In[33]:


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
                
fig.show()

st.plotly_chart(fig)
# In[34]:


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
# In[35]:


# Omzetten naar wide format
internet_wide = internet_long2.pivot(index=['City', 'Region', 'Country'], columns='Year', values='Price')
internet_wide.reset_index(level=0, inplace=True)
#internet_wide.head()


# In[36]:


#Merge voor coordinaten per stad
internet_city= internet_wide.merge(city, left_on='City', right_on='asciiname', how='inner')
#print(internet_city.shape)
#internet_city.head()


# In[37]:


internet_city2=internet_city.dropna(subset= ['latitude' , 'longitude', '2010', '2020'])
#print(internet_city2.shape)
#internet_city2.head()


# In[38]:


internet_city2['Verschil'] = internet_city2["2020"] - internet_city2["2010"]
#print(internet_city2.shape)
#internet_city2.head(1)


# In[44]:


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


# In[45]:


m = folium.Map()

m = add_categorical_legend(m, 'prijsverschil',
                           colors = ['green'],
                           labels = ['Verschil internetprijs tussen 2010 en 2020'])

for row in internet_city2.iterrows():
    row_values = row[1]
    location = [row_values['latitude'], row_values['longitude']]
    marker = folium.Marker(location = location,
                           popup = row_values['Verschil'],
                           icon = folium.Icon(icon='glyphicon glyphicon-usd', color = 'green'),
                           legend=True,
                           radius = 25,
                           draggable = True,
                           tooltip = 'Klik om het verschil te zien')
                    
    
    
    marker.add_to(m)


m

