#!/usr/bin/env python
# coding: utf-8

# # Importujemy dane

# In[9]:


import geopandas  #pd.merge(product,customer,left_on='Product_name',right_on='Purchased_Product')
import pandas as pd
import requests  
from bs4 import BeautifulSoup # PARSE HTML

path_to_data = ("C:/Users/kzeba/OneDrive/Pulpit/DANE/Polska dane/Wojewodztwa/Województwa.shp")
gdf = geopandas.read_file(path_to_data)


# In[10]:


wikiurl="https://pl.wikipedia.org/wiki/Wojew%C3%B3dztwo" #ADRES URL STRONY
table_class="wikitable sortable jquery-tablesorter" #ZBADAJ STRONĘ, POSZUKAJ TABELI(KLASY)
response=requests.get(wikiurl) #ad1
print(response.status_code)


# # html into a beautifulsoup object

# In[11]:


soup = BeautifulSoup(response.text, 'html.parser')
wojewodztwatable=soup.find('table',{'class':"wikitable"})
df=pd.read_html(str(wojewodztwatable)) #LISTA
df=pd.DataFrame(df[0]) #DATAFRAME


# # Czyszczenie danych

# In[21]:


# usuwamy niechciane kolumny (wiki)
data = df.drop(["Wyróżnik na tablicachrejestracyjnych", "Siedziba"], axis=1)
# zmieniamy nazwe kolumn
data = data.rename(columns={"PKB na 1 mieszkańca(31 XII 2018) [zł][3]": "PKB_na_mieszkanca","Poziomurbanizacji(31 XII 2018)": "Poziom_urbanizacji"})
# usuwamy niechciane kolumny z pliku
data2 = gdf.drop(["IIP_PRZEST","JPT_WAZNA_","JPT_NAZWA1","JPT_ORGAN1","WERSJA_DO","WERSJA_OD","JPT_KJ_I_3", "WAZNY_OD","ID_BUFOR_1","JPT_SPS_KO","JPT_OPIS","JPT_KJ_I_2","JPT_KOD__1","WAZNY_DO","JPT_JOR_ID","JPT_ORGAN_","ID_BUFORA1","JPT_KJ_IIP"], axis=1)
#sprawdzamy typ danych i zmieniamy typ danych: pozwoli nam to zamienic m.in 02 na 2 ()
data3=data2.astype({"JPT_KOD_JE": "int64"})


# # Inner join

# In[22]:


a=pd.merge(data,data3,left_on='TERYT',right_on='JPT_KOD_JE') 


# In[36]:


b= geopandas.GeoDataFrame(a) #zamieniamy dataframe na geodataframe
b.plot("Gęstość zaludnienia[osób/km²]", legend=True)


# In[28]:


a.dtypes


# In[ ]:




