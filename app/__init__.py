from flask import Flask
from flask_sqlalchemy import SQLAlchemy


from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('app.config.MainConfig')
db = SQLAlchemy(app)

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

