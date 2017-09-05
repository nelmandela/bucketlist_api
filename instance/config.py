import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv("nelson")
    SQLALCHEMY_DATABASE_URI = os.getenv("sqlite:///localhost/test_db")

class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = ('sqlite:///' +
                                   os.path.join(basedir, 'bucketlist.db'))
class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    JWT_AUTH_URL_RULE = "/auth/login"
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = ('sqlite:///' +
                                os.path.join(basedir, 'bucketlist_test.db'))


class StagingConfig(Config):
    """Configurations for Staging."""
    DEBUG = True

class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False

app_config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "staging": StagingConfig,
    "production": ProductionConfig,
}

