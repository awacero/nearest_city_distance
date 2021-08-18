# -*- coding: utf-8 -*-
'''
Created on Aug 16, 2021

@author: wacero
'''

from config import config
import shapefile
import numpy as np
import reverse_geocoder
import io

world_cities_file = config['default'].CITIES_FILE
country_shape_file = config['default'].COUNTRY_FILE

def point_in_polygon(location,polygon):
    
    n = len(polygon)
    inside = False
    y = location[0]
    x = location[1]
    p1x,p1y = polygon[0]
    for i in range(n+1):
        p2x,p2y = polygon[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x,p1y = p2x,p2y
    return inside

def get_nearest_country(location):
    
    location = np.array([location]) 
    geo_object = reverse_geocoder.RGeocoder(mode=2, verbose=True, stream=io.StringIO(open(world_cities_file, encoding='utf-8').read()))
    result = geo_object.query(location)
    country_name = result[0]['admin2']
    
    return country_name


def get_country(location):
    
    ec_co_pe_shape = shapefile.Reader(country_shape_file)
    country_name=0
    for i,record in enumerate(ec_co_pe_shape.records()):
        
        if point_in_polygon(location, ec_co_pe_shape.shape(i).points):
            
            country_name = record[0]
            country_name=country_name.capitalize()
            break
         
    if country_name:
        return country_name

    else:
        return get_nearest_country(location)
        


