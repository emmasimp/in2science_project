'''function to plot weather station locations on a map'''

import geopandas as gpd
import pandas as pd
from bokeh.plotting import figure


def make_map(stations):
	''' stations is a dataframe containing 'Name' ,'lat' ,'lon' columns
	'''

    lon = stations['Longitude'].apply(lambda x: float(x))
    lat = stations['Latitude'].apply(lambda x: float(x))

    d = {'lat': lat, 'lon': lon, 'name':stations['Name']}
    df_map = pd.DataFrame(data=d)

    TOOLS="hover,pan,wheel_zoom,zoom_in,zoom_out,box_zoom,undo,redo,reset,tap,save,poly_select"

    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    geosource = GeoJSONDataSource(geojson = world.to_json())

    SRC_map = ColumnDataSource(df_map)

    TOOLTIPS = [
        ("lat", "@lat"),
        ("lon", "@lon"),
        ("Name", "@name")]

    cplot = figure(title = 'Weather Stations',tools = TOOLS, tooltips=TOOLTIPS)
    cplot.circle("lon", "lat", size=8,source=SRC_map)
    states = cplot.patches('xs','ys', source = geosource,
                       fill_color = 'gray',
                       line_color = 'gray', 
                       line_width = 0.25, 
                       fill_alpha = 0.5)
    return(cplot)