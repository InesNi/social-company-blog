from flask import render_template, redirect, request, flash,url_for, Blueprint
from flask_login import current_user, login_required
from companyblog import db
from companyblog.models import BlogPost
from companyblog.blog_posts.forms import BlogPostForm


blog_posts = Blueprint('blog_posts', __name__)


# CREATE
@blog_posts.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = BlogPostForm()

    if form.validate_on_submit():
        blog_post = BlogPost(title=form.title.data,
                        text=form.text.data,
                        user_id=current_user.id)
        db.session.add(blog_post)
        db.session.commit()
        flash('Blog post successfully created!', 'success')
        return redirect(url_for('core.index'))
    return render_template('create_post.html', form=form)

# VIEW
@blog_posts.route('/<int:blog_post_id>')
def view_post(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    return render_template('view_post.html', title=blog_post.title, text=blog_post.text, date=blog_post.date, post=blog_post)


# UPDATE
@blog_posts.route('/<int:blog_post_id>/update', methods=['GET', 'POST'])
@login_required
def update(blog_post_id):

    blog_post = BlogPost.query.get_or_404(blog_post_id)
    if blog_post.author != current_user:
        abort(403)

    form = BlogPostForm()

    if form.validate_on_submit():
        blog_post.title = form.title.data
        blog_post.text = form.text.data
        db.session.commit()
        flash('Blog post successfully updated', 'success')
        return redirect(url_for('blog_posts.view_post', blog_post_id=blog_post.id))

    elif request.method == 'GET':
        form.title.data = blog_post.title
        form.text.data = blog_post.text
        
    return render_template('create_post.html', form=form)

# DELETE
@blog_posts.route('/<int:blog_post_id>/delete', methods=['GET', 'POST'])
@login_required
def delete(blog_post_id):

    blog_post = BlogPost.query.get_or_404(blog_post_id)
    if blog_post.author != current_user:
        abort(403)
    db.session.delete(blog_post)
    db.session.commit()
    flash('Blog post successfully deleted', 'success')
    return redirect(url_for('core.index'))