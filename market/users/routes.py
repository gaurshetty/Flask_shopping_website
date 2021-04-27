from shopping_website.market import db
from shopping_website.market.models import User
from flask import render_template, redirect, url_for, request, flash, Blueprint
from flask_login import current_user, login_user, logout_user
from shopping_website.market.users.forms import (RegisterForm, LoginForm, AccountForm, RequestResetForm,
                                                 ResetPasswordForm)
from shopping_website.market.users.utils import save_image_file, send_reset_email
users = Blueprint('users', __name__)


@users.route('/register/', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('shop.market'))
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data, email=form.email.data, password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        flash('User created successfully with username {}! Login to go for GM Market'.format(user_to_create.username),
              category='success')
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form)


@users.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('shop.market'))
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_match(form.password.data):
            login_user(attempted_user, remember=form.remember.data)
            flash('Login successful! Welcome {}!'.format(attempted_user.username), category='success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('shop.market'))
        else:
            flash('Login attempt failed! Try again with correct credentials.', category='danger')
    return render_template('login.html', form=form)


@users.route('/logout/')
def logout():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("main.home"))


@users.route('/account/', methods=['GET', 'POST'])
def account():
    form = AccountForm()
    if form.validate_on_submit():
        if form.image_file.data:
            picture = save_image_file(form.image_file.data)
            current_user.image_file = picture
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Account updated successfully!", category='success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', image_file=image_file, form=form)


@users.route('/reset_password/', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('shop.market'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('Reset password request mail sent to your email, please check your email.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', form=form)


@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('shop.market'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is and invalid or expired token! Try again.', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        User.password = form.password1.data
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_password.html', form=form)
