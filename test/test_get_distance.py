'''
Created on Aug 6, 2021

@author: wacero
'''
import pytest
import get_distance

def test_get_nearest_city():
    
    epn_location = (-0.210402, -78.488553)
    distance_expected = 2.52
    city_expected = 'Quito'
    
    distance_test, city_test = get_distance.get_nearest_city(epn_location)
    
    assert distance_test == distance_expected
    assert city_test == city_expected
