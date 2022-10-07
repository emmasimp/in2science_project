#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 16:00:59 2022

@author: mbexkes3
"""

''' A weather chart for three cities using a csv file.
This illustration demonstrates different interpretation of the same data
with the distribution option.

.. note::
    This example needs the Scipy and Pandas package to run. See
    ``README.md`` for more information.

'''
import datetime
from os.path import dirname, join

import pandas as pd
from scipy.signal import savgol_filter

from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, DataRange1d, Select, GeoJSONDataSource
from bokeh.palettes import Blues4
from bokeh.plotting import figure
import os
import glob
import geopandas as gpd
from bokeh.models import LinearAxis, Range1d




# get station information
stations = pd.read_csv('../data/MIDAS-open/excel_list_station_details.csv',skiprows=1)



def get_dataset(df):
    return ColumnDataSource(data=df)

def make_plot(source,source2, title):
    TOOLTIPS = [
        ("value", "@prcp_amt"),
        ]
       # ("Category 2", "@cat2")
    plot = figure(x_axis_type="datetime", tools='hover', tooltips=TOOLTIPS)#x_axis_type="datetime", width=800, tools="", toolbar_location=None)
    plot.title.text = title

    plot.line(x='ob_date',y='prcp_amt',line_color='red',legend='Year A',source=source)
    plot.line(x='ob_date',y='prcp_amt',source=source2)
    #plot.line(x=[1,2,3],y=[1,10,20])
    plot.extra_x_ranges['sec_x_axis'] = Range1d(0, 100)
    ax2 = LinearAxis(x_range_name="sec_x_axis", axis_label="secondary x-axis")
    plot.add_layout(ax2, 'below')

    

    
    # fixed attributes
    plot.xaxis.axis_label = None
    plot.yaxis.axis_label = "Precip"
    plot.axis.axis_label_text_font_style = "bold"
    plot.x_range = DataRange1d(range_padding=0.0)
    plot.grid.grid_line_alpha = 0.3
    plot.legend.title = 'Years'

    return plot

def update_plot(attrname, old, new):
    year_select.options = sorted([x[-8:-4] for x in glob.glob(path+city_select.value+'/*.csv')])
  
    city = city_select.value
    plot.title.text = "Weather data for " + city
    
    filename = glob.glob(path+'/'+city_select.value+'/*'+year_select.value+'*.csv')
    filename2 = glob.glob(path+'/'+city_select.value+'/*'+year_select_2.value+'*.csv')

    if len(filename):
        df = pd.read_csv(filename[0], skiprows=61)
        df['ob_date'] = pd.to_datetime(df['ob_date'][:-1], format='%Y-%m-%d %H:%M:%S')
        src = get_dataset(df)
        source.data.update(src.data)
    else:
        pass

    if len(filename2):
        df = pd.read_csv(filename2[0], skiprows=61)
        df['ob_date'] = pd.to_datetime(df['ob_date'][:-1], format='%Y-%m-%d %H:%M:%S')
        src = get_dataset(df)
        source2.data.update(src.data)
    else:
        pass

def make_map(stations):
    lon = stations['Longitude'].apply(lambda x: float(x))
    lat = stations['Latitude'].apply(lambda x: float(x))

    d = {'lat': lat, 'lon': lon, 'name':stations['Name']}
    df_map = pd.DataFrame(data=d)

    TOOLS="hover,pan,wheel_zoom,zoom_in,zoom_out,box_zoom,undo,redo,reset,tap,save,poly_select"

  #  p = figure(tools=TOOLS, plot_width=800)

   # p.scatter(lon, lat,
    #          fill_alpha=0.6,
     #         line_color=None)

    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    geosource = GeoJSONDataSource(geojson = world.to_json())

    SRC_map = ColumnDataSource(df_map)

    TOOLTIPS = [
        ("lat", "@lat"),
        ("lon", "@lon"),
        ("Name", "@name")]
       # ("Category 2", "@cat2")]

    cplot = figure(title = 'Weather Stations',tools = TOOLS, tooltips=TOOLTIPS, plot_width=400, plot_height=400)
    cplot.circle("lon", "lat", size=8,source=SRC_map)
    states = cplot.patches('xs','ys', source = geosource,
                       fill_color = 'gray',
                       line_color = 'gray', 
                       line_width = 0.25, 
                       fill_alpha = 0.5)
    return(cplot)



path = '../data/MIDAS-open/uk-daily-rain-obs/'
locations = [x[0][36:] for x in os.walk(path)]
city_select = Select(value=locations[1], title='City', options=sorted(locations))


files = glob.glob(path+city_select.value+'/*.csv')

years = [x[-8:-4] for x in files]
year_select = Select(value=years[0], title='Year', options=sorted(years))

year_select_2 = Select(value=years[0], title='Year', options=sorted(years))

city_select.on_change('value', update_plot)
year_select.on_change('value', update_plot)
year_select_2.on_change('value',update_plot)

filename = glob.glob(path+'/'+city_select.value+'/*'+year_select.value+'*.csv')
df = pd.read_csv(filename[0],skiprows=61)
df['ob_date'] = pd.to_datetime(df['ob_date'][:-1], format='%Y-%m-%d %H:%M:%S')
source = get_dataset(df)

filename2 = glob.glob(path+'/'+city_select.value+'/*'+year_select_2.value+'*.csv')
df2 = pd.read_csv(filename2[0],skiprows=61)
df['ob_date'] = pd.to_datetime(df['ob_date'][:-1], format='%Y-%m-%d %H:%M:%S')
source2 = get_dataset(df2)

title = city_select.value
plot = make_plot(source,source2, "Weather data for " + title)

city_select.on_change('value', update_plot)
year_select.on_change('value', update_plot)
year_select_2.on_change('value',update_plot)

controls = column(city_select, year_select, year_select_2)

map_plot = make_map(stations)

curdoc().add_root(row(map_plot,plot,controls))
curdoc().title = "Weather"