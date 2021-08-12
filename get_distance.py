# -*- coding: utf-8 -*-
'''
Created on Aug 5, 2021

@author: wacero
'''


import pandas as pd
from  scipy.spatial import distance
import numpy as np
from geopy.distance import distance as geodist

world_cities_file="./world_cities.csv"


def get_nearest_city(event_location):
    
    """
    This function return the nearest city and distance to an event. 
    
    :param tupla event_location
    :returns: tupla: distance in kilometers and city name in ascii. 
    """
    event_location = np.array([event_location])
    cities=pd.read_csv(world_cities_file)
    
    cities_location=np.array(list(zip(cities.lat, cities.lng)))
    
    distance_array=distance.cdist(cities_location,event_location, lambda u, v: geodist(u,v) . kilometers )
    
    min_distance=np.amin(distance_array)
    
    index = np.where(distance_array == min_distance) 
    
    city = cities.city_ascii[index[0][0]]
    
    return round(min_distance,2),city



