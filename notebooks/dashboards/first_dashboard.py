import pandas as pd, numpy as np, os
import matplotlib.pyplot as plt
import holoviews as hv, panel as pn
from holoviews import dim, opts
import geopandas as gpd, geoviews as gv
from holoviews.element import tiles

hv.extension('bokeh', 'matplotlib')

pn.extension()


### Load the data

path = os.path.join('..', 'data')

df = pd.read_parquet(os.path.join(path, 'static', "melb_auctions_clean.parquet"))

subs_stats = gpd.read_file(os.path.join(path, 'static', "suburbs_price.geojson"))

### Create Map

subs_stats['Mean_Median_Ratio'] = subs_stats['mean'] / df.Price.median()

melb_map = gv.Polygons(subs_stats[(subs_stats.Suburb != 'Bellfield') & 
                                  (subs_stats.Suburb != 'Hillside')], 
                       vdims=['Suburb', 'Mean_Median_Ratio'], 
                       label='House Prices in Melbourne').opts(
                                tools=['hover'], width=500, height=400, color='Mean_Median_Ratio', #toolbar=None,
                                colorbar=True, toolbar='disable', xaxis=None, yaxis=None)


### BANs

def ban(title, value, c=1):
    cols = ('#bf616a', '#d08770', '#ebcb8b', '#a3be8c', '#b48ead')
    return pn.indicators.Number(name=title, value=value, default_color=cols[c], align='center',
                                format='${value:,.0f}K', font_size='20pt', title_size='20pt')

high_price = df['Price'].max() / 1000
perc_25th = df['Price'].quantile(0.25) / 1000
median_price = df['Price'].median() / 1000
cheap_price = df['Price'].min() / 1000
perc_75th = df['Price'].quantile(0.75) / 1000

ban1 = ban("Min Price", cheap_price, 0)
ban2 = ban("25th Percentile", perc_25th, 1)
ban3 = ban("Median Price", median_price, 2)
ban4 = ban("25th Percentile", perc_75th, 3)
ban5 = ban("Max Price", high_price, 4)


### Bars

### global options

global_opts = dict(bar_width=0.2, color='#d08770', line_color=None, alpha=0.5, toolbar='disable', width=230, height=200,
                   xaxis='bottom', yformatter='$%.0fK', labelled=[])



data_bar1 = (df.groupby('Type')['Price'].median() / 1000).reset_index()
data_bar2 = (df.groupby('CarSpots')['Price'].median() / 1000).reset_index()
data_bar3 = (df.groupby('Bathroom')['Price'].median() / 1000).reset_index()
data_bar4 = (df.groupby('Rooms')['Price'].median() / 1000).reset_index()

b1 = hv.Bars(data_bar1, 'Type', 'Price').opts(title="Median Price/Type", **global_opts,
                                              yticks=list(range(100, round(data_bar1.Price.max()), 300)))

b2 = hv.Bars(data_bar2, 'CarSpots', 'Price').opts(title='Avg Price/Car Spots', **global_opts,
                                                  yticks=list(range(100, round(data_bar2.Price.max()), 300)))

b3 = hv.Bars(data_bar3, 'Bathroom', 'Price').opts(title='Avg Price/Bathrooms', **global_opts, yticks=list(range(100, round(data_bar3.Price.max()), 600)))

b4 = hv.Bars(data_bar4, 'Rooms', 'Price').opts(title='Avg Price/Rooms', **global_opts, yticks=list(range(100, round(data_bar4.Price.max()), 400)))


### Loli Suburbs Chart

subs_counts = df.Suburb.value_counts()
subs_counts = list(subs_counts[subs_counts > 149].index)

fav_lolli = (hv.Scatter((df[df.Suburb.isin(subs_counts)].groupby('Suburb')['Price'].agg(['mean', 'median']) / 1000).reset_index(), 'mean', 'Suburb', label="Average Price per Suburb")
 .sort()
 .opts(color='blue', size=5, width=500, height=400, toolbar='disable', xformatter='$%.0fK', show_grid=True, xrotation=45, bgcolor=None, labelled=[])
)


### Dashboard

title = pn.Row(
    pn.pane.Markdown("## Housing Analysis in Melbourne, AU", style={"color": "#3b4252"}, width=500, 
                     sizing_mode="stretch_width", margin=(10,5,10,15)), 
    pn.Spacer(),
    pn.pane.PNG("https://icons.iconarchive.com/icons/google/noto-emoji-travel-places/1024/42486-house-icon.png", height=50, sizing_mode="fixed", align="center"),
    pn.pane.PNG("https://image.flaticon.com/icons/png/512/505/505026.png", height=50, sizing_mode="fixed", align="center"),
    background="#d8dee9", sizing_mode='stretch_width'
)

r1 = pn.Row(b1, b2, b3, b4, sizing_mode='stretch_width', align='center')

r2 = pn.Row(ban1, ban2, ban3, ban4, ban5, align='center')

r3 = pn.Row(fav_lolli, (tiles.OSM() * melb_map), sizing_mode='stretch_width', align='center')

dash = pn.Column(title, r1, r2, r3, background='#eceff4', sizing_mode='stretch_width', 
          align='center')

dash.save('static_dash.html')

dash.show()