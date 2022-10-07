#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 10:10:48 2022

@author: mbexkes3
"""

import datetime
from os.path import dirname, join

import pandas as pd
from scipy.signal import savgol_filter

from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, DataRange1d, Select
from bokeh.palettes import Blues4
from bokeh.plotting import figure
import os
import glob

def update_fun(attrname, old, new):
    
    pass

locations = ['Manchester','Roslin','Cheadle']

location_select = Select(value=locations[0], title='Locations',options=locations)

# year select
files = glob.glob(path=location_select.value+'/*.csv')
years = [x[-8:-4] for x in files]
year_select = Select(value=years[0], title='Year', options=years)


location_select.on_change('value', update_fun)

controls = column(location_select)

curdoc().add_root(row(controls))
curdoc().title = 'Rain Graphs'


#location_select.value 
#location_select.options




# get data

filename = glob.glob(path+'/'+location_select.value+'/*'+year_select.value+'*.csv')

data = pd.read_csv(filename, skiprows=61)











