'''
Created on Aug 6, 2021

@author: wacero
'''

from flask import Flask, request, Response, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from . import main
from . import get_distance


#security_token = generate_password_hash(current_app.config['ACCESS_TOKEN'])
#security_token = generate_password_hash('clavemuysecreta')
@main.route('/get_nearest_city')
def call_get_nearest_city():

    security_token = generate_password_hash(current_app.config['ACCESS_TOKEN'])
    
    token = request.args.get('token')
    
    if check_password_hash(security_token, token):
        lat = float(request.args.get('lat'))
        lon = float(request.args.get('lon'))
        event_location = (lat,lon)
        print(event_location)
        return str(get_distance.get_nearest_city(event_location,current_app.config['CITIES_FILE']))
    
