'''
Created on Aug 6, 2021

@author: wacero
'''


from flask import Flask, request, Response
from werkzeug.security import generate_password_hash, check_password_hash

import get_distance

app = Flask(__name__)

# TEMPORAL

security_token = generate_password_hash("clavemuysecreta")


@app.route('/get_nearest_city')
def call_get_nearest_city():

    """
    This function returns the name of the country to an event

    Country name is given in ascii.

    :returns: str(get_distance.get_nearest_city(event_location))
    :rtype: String
    """

    token = request.args.get('token')

    if check_password_hash(security_token, token):
        lat = float(request.args.get('lat'))
        lon = float(request.args.get('lon'))
        event_location = (lat, lon)
        print(event_location)
        return str(get_distance.get_nearest_city(event_location))


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
