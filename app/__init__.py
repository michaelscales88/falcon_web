from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager

from .momentjs import MomentJs

app = Flask(__name__, instance_relative_config=True)

# Load the default configuration
app.config.from_object('app.configmodule.DevelopmentConfig')

# Load the configuration from the instance folder
app.config.from_pyfile('config.cfg', silent=True)

# create app dB
db = SQLAlchemy(app)

# Mailing service
mail = Mail(app)

# Render UTC dates based on browser settings
app.jinja_env.globals['momentjs'] = MomentJs

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

if app.config['ENABLE_SEARCH']:
    from whooshalchemy import IndexService
    from app.models import Post
    index_service = IndexService(config=app.config)
    index_service.register_class(Post)

if not app.debug:
    import logging
    from logging.handlers import SMTPHandler
    credentials = None

    if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
        credentials = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])

    mail_handler = SMTPHandler(
        (app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
        'no-reply@' + app.config['MAIL_SERVER'],
        app.config['ADMINS'],
        'microblog failure',
        credentials
    )

    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

    from logging.handlers import RotatingFileHandler

    file_handler = RotatingFileHandler('app/tmp/falcon_web.log', 'a', 1 * 1024 * 1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('falcon startup')


from app import views, models
from app.models import User, Post

