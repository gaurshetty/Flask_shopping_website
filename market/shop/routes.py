from shopping_website.market.models import Item
from shopping_website.market.shop.forms import PurchaseItemForm, SellItemForm
from flask import request, render_template, redirect, url_for, flash, Blueprint
from flask_login import login_required, current_user
shop = Blueprint('shop', __name__)


@shop.route('/market/', methods=['GET', 'POST'])
@login_required
def market():
    purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()
    if request.method == "POST":
        # Purchase Item Logic
        purchased_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name=purchased_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(f"Congratulations! You purchased {p_item_object.name} for {p_item_object.price}$", category='success')
            else:
                flash(f"Unfortunately, you don't have enough money to purchase {p_item_object.name}!", category='danger')
        # Sell Item Logic
        sold_item = request.form.get('sold_item')
        s_item_object = Item.query.filter_by(name=sold_item).first()
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)
                flash(f"Congratulations! You sold {s_item_object.name} back to shop!", category='success')
            else:
                flash(f"Something went wrong with selling {s_item_object.name}", category='danger')
        return redirect(url_for('shop.market'))

    if request.method == "GET":
        page = request.args.get('page', 1, type=int)
        items = Item.query.filter_by(owner=None).paginate(page=page, per_page=5)
        owned_items = Item.query.filter_by(owner=current_user.id).all()
        return render_template('market.html', items=items, purchase_form=purchase_form, owned_items=owned_items,
                               selling_form=selling_form)
