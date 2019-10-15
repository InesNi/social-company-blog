from flask import render_template, redirect, request, flash,url_for, Blueprint
from flask_login import current_user, login_required
from companyblog import db
from companyblog.models import BlogPost
from companyblog.blog_posts.forms import BlogPostForm, UpdatePostForm


blog_posts = Blueprint('blog_posts', __name__)


def get_or_create_tag(label):
    tag = Tag.query.filter_by(tag=label).first()
    if not tag:
        tag = Tag(label)
        db.session.add(tag)
        db.session.commit()
    return tag
    

def slugify(data):
    slug = data.strip().lower().replace(' ', '-')


def tags_from_string(str_tags, post):
    """Gets or creates tags given in string format and
    creates relationship between them and post if nonexistant
    """
    new_tags = str_tags.strip().split(',')
    for item in new_tags:
        if item not in string.whitespace:
            tag = get_or_create_tag(item)
            post.tag(tag)
    return new_tags


def update_tags(post, form):
    """Updates tags of post with data provided in form"""
    new_tags = tags_from_string(form.tags.data, post)
    for tag in post.tags:
        if tag.tag not in new_tags:
            post.untag(tag)
            if not tag.posts:
                db.session.delete(tag)
                db.session.commit()


def update_post_from_form(post, form):
    """Updates post with data provided in form"""
    for field,data in request.form.items():
            if field != 'tags':
                setattr(post, field, data)
    post.slug=slugify(form.title.data)
    post.author=current_user._get_current_object()
    db.session.commit()
    update_tags(post, form)


# CREATE
@blog_posts.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = BlogPostForm()

    if form.validate_on_submit():
        blog_post = BlogPost(
                    title=form.title.data,
                    text=form.text.data,
                    user_id=current_user.id,
                    slug=slugify(form.title.data)
        )
        tags_from_string(form.tags.data, blog_post)
        db.session.add(blog_post)
        db.session.commit()
        flash('Blog post successfully created!', 'success')
        return redirect(url_for('core.index'))
    return render_template('create_post.html', form=form)

# VIEW
@blog_posts.route('/post/<slug>')
def view_post(slug):
    blog_post = BlogPost.query.filter_by(slug=slug).first_or_404()
    return render_template('view_post.html', title=blog_post.title, text=blog_post.text, date=blog_post.date, post=blog_post)


# UPDATE
@blog_posts.route('/<slug>/update', methods=['GET', 'POST'])
@login_required
def update(slug):

    blog_post = BlogPost.query.filter_by(slug=slug).first_or_404()
    if blog_post.author != current_user:
        abort(403)

    form = UpdatePostForm(orig_title=blog_post.title)

    if form.validate_on_submit():
        update_from_form(blog_post, form)
        flash('Blog post successfully updated', 'success')
        return redirect(url_for('blog_posts.view_post', slug=blog_post.slug))

    elif request.method == 'GET':
        form.title.data = blog_post.title
        form.text.data = blog_post.text
        form.tags.data = ','.join([tag.tag for tag in blog_post.tags])
        
    return render_template('create_post.html', form=form)

# DELETE
@blog_posts.route('/<slug>/delete', methods=['GET', 'POST'])
@login_required
def delete(slug):

    blog_post = BlogPost.query.filter_by(slug=slug).first_or_404()
    if blog_post.author != current_user:
        abort(403)
    db.session.delete(blog_post)
    db.session.commit()
    flash('Blog post successfully deleted', 'success')
    return redirect(url_for('core.index'))