from flask import render_template, request, Blueprint
from companyblog.models import BlogPost

core = Blueprint('core', __name__)

@core.route('/')
def index():
    """Renders homepage and lists all blogposts in paginated form """
    page = request.args.get("page", 1, type=int)
    blog_posts = BlogPost.query.order_by(BlogPost.date.desc()).paginate(page=page, per_page=5)
    return render_template('index.html', blog_posts=blog_posts)

@core.route('/info')
def info():
    """Renders About page with info about the company"""
    return render_template('info.html')