import folium as folium
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from folium.plugins import FloatImage

df = pd.read_csv('kc_house_data.csv')
# Convert date to timestamp
df['date'] = pd.to_datetime(df['date'])
df.head()

###Exploratory analysis
# Check for the shape of the dataset
df.shape
#check for the data types
df.dtypes

#correlation between variables
df.corr()['price'].sort_values(ascending=False)
plt.figure(figsize=(12,12))
sns.heatmap(df.corr(),vmax=1.0,vmin=-1.0, square=True, fmt='.2f',
            annot=True, cbar_kws={"shrink": .75}, cmap='YlGnBu')
plt.show()

##Visualisations
#House prices and Grade boxplot visualisation
plt.figure(figsize=(8,6))
sns.boxplot(x = df['grade'], y=df['price'], palette="PiYG")
plt.suptitle('House Prices and Grade Rating', size=18)
plt.xlabel('Grade', fontsize = 15)
plt.ylabel('House Prices', fontsize = 15)
plt.show()


#Folium Map visulaisation- Average House Prices and Zip Code
#add heatmao scall to map

mymap = folium.Map(location= [47.56 , -122.22], zoom_start =9)

# Get the highest average house price
maxave = int(df.groupby(['zipcode']).mean()['price'].max())
print("Highest City House Price is: ", maxave)

# Create a color map to match house prices.
colormap = ['#00fff7', '#009b48' ,'#fbff00' ,'#ffc800' ,'#f200ff' ,'#ff0000' ]

# Add marker info
for index, row in df.groupby('zipcode').agg({'lat': 'mean','long': 'mean', 'price':'mean', 'zipcode':'count' }).iterrows():
    # Set icon color based on price
    theCol = colormap[ int((len(colormap) - 1 ) *  float( row['price']) / maxave) ]
    markerText =  ( 'Average price : ' + str(round(row['price'], 2) ) +' $' + '\n' + 'Houses sold : ' + str(row['zipcode']) )
    folium.CircleMarker( radius=(row['zipcode'])/15, location=[row['lat'],row['long']], popup=folium.Popup(markerText,max_width=150,min_width=150), color= theCol,fill=True,fill_color=theCol,  ).add_to(mymap)

FloatImage('https://lh3.googleusercontent.com/proxy/SRXTqZngcyOscx1nR1iB9c4IobPtOn0cEROsZ_wK6CO3nfAjD4e4TDXPDjN3AU2ZLJxzJQaoLJnlqk9zZevN7S2wZZctQysIIKOvigpGatc', bottom=0, left=65).add_to(mymap)
mymap.save('Mymap.html')