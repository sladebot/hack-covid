import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # Application settings
    APP_NAME = "Heimdallr"

    # Flask settings
    CSRF_ENABLED = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    HOST = '127.0.0.1'
    PORT = 9000


class ProductionConfig(Config):
    DEBUG = False
    HOST = '127.0.0.1'
    PORT = 5001

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}

