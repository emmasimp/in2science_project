import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import glob
import os

# where is the data?
path = './Data/CEDA/MIDAS-open/uk-daily-rain-obs/'

# what files/locations are available?
locations = [x[0][41:] for x in os.walk(path)]

# read in data
files = glob.glob(path+locations[1]+'/*.csv')

years = [x[-8:-4] for x in files]

