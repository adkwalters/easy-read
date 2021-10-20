from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField
from wtforms.validators import DataRequired

from app.models import Article


class ArticleForm(FlaskForm):
    article_id = IntegerField('Id')
    article_title = StringField('Title', validators=[DataRequired()])
    article_desc = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Save Article')
    