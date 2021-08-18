
import os

from nearest_city_distance import create_app



app = create_app(os.getenv('FLASK_CONFIG') or 'default')



if __name__ == '__main__':
    app.run()
