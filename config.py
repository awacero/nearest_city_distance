import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN') or  'clavemuysecreta'
    CITIES_FILE = os.path.join(basedir,'./data/world_cities_RG.csv')
    COUNTRY_FILE = os.path.join(basedir,'./data/ec_pe_co.shp')

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config): 

    DEBUG = False

config = {
        'development': DevelopmentConfig,
        'production': ProductionConfig, 

        'default': DevelopmentConfig

            }
