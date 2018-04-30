from flask import Blueprint, request, flash, render_template, jsonify, session, url_for, redirect
from sqlalchemy import exc
from ..forms import RestaurantBaseForm, RestaurantOpeningHoursForm,\
    RestaurantSocialMediaForm, MenuSetup, MenuItems, OrdersHampersMethods, \
    OrdersHampersTiming, Employees
from app import db_session
from app.models import RestaurantBaseInformation, OpeningHours, SocialMedia, \
    MenuSetUp, MenuItems as MenuItemsTable, PickUp, Delivery, OrdersTiming, Employee
from werkzeug.utils import secure_filename
import os
import app.utilities
from importlib import reload


Omod = Blueprint('owner_panel', __name__,
                 template_folder='templates',
                 static_folder='static')


@Omod.route('/restaurant', methods=['GET', 'POST'])
def restaurant():
    if session.get('owner_logged_in'):
        base_form = RestaurantBaseForm()
        opening_form = RestaurantOpeningHoursForm()
        media_form = RestaurantSocialMediaForm()

        if request.method == 'POST':
            if base_form.base_submit.data and base_form.validate():

                data = {
                    'restaurant_name': base_form.restaurant_name.data,
                    'restaurant_about': base_form.restaurant_about.data,
                    'restaurant_img': os.path.join('img/home_page/',
                                                   uploadimage(base_form.restaurant_welcome_img,
                                                               'app\owner_panel\static\img\home_page')),
                    'restaurant_address_line': base_form.restaurant_address_line.data,
                    'restaurant_city': base_form.restaurant_city.data,
                    'restaurant_country': base_form.restaurant_country.data,
                    'restaurant_zipcode': base_form.restaurant_zipcode.data,
                    'restaurant_email': base_form.restaurant_email.data,
                    'restaurant_phone_number': base_form.restaurant_phone.data,
                    'restaurant_logo': os.path.join("img/home_page/",
                                                    uploadimage(base_form.restaurant_logo,
                                                                "app\owner_panel\static\img\home_page")),
                }

                updatedata(data, RestaurantBaseInformation)

            elif opening_form.opening_submit.data and opening_form.validate():
                data = {
                    'from_date': opening_form.from_hour.data,
                    'to_date': opening_form.to_hour.data,
                    'saturday': 0,
                    'sunday': 0,
                    'monday': 0,
                    'tuesday': 0,
                    'wednesday': 0,
                    'thursday': 0,
                    'friday': 0,
                }

                for key, value in data.items():
                    for day in opening_form.opening_days.data:
                        if key == day:
                            data[day] = 1

                updatedata(data, OpeningHours)

            elif media_form.media_submit.data and media_form.validate():
                data = {}
                for k, v in media_form.data.items():
                    if v is not '' and k is not 'csrf_token' and k is not 'media_submit':
                        if v.lower().startswith('https://'):
                            data[k] = v[8:]
                        elif v.lower().startswith('http://'):
                            data[k] = v[7:]
                        else:
                            data[k] = v
                update_social_media(data)
        reload(app.utilities)
        return render_template('owner_restaurant.html',
                               base_form=base_form,
                               opening_form=opening_form,
                               media_form=media_form,
                               restaurant_name=app.utilities.restaurant_name,
                               restaurant_about=app.utilities.restaurant_about,
                               restaurant_address_line=app.utilities.restaurant_address_line,
                               restaurant_city=app.utilities.restaurant_city,
                               restaurant_country=app.utilities.restaurant_country,
                               restaurant_zipcode=app.utilities.restaurant_zipcode,
                               restaurant_email=app.utilities.restaurant_email,
                               restaurant_phone_number=app.utilities.restaurant_phone_number,
                               from_date=app.utilities.from_date,
                               to_date=app.utilities.to_date,
                               working_days=app.utilities.working_days,
                               facebook=app.utilities.facebook,
                               twitter=app.utilities.twitter,
                               snapchat=app.utilities.snapchat,
                               instagram=app.utilities.instagram,
                               yelp=app.utilities.yelp,
        )
    return redirect(url_for('RPOSS.login'))


@Omod.route('/menu', methods=['GET', 'POST'])
def menu():
    if session.get('owner_logged_in'):
        menu_setup_form = MenuSetup()
        menu_items_form = MenuItems()

        if request.method == 'POST':
            if menu_setup_form.menu_setup_submit.data and menu_setup_form.validate():

                data = {
                    'restaurant_image': os.path.join('img/home_page/',
                                                     uploadimage(menu_setup_form.restaurant_menu_image,
                                                                 "app\owner_panel\static\img\home_page")),
                    'restaurant_description': menu_setup_form.restaurant_menu_description.data,
                }

                updatedata(data, MenuSetUp)

            elif menu_items_form.menu_items_submit.data and menu_items_form.validate():

                data = {
                    'item_name': menu_items_form.item_name.data,
                    'item_category': menu_items_form.item_category.data,
                    'item_status': menu_items_form.item_status.data,
                    'item_price': menu_items_form.item_price.data,
                    'item_size': menu_items_form.item_size.data,
                    'item_image': os.path.join('static/img/menu_items/', uploadimage(menu_items_form.item_image,
                                                                                     "app\owner_panel\static\img\menu_items")),
                }

                add_menu_item(data)
        reload(app.utilities)
        return render_template('owner_menu.html',
                               menu_setup_form=menu_setup_form,
                               menu_items_form=menu_items_form,
                               menu_description=app.utilities.menu_description)
    return redirect(url_for('RPOSS.login'))


@Omod.route('/get_menu_items', methods=['GET'])
def get_menu_items():
    menu_items = db_session.query(MenuItemsTable).all()
    return jsonify([i.serialize for i in menu_items])


@Omod.route('/get_employees_accounts', methods=['GET'])
def get_employees_accounts():
    employees = db_session.query(Employee).all()
    return jsonify([i.serialize for i in employees])


@Omod.route('/delete_menu_item/<int:item_id>', methods=["DELETE"])
def delete_menu_item(item_id):
    db_session.query(MenuItemsTable).filter(MenuItemsTable.item_id == item_id).delete()
    db_session.commit()
    return jsonify({'success': True}), 200, {'ContentType': 'application/json'}


@Omod.route('/delete_employee_account/<int:employee_id>', methods=["DELETE"])
def delete_employee_account(employee_id):
    db_session.query(Employee).filter(Employee.employee_id == employee_id).delete()
    db_session.commit()
    return jsonify({'success': True}), 200, {'ContentType': 'application/json'}


@Omod.route('/modify_menu_item/<int:item_id>/<string:status>', methods=['PUT'])
def modify_menu_item(item_id, status):
    db_session.query(MenuItemsTable).filter(MenuItemsTable.item_id == item_id). \
        update({"item_status": status.lower()})
    db_session.commit()
    return jsonify({'success': True}), 200, {'ContentType': 'application/json'}


@Omod.route('/modify_employee_status/<int:employee_id>/<string:status>', methods=['PUT'])
def modify_employee_status(employee_id, status):
    db_session.query(Employee).filter(Employee.employee_id == employee_id). \
        update({"employee_status": status.lower()})
    db_session.commit()
    return jsonify({'success': True}), 200, {'ContentType': 'application/json'}


@Omod.route('/orders_hampers', methods=['GET', 'POST'])
def orders_hampers():
    if session.get('owner_logged_in'):
        orders_methods_form = OrdersHampersMethods()
        orders_timing_form = OrdersHampersTiming()

        if request.method == 'POST':
            if orders_methods_form.methods_submit.data and orders_methods_form.validate():

                pickup_data = {
                    "allow_pickup":  orders_methods_form.allow_pickup.data,
                    "pickup_tax":  orders_methods_form.pickup_tax.data,
                }
                delivery_data = {
                    "allow_delivery":  orders_methods_form.allow_delivery.data,
                    "delivery_tax":  orders_methods_form.delivery_tax.data,
                    "delivery_charges": orders_methods_form.delivery_charges.data,
                    "min_amount":  orders_methods_form.min_order_amount.data,
                    "max_amount":  orders_methods_form.max_order_amount.data,
                }

                updatedata(pickup_data, PickUp)
                updatedata(delivery_data, Delivery)

            elif orders_timing_form.timing_submit.data and orders_timing_form.validate():
                data = {
                    "delivery_time": orders_timing_form.delivery_time.data,
                    "preparing_time": orders_timing_form.preparing_time.data,
                    "pending_time": orders_timing_form.pending_time.data,
                }

                updatedata(data, OrdersTiming)
        reload(app.utilities)
        return render_template('owner_orders_hampers.html',
                               orders_methods_form=orders_methods_form,
                               orders_timing_form=orders_timing_form,
                               allow_pickup=app.utilities.pickup_allowed,
                               allow_delivery=app.utilities.delivery_allowed,
                               delivery_taxes=app.utilities.delivery_tax,
                               pickup_tax=app.utilities.pickup_tax,
                               delivery_charges=app.utilities.delivery_charges,
                               min_amount=app.utilities.min_amount,
                               max_amount=app.utilities.max_amount,
                               delivery_time=app.utilities.delivery_time,
                               preparing_time=app.utilities.preparing_time,
                               pending_time=app.utilities.pending_time)
    return redirect(url_for('RPOSS.login'))


@Omod.route('/employees_registration', methods=['GET', 'POST'])
def employees_registration():
    if session.get('owner_logged_in'):
        employee_form = Employees()
        if request.method == 'POST' and employee_form.validate():
            data = {
                'employee_username': employee_form.employee_name.data,
                'employee_email': employee_form.employee_email.data,
                'employee_status': 'active',
                'employee_password': employee_form.employee_password.data,
            }

            add_employee(data)

        return render_template('owner_employees.html',
                               employees_form=employee_form)
    return redirect(url_for('RPOSS.login'))


@Omod.route('/system_interfaces', methods=['GET'])
def system_interfaces():
    if session.get('owner_logged_in'):
        return render_template('owner_system_interfaces.html')
    return redirect(url_for('RPOSS.login'))


def uploadimage(form_field, path):
    image = form_field.data
    image_name = secure_filename(image.filename)
    image.save(os.path.join(os.path.abspath(path), image_name))
    return image_name


def updatedata(data, model):
    try:
        db_session.query(model).filter(model.id == 1).update(data)
        db_session.commit()
        flash("information updated successfully", "success")
    except exc.SQLAlchemyError as e:
        print(e)
        db_session.rollback()
        flash('there was an error committing your data.', 'danger')


def update_social_media(data):
    try:
        for i, k in enumerate(data, start=1):
            db_session.query(SocialMedia).filter(SocialMedia.site_id == i). \
                update({'site_link': data[k]})
        db_session.commit()
        flash('Restaurant social media accounts committed successfully .', 'success')
    except exc.SQLAlchemyError:
        db_session.rollback()
        flash('there was an error committing your data.', 'danger')


def add_menu_item(data):
    try:
        new_item = MenuItemsTable(item_name=data['item_name'],
                                  item_category=data['item_category'],
                                  item_status=data['item_status'],
                                  item_price=data['item_price'],
                                  item_size=data['item_size'],
                                  item_image=data['item_image'])
        db_session.add(new_item)
        db_session.commit()
        db_session.refresh(new_item)
        flash('Item {} added successfully .'.format(data['item_name']), 'success')
    except exc.SQLAlchemyError:
        db_session.rollback()
        flash('there was an error committing your data.', 'danger')


def add_employee(data):
    try:
        new_employee = Employee(employee_username=data['employee_username'],
                                employee_email=data['employee_email'],
                                employee_status=data['employee_status'])
        new_employee._set_password = data['employee_password']
        db_session.add(new_employee)
        db_session.commit()
        db_session.refresh(new_employee)
        flash('Employee {} added successfully .'.format(data['employee_username']), 'success')
    except exc.SQLAlchemyError as e:
        db_session.rollback()
        flash('there was an error committing your data.', 'danger')
