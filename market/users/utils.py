import os
import secrets
from PIL import Image
from flask import url_for
from flask_mail import Message
from shopping_website.market import mail


def save_image_file(image_file):
    random_hex = secrets.token_hex(8)
    _, pic_ext = os.path.splitext(image_file.filename)
    pic_name = random_hex + pic_ext
    pic_path = os.path.join('market/static/profile_pics', pic_name)
    output_size = (125, 125)
    i = Image.open(image_file)
    i.thumbnail(output_size)
    i.save(pic_path)
    return pic_name


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset request', sender='pary143@gmail.com', recipients=[user.email])
    msg.body = f"""To reset your password, visit the following link: 
{url_for('users.reset_password', token=token, _external=True)}

If you did not made this request then simply ignore this email and no changes will be made."""
    mail.send(msg)
