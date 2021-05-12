import pandas as pd, numpy as np, os
import matplotlib.pyplot as plt
import holoviews as hv, panel as pn
from holoviews import dim, opts
import geopandas as gpd, geoviews as gv
from holoviews.element import tiles
import IPython
from holoviews.element import tiles

hv.extension('bokeh', 'matplotlib')

pn.extension()

pd.options.display.max_columns = None
pd.options.display.max_rows = None
pd.options.display.float_format = '{:.2f}'.format


################### Data ###################

df = pd.read_parquet( "sydney_airbnb.parquet")

subs_geo = gpd.read_file("neighbourhoods.geojson")



################### Widgets and Extra Variables ###################

property_types = list(df['property_type'].unique())
p_type = pn.widgets.Select(value='Apartment', options=property_types)

revs_mask = df['number_of_reviews'] > 0
def get_nps(x):
    if x >= 90:
        return "Excellent"
    elif x >= 70:
        return "Okay"
    else:
        return "No Bueno"

    
df['nps'] = 'None'
df.loc[revs_mask, 'nps'] = df.loc[revs_mask, 'review_scores_rating'].apply(get_nps)

nps_vals = list(df.nps.unique())
nps_vals.remove('None')


nps = pn.widgets.Select(value='Excellent', options=nps_vals)

################### Map ###################

pn.depends(p_type.param.value)
def get_map(p_type, **kwargs):
    
    data = df[df['property_type'] == p_type].copy()
    data_group = data.groupby('neighbourhood_cleansed')['min_price_per_stay'].median().reset_index()
    data_merged = (data_group.merge(subs_geo[['neighbourhood', 'geometry']], left_on='neighbourhood_cleansed', right_on='neighbourhood')
                             .drop('neighbourhood', axis=1)
                             .rename(columns={'neighbourhood_cleansed': "Suburb"}))
    
    geo_data = gpd.GeoDataFrame(data_merged)
    
    fig = gv.Polygons(geo_data, vdims=['Suburb', 'min_price_per_stay']).opts(tools=['hover'], width=500, height=400, 
                                                                        color='min_price_per_stay', cmap='viridis_r',colorbar=True, 
                                                                        toolbar='above', xaxis=None, yaxis=None, color_levels=20)
    
    
    return (tiles.CartoLight() * fig).relabel(label=f'Median Listing Price per {p_type}')



################### Table ###################


reviews = ['review_scores_checkin', 'review_scores_cleanliness', 'review_scores_accuracy', 
           'review_scores_location', 'review_scores_communication', 'review_scores_value']
new_names = ['Checkin', 'Cleanliness', 'Accuracy', 'Location', 'Communication', 'Value']

names_dict = {old:new for old, new in zip(reviews, new_names)}


@pn.depends(p_type.param.value)
def get_rev_table(p_type, **kwargs):
    
    p_mask = df['property_type'] == p_type
    revs_mask = df['number_of_reviews'] > 0
    
    data = df[p_mask & revs_mask].copy()
    
    data.rename(names_dict, axis=1, inplace=True)
    
    data_group = data[new_names].mean().to_frame(name='vals').reset_index()
    data_group.columns = ['Reviews', 'Average Score']
    
    table = hv.Table(data_group).opts(width=250, height=180, bgcolor='red')
    
    return table


################### Box and Whisker ###################



@pn.depends(nps.param.value)
def cat_whisker(nps, **kwargs):
    
    nps_mask = df['nps'] == nps
    budget = df['two_weeks_price'] < 2000
    
    data = df.loc[nps_mask & budget, ['property_type', 'two_weeks_price']].copy()
    
    label = f"(2-Week Stay) Price Range per Property Type with {nps} Reviews"
    
    boxw = hv.BoxWhisker(data, 'property_type', 'two_weeks_price', label=label)
    
    return boxw.opts(box_fill_color='#D5E051', box_line_color='#5F6062', width=600, height=250, box_line_width=1,
                     whisker_color='#FFFFFF', xrotation=25, bgcolor='#5F6062', labelled=[], outlier_color='#FFFFFF')


################### Dots ###################


@pn.depends(p_type.param.value, nps.param.value)
def my_dots(p_type, nps, **kwargs):
    
    nps_mask = df['nps'] == nps
    p_mask = df['property_type'] == p_type
    revs_mask = df['number_of_reviews'] > 0
    
    data = df[nps_mask & p_mask & revs_mask].copy()
    group = data.groupby(['neighbourhood_cleansed', 'host_is_superhost'])['number_of_reviews'].mean().reset_index()
    
    superh = group[group['host_is_superhost'] == 't']
    regularh = group[group['host_is_superhost'] == 'f']
    
    dots1 = hv.Scatter(superh, 'neighbourhood_cleansed', 'number_of_reviews', label='Super Hosts').sort('number_of_reviews').opts(color='#D5E051', width=500, show_grid=True,
                                                                                height=400, invert_axes=True, size=7, tools=['hover'],
                                                                                legend_position='bottom_right', toolbar='right',
                                                                                labelled=[], title="Average # of Reviews per Suburb")
    dots2 = hv.Scatter(regularh, 'neighbourhood_cleansed', 'number_of_reviews', label='Regular Hosts').opts(size=7, color='#FFFFFF')
    
    return (dots1 * dots2)



################### BANs ###################


@pn.depends(p_type.param.value)
def bans(p_type):
    
    g_opts = dict(default_color='#FFFFFF', align='start', # the global options that fit our 3 BANS
                  font_size='13pt', title_size='13pt')
    
    p_mask = df['property_type'] == p_type
    
    data = df[p_mask].copy()
    
    # the BANs will need a sum a count and a mean 
    listings = p_mask.sum() 
    super_host = data.groupby('host_is_superhost')['host_is_superhost'].count().loc['t']
    avg_price = data['price'].mean()
    
    # the title will change depending on the property type
    main_title = pn.pane.Markdown(f"# {p_type}", style={'color':'#FFFFFF'})
    
    ban1 = pn.indicators.Number(name="Listings", value=listings, **g_opts, format='{value:,.0f}')
    ban2 = pn.indicators.Number(name="Super Hosts", value=super_host, **g_opts, format='{value:,.0f}')
    ban3 = pn.indicators.Number(name="Avg Price/Night", value=avg_price, **g_opts, format='${value:,.0f}')
    
    return pn.Column(main_title, pn.Row(ban1, ban2, ban3, align='start'), align='start', height=80, width=150)



################### Title ###################


title = pn.Row(
    pn.pane.Markdown(f"# Airbnb Listings Analysis in Sydney", 
                     style={"color": "#FFFFFF"}, width=500, height=50,
                     sizing_mode="stretch_width", margin=(0,0,0,5)), 
    pn.Spacer(),
    pn.pane.PNG("https://i.pinimg.com/originals/a3/cd/30/a3cd30c0ba0e7f827dfe22e7a7011cd8.gif", height=50, sizing_mode="fixed", align="center"),
    pn.pane.PNG("https://e7.pngegg.com/pngimages/388/581/png-clipart-sydney-opera-house-city-of-sydney-cartoon-illustration-sydney-opera-house-creative-cartoon-cartoon-character-angle.png", height=50, sizing_mode="fixed", align="center"),
    background="#5F6062", sizing_mode='fixed', height=250, width=1050
)

################### All together ###################


c1  = pn.Column(bans, pn.Spacer(height=20), get_rev_table, width=250, height=290)

c2 = pn.Column(pn.Row(p_type, nps, align='center'), cat_whisker, height=290, align='center')

r1 = pn.Row(c1, pn.Spacer(width=100), c2, sizing_mode='fixed', align='center', width=1000, height=350)

r2 = pn.Row(my_dots, get_map, align='center', sizing_mode='fixed', width=1100, height=420)

dashboard = pn.Column(title, r1, r2, background='#5F6062', sizing_mode='fixed', 
          align='center', height=800, width=1050)

from bokeh.themes.theme import Theme

theme = Theme(
    json={
    'attrs' : {
        'Figure' : {
            'background_fill_color': '#5F6062',
            'border_fill_color': '#5F6062',
            'outline_line_color': '#5F6062',
        },
        'Grid': {
            'grid_line_dash': [6, 4],
            'grid_line_alpha': .3,
        },

        'Axis': {
            'major_label_text_color': '#D5E051',
            'axis_label_text_color': '#D5E051',
            'major_tick_line_color': '#D5E051',
            'minor_tick_line_color': '#D5E051',
            'axis_line_color': "#D5E051"
        },
        'Title': {
            'text_color': '#FFFFFF'
        }
    }
})

hv.renderer('bokeh').theme = theme

# dashboard.show(threaded=True)

dashboard.servable("My_Dashboard")