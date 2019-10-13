import os
from flask import url_for,render_template, request, redirect, flash, Blueprint
from flask_login import login_user,current_user,logout_user,login_required
from werkzeug.urls import url_parse

from companyblog import db
from companyblog.models import User, BlogPost
from companyblog.users.forms import LoginForm, RegistrationForm, UpdateUserForm
from companyblog.users.picture_handler import add_profile_pic


users = Blueprint('users', __name__)

# register
@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You have succesfully registered!', 'success')
        return redirect(url_for("users.login"))
    return render_template("register.html", form=form)
        


# login
@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('core.index'))
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password', 'warning')
            return redirect(url_for('users.login'))
        login_user(user)
        flash("You've been logged in!", 'success')
        next = request.args.get('next')
        if not next or url_parse(next).netloc != '':
            next = url_for('core.index')
        return redirect(next)
    return render_template('login.html', form=form)


# logout
@users.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You've been logged out!", 'success')
    return redirect(url_for("core.index"))

# account/update
@users.route('/account', methods=['GET','POST'])
@login_required
def account():
    form = UpdateUserForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        if form.picture.data:
            email = current_user.email
            pic = add_profile_pic(form.picture.data, email)
            current_user.profile_image = pic
        db.session.commit()
        flash("User account succesfully updated!", "success")
        return redirect(url_for("users.account"))

    elif request.method == "GET":
        form.email.data = current_user.email
        form.username.data = current_user.username

    profile_image = url_for('static',filename='profile_pics/'+ current_user.profile_image)

    return render_template("account.html", profile_image=profile_image, form=form)


# users list of blog posts

@users.route("/<username>")
def user_posts(username):
    page = request.args.get("page",1,type=int)
    user = User.query.filter_by(username=username).first_or_404()
    # try to do user.posts instead of blogpost.query.filter_by(author=user)
    blog_posts = BlogPost.query.filter_by(author=user).order_by(BlogPost.date.desc()).paginate(page=page,per_page=5)
    return render_template("user_blog_posts.html", blog_posts=blog_posts, user=user)