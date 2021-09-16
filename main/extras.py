import numpy as np

def minutes_to_degrees(deg:int,minutes:float,seconds:float=0.0):
    deg_fin = deg + (minutes/60) + (seconds/3600)
    return deg_fin

def wgs84_to_web_mercator(lat:float, lon:float):
    """Converts decimal longitude/latitude to Web Mercator format"""
    k = 6378137
    x = lon * (k * np.pi/180.0)
    y = np.log(np.tan((90 + lat) * np.pi/360.0)) * k
    return x,y

def dataframe_minutes_to_degrees(df,deg:str,min:str,label:str,sec:str=None):
    if sec:
        deg_fin = df[deg] + (df[min]/60) + (df[sec]/3600)
    else:
        deg_fin = df[deg] + (df[min]/60)
    df[label] = deg_fin
    return df

def dataframe_wgs84_to_mercator(df,lat:str,lon:str):
    k = 6378137
    df['x'] = df[lon] * (k * np.pi/180.0)
    df['y'] = np.log(np.tan((90 + df[lat]) * np.pi/360.0)) * k
    return df