from flask import Blueprint, request, render_template, jsonify, redirect, url_for
from ..forms import ContactUsForm, CustomerDetailsForm
from instance.config import send_mail
from app import db_session
from app.models import MenuItems, Delivery, RestaurantBaseInformation
from app.utilities import pickup_options, query


Cmod = Blueprint('customer', __name__,
                 template_folder='templates',
                 static_folder='static',
                 static_url_path='/customer/static')


@Cmod.route("/", methods=['GET', 'POST'])
def index():
    contact_us_form = ContactUsForm()

    if request.method == 'POST' and contact_us_form.validate():
        customer_name = contact_us_form.customer_name.data
        customer_phone = contact_us_form.customer_phone.data
        customer_email = contact_us_form.customer_email.data
        customer_message = contact_us_form.customer_message.data

        send_mail(customer_name, customer_message, customer_email, customer_phone)

    return render_template('index.html',
                           contact_us_form=contact_us_form)


@Cmod.route("/menu", methods=['GET'])
def menu():
    # get delivery orders hampers
    allow_delivery = query(model_column=Delivery.allow_delivery)
    delivery_taxes = query(model_column=Delivery.delivery_tax)
    delivery_charges = query(model_column=Delivery.delivery_charges)
    min_amount = query(model_column=Delivery.min_amount)
    max_amount = query(model_column=Delivery.max_amount)

    return render_template('menu.html',
                           allow_delivery=allow_delivery,
                           delivery_taxes=delivery_taxes,
                           delivery_charges=delivery_charges,
                           min_amount=min_amount,
                           max_amount=max_amount
                           )


@Cmod.route("/get_menu_items", methods=['GET'])
def get_menu_items():
    categories_set = set()
    menu_items = db_session.query(MenuItems).all()
    # get categories out
    for item in menu_items: categories_set.add(item.item_category)
    # CMS
    categorized_menu_items = {}
    for category in categories_set:
        category_items = db_session.query(MenuItems).filter(MenuItems.item_category == category).all()
        serialized_category_items = [item.serialize for item in category_items]
        categorized_menu_items[category] = serialized_category_items
    return jsonify(categorized_menu_items)


@Cmod.route("/few_steps", methods=['GET', 'POST'])
def few_steps():
    customer_details_form = CustomerDetailsForm()
    if request.method == 'POST' and customer_details_form.validate():
        customer_name = customer_details_form.customer_name.data
        customer_phone = customer_details_form.customer_phone.data
        customer_email = customer_details_form.customer_email.data
        order_method = customer_details_form.order_method.data
        address_line1 = customer_details_form.address_line1.data
        address_line2 = customer_details_form.address_line2.data
        state = customer_details_form.state.data
        zipcode = customer_details_form.zipcode.data
        notes = customer_details_form.notes.data
    elif request.method == 'POST':
        return render_template('few_steps.html',
                               customer_details_form=customer_details_form)
    return redirect(url_for('.menu'))


@Cmod.route("/phone_validation", methods=['GET', 'POST'])
def phone_validation():
    if request.method == 'POST':
        # request.form['code_field']
        pass
    return render_template('phone_validation.html')


@Cmod.route("/order_received", methods=['GET'])
def order_received():
    return render_template('order_received.html')
