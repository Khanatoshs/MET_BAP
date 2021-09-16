from datetime import date
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import pandas as pd

from bokeh.plotting import show,output_file
from bokeh.tile_providers import CARTODBPOSITRON, get_provider
from bokeh.models import ColumnDataSource,Circle,DateRangeSlider,IndexFilter,CDSView,Button,Dropdown
from bokeh.layouts import row,gridplot,layout,column

from extras import dataframe_minutes_to_degrees,dataframe_wgs84_to_mercator
from js_functions import Button_callback,Dropdown_y1_callback,Dropdown_y2_callback
from main_functions import get_dataframe_csv,setup_dataframe,create_bokeh_map,create_bokeh_plot

output_file('Graficos_BAP.html',title='Graficos de recorrido BAP')

df = get_dataframe_csv('./data/Data_BAP.csv')
df = setup_dataframe(df)


tile_provider = get_provider(CARTODBPOSITRON)
tools = 'wheel_zoom,pan,reset,save,box_select,tap'
source = ColumnDataSource(df)

filter=IndexFilter(indices=[i for i in range(len(list(df['date'])))])
view= CDSView(source=source,filters=[filter])

tooltips = [('Date:','@date{%Y-%m-%d %H:%M:%S}'),('Lat:','@lat'),('Lon:','@lon')]

selected_circle = Circle(fill_alpha=1,fill_color="firebrick", line_color=None)
nonselected_circle = Circle(fill_alpha=0.01, fill_color="grey", line_color=None)

dropdown_menu = [
    ('Presion','PRESSION'),
    ('Humedad Relativa','HR'),
    ('Temperatura','TEMP'),
    ('Velocidad de Viento (Estribor)','VEL-ESTRIBOR'),
    ('Velocidad de Viento (Babor)','VEL-BABOR')]


legend_dict = {
    'PRESSION':'Presion',
    'HR':'Humedad Relativa',
    'TEMP':'Temperatura',
    'VEL-ESTRIBOR':'Velocidad de Viento (Estribor)',
    'VEL-BABOR':'Velocidad de Viento (Babor)'
}

extras = {
    'title':'Mapa Recorrido BAP',
    'tooltips':tooltips,
    'tile_provider':tile_provider,
    'tools':tools,
    'view':view,
    'selected_circle':selected_circle,
    'nonselected_circle':nonselected_circle
}

f1 = create_bokeh_map(
    source,
    df,
    **extras
    )

extras['title'] = 'Tabla Comparativa'
extras['y_label'] = 'Presion'
extras['y_extra_label'] = 'Velocidad de Viento (Estribor)'
f2 = create_bokeh_plot(
    data_source=source,
    df= df,
    x_axis='date',
    y_axis='PRESSION',
    y_axis_offset= 2,
    y_extra='VEL-ESTRIBOR',
    y_extra_offset=10,
    **extras
    )


date_slider= DateRangeSlider(value=(date(2019,12,11),date(2019,12,30)),start=date(2019,12,11),end=date(2019,12,30))

# dropdown_menu = [
#     ('Fecha','date')
#     ('Presion','PRESSION'),
#     ('Humedad Relativa','HR'),
#     ('Temperatura','TEMP'),
#     ('Velocidad de Viento (Estribor)','VEL-ESTRIBOR'),
#     ('Velocidad de Viento (Babor)','VEL-BABOR')]





dropdown_y1 = Dropdown(label='Escoger Eje Y Izq', button_type='warning',menu =dropdown_menu)
dropdown_y2 = Dropdown(label='Escoger Eje Y Der', button_type='warning',menu =dropdown_menu)

y1 = f2.select_one({'name':'data_y1'})
ly1 = f2.select_one({'name':'ly1'})

y2 = f2.select_one({'name':'data_y2'})
ly2 = f2.select_one({'name':'ly2'})
# y_extra_range = f2.select_one({'name':'extra_range'})

dropdown_y1.js_on_event('menu_item_click',Dropdown_y1_callback(source,y1,f2,ly1,legend_dict))
dropdown_y2.js_on_event('menu_item_click',Dropdown_y2_callback(source,y2,f2,ly2,legend_dict))

apply_button = Button(label='Aplicar',button_type='primary')
apply_button.js_on_click(Button_callback(source,filter,date_slider))




p = layout([row(column(f1),column(f2,row(dropdown_y1,dropdown_y2),row(date_slider,apply_button)))])



show(p)
