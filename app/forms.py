from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired, Length

from app.models import User


class LoginForm(FlaskForm):
    login = StringField('login', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class EditForm(FlaskForm):
    nickname = StringField('nickname', validators=[DataRequired()])
    about_me = StringField('about_me', validators=[Length(min=0, max=140)])

    def __init__(self, original_nickname, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_nickname = original_nickname

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        if self.nickname.data == self.original_nickname:
            return True
        user = User.query.filter_by(nickname=self.nickname.data).first()
        if user is not None:
            self.nickname.errors.append('This nickname is already in use. Please choose another one.')
            return False
        return True


class PostForm(FlaskForm):
    post = StringField('post', validators=[DataRequired()])


class SearchForm(FlaskForm):
    search = StringField('search', validators=[DataRequired()])
