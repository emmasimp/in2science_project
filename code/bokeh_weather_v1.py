#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 09:38:48 2022

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

def update_plot(attrname, old, new):
  #  city = city_select.value
    year_select.options = sorted([x[-8:-4] for x in glob.glob(path+city_select.value+'/*.csv')])
  

#locations = ['test1','test2']

path = './Data/CEDA/MIDAS-open/uk-daily-rain-obs/'

# location select
locations = [x[0][41:] for x in os.walk(path)]
city_select = Select(value=locations[1], title='City', options=sorted(locations))

# year select
files = glob.glob(path+city_select.value+'/*.csv')
years = [x[-8:-4] for x in files]
year_select = Select(value=years[0], title='Year', options=sorted(years))

# add functionality to selects
city_select.on_change('value', update_plot)
year_select.on_change('value', update_plot)

# add selects to layout
controls = column(city_select,year_select)
curdoc().add_root(row(controls))
curdoc().title = "Weather"

