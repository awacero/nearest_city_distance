'''
Created on Aug 6, 2021

@author: wacero
'''
import pytest
import os,sys

from nearest_city_distance.main import get_distance
from nearest_city_distance.main import get_country



epn_location = (-0.210402, -78.488553)
distance_expected = 2.52
city_expected = 'Quito'
province_expected = 'Pichincha'
country_expected = 'Ecuador'

def test_get_nearest_city():
        
    distance_test, city_test,province_test = get_distance.get_nearest_city(epn_location)
    
    assert distance_test == distance_expected
    assert city_test == city_expected
    assert province_test == province_expected
    
def test_get_country():
    
    country_test = get_country.get_country(epn_location)
    
    assert country_test == country_expected
    

