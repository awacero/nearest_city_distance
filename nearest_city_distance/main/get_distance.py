# -*- coding: utf-8 -*-
'''
Created on Aug 5, 2021

@author: wacero
'''

import io
import numpy as np
from geopy.distance import distance as geodist
import reverse_geocoder
from config import config


import unicodedata
world_cities_file = config['default'].CITIES_FILE


def get_nearest_city(event_location):

    """
    This function return the nearest city and distance to an event.
    Distance is given in kilometers and city name in ascii.

    :param event_location: (latitude,longitude)
    :type event_location: tupla
    :returns: round(distance, 2)
    :returns: city
    :returns: province
    """
    event_location = np.array([event_location])
    geo_object =\
        reverse_geocoder.RGeocoder(mode=2, verbose=True,
                                   stream=io.StringIO(open(world_cities_file,
                                   encoding='utf-8').read()))

    result = geo_object.query(event_location)
    city = result[0]['name']
    province = result[0]['admin1']
    province = str(unicodedata.
                   normalize('NFKD', province).encode('ascii', 'ignore'),
                   encoding='utf-8')
    city_location = (result[0]['lat'], result[0]['lon'])
    distance = geodist(event_location, city_location).kilometers

    return round(distance, 2), city, province
