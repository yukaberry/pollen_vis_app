
import geopandas as gpd # dependencies shaply, fiona
import matplotlib.pyplot as plt
plt.style.use('seaborn')
import pandas as pd
import numpy as np
#import mplleaflet


# note! place all of files (dbf,prj,shp, shx in the same folder)
# the polygons define the postal code’s shape.
plz_shape_df = gpd.read_file('geo_data/plz-gebiete.shp', dtype={'plz': str})
plz_region_df = pd.read_csv('geo_data/zuordnung_plz_ort.csv', sep=',', dtype={'plz': str})
#germany_shape = pd.read_csv('geo_data/zuordnung_plz_ort.csv', sep=',', dtype={'plz': str})
plz_region_df.drop('osm_id', axis=1, inplace=True)





plt.rcParams['figure.figsize'] = [11, 11]
# Get lat and lng of Germany's main cities. 
all_year = {
    'Berlin': (13.404954, 52.520008), 
    'Dresden': (13.731137273908088,51.041131415920624),
    'Rostock': (12.136413737416127, 54.094001340865404),
    'Delmenhorst': (8.630375080273396,53.052618829565816),
    'Hannover': (9.73322, 52.37052),
    "Mönchengladbach":(6.439590,51.192230),
    "Fulda":(9.6835170818526,50.557076417360484),
    "Freiburg":(7.840304025119172,47.99681292704471),}
season ={
    "Borstel":(8.970460,52.669842),
    "Goettingen":(9.925517969237282,51.53637615034263),
    "Aachen":(6.083887,50.775345),}
not_in_use ={
    "Heidelberg":(8.674091023895429,49.43408292001512),}
non_PID ={
    "Cottbus":(14.3248674827388,51.75041803756246),}

# Merge data
# plz_shape_df : shape of germany
# plz_region_df : each region shape
germany_df = pd.merge(left=plz_shape_df, right=plz_region_df,on='plz',how='inner')
germany_df.drop(['note'], axis=1, inplace=True)



fig, ax = plt.subplots()
plz_shape_df.plot(color='lightgray', alpha=0.8,ax=ax)

#plz_region_df.plot(ax=ax, color='white',edgecolor='black',column="bundesland", alpha=0.8)

# union=gpd.overlay(plz_shape_df,plz_region_df, how='union')
# union.plot(edgecolor ='black')
#plt.show()

# params
# bbox_to_anchor : position the legend. A 2-tuple (x, y) places the corner of the legend specified by loc at x, y.
# cmap : colour type
# #germany_df.plot(ax=ax,column='bundesland',edgecolor='black', color='white') #,categorical=True,
# legend=True, legend_kwds={'title':'Bundesland', 'bbox_to_anchor': (1.35, 0.8)},
# alpha=0.9,
# cmap='Wistia')

# Plot cities. 
for c in all_year.keys():
    #Plot city name.
    ax.text(
        x=all_year[c][0], 
        # Add small shift to avoid overlap with point.
        y=all_year[c][1] + 0.08, 
        s=c, 
        fontsize=12,
        ha='left')

    # Plot city location centroid.
    ax.plot(
        all_year[c][0], 
        all_year[c][1], 
        marker='o',
        c='green', 
        alpha=0.5
    )

for c in season.keys():
    #Plot city name.
    ax.text(
        x=season[c][0], 
        # Add small shift to avoid overlap with point.
        y=season[c][1] + 0.08, 
        s=c, 
        fontsize=12,
        ha='left')

    # Plot city location centroid.
    ax.plot(
        season[c][0], 
        season[c][1], 
        marker='o',
        c='blue', 
        alpha=0.5
    )



for c in not_in_use.keys():
    #Plot city name.
    ax.text(
        x=not_in_use[c][0], 
        # Add small shift to avoid overlap with point.
        y=not_in_use[c][1] + 0.08, 
        s=c, 
        fontsize=12,
        ha='left')

    # Plot city location centroid.
    ax.plot(
        not_in_use[c][0], 
        not_in_use[c][1], 
        marker="o",
        c='black', 
        alpha=0.5
    )


for c in non_PID.keys():
    #Plot city name.
    ax.text(
        x=non_PID[c][0], 
        # Add small shift to avoid overlap with point.
        y=non_PID[c][1] + 0.08, 
        s=c, 
        fontsize=12,
        ha='left')

    # Plot city location centroid.
    ax.plot(
        non_PID[c][0], 
        non_PID[c][1], 
        marker="o",
        c='darkgreen', 
        alpha=0.5
    )

    ax.set(
    title='Germany', 
    aspect=1.3, 
    facecolor= 'white') #'lightblue')

# axis off 
plt.axis("off")
plt.show()