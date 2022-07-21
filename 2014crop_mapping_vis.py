'''
Based on a 2014 dataset found on kaggle.
'''

import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors


gdf = gpd.read_file('crop_mapping_2014.gpkg')


#pull idle land out

gdf_idle = gdf[gdf['Crop2014'] == 'Idle']
idle_areas = gdf_idle[['County','Area_ha']].groupby('County').sum()
crop_areas = gdf[['County', 'Area_ha']].groupby('County').sum()

frac_idle = idle_areas.divide(crop_areas, fill_value=0)
frac_idle_by_county = frac_idle.groupby('County').mean().sort_values('Area_ha', ascending=False).plot.bar(figsize = (20,5))
plt.title('Fraction of Idle Area by County')
plt.tight_layout()
plt.savefig('frac_idle_area_by_county.png')


#define new broader land use categories
def categorize(val):
    if val['Crop2014'] == 'Idle':
        return 'Idle'
    return 'Crop'

gdf['Combi'] = gdf.apply(lambda row: categorize(row), axis=1)

#create color maps

#mid idle
imperial = gdf[gdf.County == 'Imperial']
fig1, ax1 = plt.subplots(figsize=(20,30))
ax1.set_title('Imperial County')
imperial.plot(column='Combi', categorical='True', legend=True, legend_kwds={'loc':'best', 'fontsize':'large'},cmap="Paired", ax = ax1)
ax1.axis('off')

# low idle
sanjoaquin = gdf[gdf.County == 'San Joaquin']
fig2, ax2 = plt.subplots(figsize=(20,30))
ax2.set_title('San Joaquin County')
sanjoaquin.plot(column='Combi', categorical='True', legend=True, legend_kwds={'loc':'best', 'fontsize':'large'},cmap="Paired", ax = ax2)
ax2.axis('off')

# higher idle
fresno = gdf[gdf.County == 'Fresno']
fig3, ax3 = plt.subplots(figsize=(20,30))
ax3.set_title('Fresno County')
fresno.plot(column='Combi', categorical='True', legend=True, legend_kwds={'loc':'best', 'fontsize':'large'},cmap="Paired", ax = ax3)
ax3.axis('off')

plt.show()
