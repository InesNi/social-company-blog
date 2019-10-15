from flask import render_template, redirect, request, flash,url_for, Blueprint
from flask_login import current_user, login_required
import string
from companyblog import db, app
from companyblog.models import BlogPost, Tag, post_tag, Comment
from companyblog.blog_posts.forms import BlogPostForm, UpdatePostForm, CommentForm


blog_posts = Blueprint('blog_posts', __name__)


def get_or_create_tag(label):
    tag = Tag.query.filter_by(tag=label).first()
    if not tag:
        tag = Tag(tag=label)
        db.session.add(tag)
        db.session.commit()
    return tag


def tags_from_string(str_tags, post):
    """Gets or creates tags given in string format and
    creates relationship between them and post if nonexistant
    """
    new_tags = str_tags.strip().split(',')
    print(new_tags)
    for item in new_tags:
        if item not in string.whitespace:
            print(item)
            tag = get_or_create_tag(item)
            print(tag.tag)
            post.tag(tag)
    for item in post.tags:
        print(item.tag)
    db.session.commit()
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


def update_from_form(post, form):
    """Updates post with data provided in form"""
    for field,data in request.form.items():
            if field != 'tags':
                setattr(post, field, data)
    post.slug=form.title.data.strip().lower().replace(' ', '-')
    post.author=current_user._get_current_object()
    db.session.commit()



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
                    slug=form.title.data.strip().lower().replace(' ', '-')
        )
        db.session.add(blog_post)
        db.session.commit()
        tags_from_string(form.tags.data, blog_post)
        flash('Blog post successfully created!', 'success')
        return redirect(url_for('core.index'))
    return render_template('create_post.html', form=form)

# VIEW
@blog_posts.route('/post/<slug>', methods=['GET', 'POST'])
def view_post(slug):
    page = request.args.get("page", 1, type=int)
    blog_post = BlogPost.query.filter_by(slug=slug).first_or_404()
    comments = Comment.query.filter(Comment.post_id == blog_post.id).order_by(
        Comment.timestamp.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
    form = CommentForm()

    if form.validate_on_submit():
        # if form.text is not None:
        comment = Comment(
            text=form.text.data,
            author=current_user._get_current_object(),
            post=blog_post
        )
        db.session.add(comment)
        db.session.commit()
        flash('Comment successfully posted!', 'success')
        return redirect(url_for('blog_posts.view_post', slug=blog_post.slug))
    return render_template('view_post.html', post=blog_post, comments=comments, form=form)


# VIEW BY TAG

@blog_posts.route('/posts/<tag>')
def posts_by_tag(tag):
    """Fetches all posts related to tag that is passed in"""
    page = request.args.get("page", 1, type=int)
    label = Tag.query.filter_by(tag=tag).first_or_404()
    posts = label.posts.order_by(BlogPost.date.desc()).paginate(page,
                                            app.config['POSTS_PER_PAGE'], False)
    return render_template(
        'posts_by_tag.html',
        title="Blog Post Entries|{}".format(tag),
        blog_posts=posts, tag=label
    )


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
        update_tags(blog_post, form)
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
    
    for tag in blog_post.tags:
        blog_post.untag(tag)
        if not tag.posts:
            db.session.delete(tag)

    db.session.delete(blog_post)
    db.session.commit()
    flash('Blog post successfully deleted', 'success')
    return redirect(url_for('core.index'))


# REMOVE COMMENT
@blog_posts.route('/remove_comment/<post_slug>/<int:id>')
@login_required
def remove_comment(id, post_slug):
    comment = Comment.query.filter_by(id=id).first_or_404()
    db.session.delete(comment)
    db.session.commit()
    flash('Comment successfully removed!', 'success')
    return redirect(url_for('blog_posts.view_post', slug=post_slug))
