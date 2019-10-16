import click
from flask.cli import with_appcontext

from companyblog import db
from .models import User, BlogPost, Tag, Comment

@click.command(name='create_tables')
@with_appcontext
def create_tables():
    db.create_all()