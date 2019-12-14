#!/usr/bin/env python
# coding: utf-8

# # Week 3 Assignment

# Import libraries

# In[3]:


import numpy as np 

import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

import json # library to handle JSON files

import requests # library for requests
from pandas.io.json import json_normalize # JSON to pandas handling

# import Beautiful Soup for scraping 
from bs4 import BeautifulSoup

import xml

print('Imports completed.')


# Import data

# In[4]:


url = requests.get('https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M').text
soup = BeautifulSoup(url,'lxml')


# Find and Display Table

# In[5]:


table_post = soup.find('table')
fields = table_post.find_all('td')

postcode = []
borough = []
neighbourhood = []

for i in range(0, len(fields), 3):
    postcode.append(fields[i].text.strip())
    borough.append(fields[i+1].text.strip())
    neighbourhood.append(fields[i+2].text.strip())
        
df_pcode = pd.DataFrame(data=[postcode, borough, neighbourhood]).transpose()
df_pcode.columns = ['Postcode', 'Borough', 'Neighbourhood']
df_pcode.head()


# Remove 'not assigned'

# In[6]:


df_pcode['Borough'].replace('Not assigned', np.nan, inplace=True)
df_pcode.dropna(subset=['Borough'], inplace=True)

df_pcode.head()


# In[7]:


df_pcn = df_pcode.groupby(['Postcode', 'Borough'])['Neighbourhood'].apply(', '.join).reset_index()
df_pcn.columns = ['Postcode', 'Borough', 'Neighbourhood']
df_pcn


# In[8]:


df_pcn['Neighbourhood'].replace('Not assigned', "Queen's Park", inplace=True)
df_pcn


# In[7]:


df_pcn.shape


# Add additional libraries

# In[1]:


get_ipython().system('conda install -c conda-forge geopy --yes ')
from geopy.geocoders import Nominatim # convert an address to Lat/Long format

import requests # requests library
from pandas.io.json import json_normalize # tranform JSON file to pandas df

# Plotting modules
import matplotlib.cm as cm
import matplotlib.colors as colors

get_ipython().system('conda install -c conda-forge folium=0.5.0 --yes ')
import folium # map rendering library

print('Libraries loaded.')


# Merge lat/long data with Wiki data

# In[9]:


df_ltlg = pd.read_csv('http://cocl.us/Geospatial_data')
df_ltlg.columns = ['Postcode', 'Latitude', 'Longitude']

df_pos = pd.merge(df_pcn, df_ltlg, on=['Postcode'], how='inner')

df_tor = df_pos[['Borough', 'Neighbourhood', 'Postcode', 'Latitude', 'Longitude']].copy()

df_tor.head()


# Load map info

# In[10]:


address = 'Toronto, Canada'

geolocator = Nominatim()
location = geolocator.geocode(address)
latitude = location.latitude
longitude = location.longitude


# In[11]:


# create map of Toronto
map_toronto = folium.Map(location=[latitude, longitude], zoom_start=10)

# mark map
for lat, lng, borough, neighborhood in zip(df_tor['Latitude'], df_tor['Longitude'], df_tor['Borough'], df_tor['Neighbourhood']):
    label = '{}, {}'.format(neighborhood, borough)
    label = folium.Popup(label, parse_html=True)
    folium.CircleMarker(
        [lat, lng],
        radius=3,
        popup=label,
        color='green',
        fill=True,
        fill_color='#3199cc',
        fill_opacity=0.3,
        parse_html=False).add_to(map_toronto)  
    
map_toronto


# In[ ]:




