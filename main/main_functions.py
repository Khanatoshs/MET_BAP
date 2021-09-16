import pandas as pd
from bokeh.plotting import figure
from bokeh.tile_providers import CARTODBPOSITRON, get_provider
from bokeh.models import HoverTool,IndexFilter,CDSView,Circle,Range1d,LinearAxis,LegendItem,Legend

from  extras import dataframe_minutes_to_degrees,dataframe_wgs84_to_mercator

def get_dataframe_csv(filename:str,delimiter:str=';'):
    data = pd.read_csv(filename,delimiter=delimiter)
    df = pd.DataFrame(data)
    return df

def setup_dataframe(df_source):
    df = dataframe_minutes_to_degrees(df_source,'LAT GRADOS','LAT MIN','lat')
    df = dataframe_minutes_to_degrees(df,'LONG GRADOS','LONG MIN','lon')
    df = dataframe_wgs84_to_mercator(df,'lat','lon')
    df['date'] = pd.to_datetime(df['FECHA'] + ' ' +df['HORA'],format='%d/%m/%Y %H:%M:%S')
    return df

def create_bokeh_map(data_source,df,**extras):
    default_tile_provider = get_provider(CARTODBPOSITRON)
    scale=extras.get('scale',10000)
    x = df['x']
    y = df['y']
    x_min=int(x.mean() - (scale * 350))
    x_max=int(x.mean() + (scale * 350))
    y_min=int(y.mean() - (scale * 350))
    y_max=int(y.mean() + (scale * 350))

    default_tools = 'wheel_zoom,pan,reset,save,box_select,tap'
    default_tooltips = [('Date:','@date{%Y-%m-%d %H:%M:%S}'),('Lat:','@lat'),('Lon:','@lon')]
    default_filter=IndexFilter(indices=[])
    defualt_view= CDSView(source=data_source,filters=[default_filter])
    default_selected_circle = Circle(fill_alpha=1,fill_color="firebrick", line_color=None)
    default_nonselected_circle = Circle(fill_alpha=0.01, fill_color="grey", line_color=None)

    f1 = figure(
        title=extras.get('title','Recorrido BAP'),
        tools=extras.get('tools',default_tools),
        x_range=(x_min,x_max),
        y_range=(y_min,y_max),
        x_axis_type='mercator',
        y_axis_type='mercator',
        width=extras.get('width',700),
        height=extras.get('height',700)
        )
    f1.add_tile(extras.get('tile_provider',default_tile_provider))

    f1.xaxis.visible = False
    f1.yaxis.visible = False

    rend1 = f1.circle(x='x',y='y',source=data_source,color='navy',size=5,hover_color='firebrick',view=extras.get('view',defualt_view))
    map_hover = HoverTool(tooltips=extras.get('tooltips',default_tooltips),formatters={'@date':'datetime'},renderers=[rend1])
    map_hover.renderers.append(rend1)
    f1.tools.append(map_hover)

    rend1.selection_glyph = extras.get('selected_circle',default_selected_circle)
    rend1.nonselection_glyph =  extras.get('nonselected_circle',default_nonselected_circle)

    return f1

def create_bokeh_plot(data_source,df,x_axis:str,y_axis:str,y_axis_offset:int,y_extra:str,y_extra_offset:int,**extras):
    y = df[y_axis]
    y_min = y.min() - y_axis_offset
    y_max = y.max() + y_axis_offset
    
    y2 = df[y_extra]
    y2_min = y2.min() - y_extra_offset
    y2_max = y2.max() + y_extra_offset

    default_tools = 'wheel_zoom,pan,reset,save,box_select,tap'
    default_tooltips = [('Date:','@date{%Y-%m-%d %H:%M:%S}'),('Lat:','@lat'),('Lon:','@lon')]
    default_filter=IndexFilter(indices=[])
    default_view= CDSView(source=data_source,filters=[default_filter])
    default_selected_circle = Circle(fill_alpha=1,fill_color="firebrick", line_color=None)
    default_nonselected_circle = Circle(fill_alpha=0.01, fill_color="grey", line_color=None)

    f2 = figure(
        title=extras.get('title','Tabla Comparativa'),
        tools=extras.get('tools',default_tools),
        x_axis_type='datetime',
        y_range=(y_min,y_max),
        tooltips=extras.get('tooltips',default_tooltips),
        width=800
    )
    f2.extra_y_ranges = {'extra_range':Range1d(y2_min,y2_max)}

    rend2 = f2.circle(
        x=x_axis,y=y_axis,
        source=data_source,
         color='navy',
          alpha=0.5,
          size=5,
          view=extras.get('view',default_view),
          name='data_y1'
          )
    rend_extra = f2.circle(
        x=x_axis,y=y_extra,
        source=data_source, 
        color='forestgreen',
         alpha=0.5,size=5,
         view=extras.get('view',default_view),
         y_range_name = 'extra_range',
         name='data_y2'
         )
    l1 = LegendItem(label=extras.get('y_label',y_axis),renderers=[rend2],name='ly1')
    l2 = LegendItem(label=extras.get('y_extra_label',y_extra),renderers=[rend_extra],name='ly2')
    
    f2.add_layout(Legend(items=[l1,l2]))
    f2.add_layout(LinearAxis(y_range_name='extra_range'),'right')

    f2.legend.location= 'top_right'
    f2.legend.click_policy = 'hide'
    
    graph_hover = HoverTool(tooltips=extras.get('tooltips',default_tooltips),formatters={'@date':'datetime'},renderers=[rend2,rend_extra])
    # graph_hover_extra = HoverTool(tooltips=extras.get('tooltips',default_tooltips),formatters={'@date':'datetime'},renderers=[rend_extra])

    graph_hover.renderers.append(rend2)
    graph_hover.renderers.append(rend_extra)
    # graph_hover_extra.renderers.append(rend_extra)

    f2.tools.append(graph_hover)
    # f2.tools.append(graph_hover_extra)

    rend2.selection_glyph = extras.get('selected_circle',default_selected_circle)
    rend2.nonselection_glyph = extras.get('nonselected_circle',default_nonselected_circle)
    rend_extra.selection_glyph = extras.get('selected_circle',default_selected_circle)
    rend_extra.nonselection_glyph = extras.get('nonselected_circle',default_nonselected_circle)

    return f2