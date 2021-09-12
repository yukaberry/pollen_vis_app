import geopandas as gpd 
import matplotlib.pyplot as plt
plt.style.use('seaborn')
import pandas as pd
import numpy as np


plz_shape_df = gpd.read_file('geo_data/plz-gebiete.shp', dtype={'plz': str})

data_of_df = {"city" : ['Berlin','Dresden','Rostock','Delmenhorst','Hannover',"Mönchengladbach","Fulda","Freiburg",
"Borstel","Goettingen","Aachen"],
"station_type":["all_year","all_year","all_year","all_year","all_year","all_year","all_year","all_year",
"seaonal","seaonal","seaonal",
],
"lat":[52.520008,51.041131415920624,54.094001340865404,53.052618829565816,52.37052,51.192230,50.557076417360484,47.99681292704471,
52.669842,51.53637615034263,50.775345],
"lon":[13.404954,13.731137273908088,12.136413737416127,8.630375080273396,9.73322,6.439590,9.6835170818526,7.840304025119172,
8.970460,9.925517969237282,6.083887,
],
}


city_df = pd.DataFrame(data_of_df)
#print(city_df.head())
city_df_all = city_df.loc[(city_df["station_type"]=="all_year")]
city_df_seasonal = city_df.loc[(city_df["station_type"]=="seasonal")]

print(city_df_all.head())


fig, ax = plt.subplots()
plz_shape_df.plot(color='lightgray', alpha=0.8,ax=ax)

ax.plot(
        city_df_all["lat"],
        city_df_all["lon"], 
        marker='o',
        c='green', 
        alpha=0.5
    )

# city_df_all.plot(
#     kind='scatter', 
#     x='lon', 
#     y='lat', 
#     c='r', 
#     marker='*',
#     s=50,
#     #label=city_df["station_type"].values,  
#     ax=ax
# )
# city_df_seasonal.plot(
#     kind='scatter', 
#     x='lon', 
#     y='lat', 
#     c='g', 
#     marker='o',
#     s=50,
#     #label=city_df["station_type"].values,  
#     ax=ax
# )


# axis off 
plt.axis("off")
plt.show()
