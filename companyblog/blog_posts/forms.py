from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError
from companyblog.models import BlogPost

class BlogPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    text = TextAreaField('Text', validators=[DataRequired()])
    submit = SubmitField('Post')

    def validate_title(self,form):
            if BlogPost.query.filter_by(title=self.title.data).first():
                raise ValidationError('Post with this title already exists, please choose another title')

class UpdatePostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    text = TextAreaField('Text', validators=[DataRequired()])
    submit = SubmitField('Post')

    def __init__(self, orig_title, *args, **kwargs):
        super(UpdatePostForm, self).__init__(*args, **kwargs)
        self.orig_title = orig_title

    def validate_title(self,title):
        if self.title.data != self.orig_title:
            post = BlogPost.query.filter_by(title=self.title.data).first()
            if post:
                raise ValidationError('Post with this title already exists, please choose another title')
