import os

class Config(object):
    DEBUG = False
    TESTING = False
    SECURITY_PASSWORD_SALT = 'my_precious_two'
    TEMPLATES_AUTO_RELOAD = True
    S3_BUCKET = "yestomeetyou"
    S3_KEY = os.environ.get('s3_key')
    S3_SECRET = os.environ.get('s3_secret')
    S3_LOCATION = "f'http://{S3_BUCKET}.s3.amazonaws.com/'"
    LANGUAGES = {
        'fr': 'Français',
        'nl': 'Dutch'
    }
    BABEL_DEFAULT_LOCALE = 'fr'


class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = '2230f815e1d443d5b7cd96f2b73af0bf'
    MYSQL_DB_NAME = os.environ.get('db_name')
    MYSQL_DB_USERNAME = os.environ.get('db_username')
    MYSQL_DB_PASSWORD = os.environ.get('db_password')
    MYSQL_DB_HOST = os.environ.get('db_host')
    MAIL_SERVER = 'email-smtp.eu-west-1.amazonaws.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('mail_username')
    MAIL_PASSWORD = os.environ.get('mail_password')
    MAIL_DEFAULT_SENDER = 'no-reply@yestomeetyou.com'
    CELERY_BROKER_URL = os.environ.get('redis_server')

class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = 'my-secret'
    MAIL_SERVER = 'email-smtp.eu-west-1.amazonaws.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('mail_username')
    MAIL_PASSWORD = os.environ.get('mail_password')
    MYSQL_DB_NAME = "yestomeet"
    MYSQL_DB_USERNAME = "root"
    MYSQL_DB_PASSWORD = ""
    MYSQL_DB_HOST = "localhost"
    MAIL_DEFAULT_SENDER = 'no-reply@yestomeetyou.com'
    CELERY_BROKER_URL = 'redis://127.0.0.1:6379'
