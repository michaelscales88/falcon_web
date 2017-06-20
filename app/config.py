import os


class MainConfig(object):
    WTF_CSRF_ENABLED = True
    SECRET_KEY = 'you-will-never-guess'

    BASEDIR = os.path.abspath(os.path.dirname(__file__))

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'app.db')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(BASEDIR, 'db_repository')
    SQLALCHEMY_TRACK_MODIFICATIONS = True   # Turn this off to reduce overhead

    # indexing service
    WHOOSH_BASE = os.path.join(BASEDIR, 'tmp/whoosh')
    ENABLE_SEARCH = True

    # mail server settings
    MAIL_SERVER = 'localhost'
    MAIL_PORT = 5001
    MAIL_USERNAME = None
    MAIL_PASSWORD = None

    # administrator list
    ADMINS = ['you@example.com']
