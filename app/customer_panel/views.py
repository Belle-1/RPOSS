from flask import Blueprint, request, render_template, jsonify, redirect, url_for, flash, session
from ..forms import ContactUsForm, CustomerDetailsForm, DeliveryCustomerDetailsForm
from instance.config import send_mail
from app import db_session
from app.models import MenuItems, Delivery, RestaurantBaseInformation, Orders, OrderItems, Customers
from app.utilities import query, send_confirmation_code, is_number_valid
from sqlalchemy import exc
from twilio.base.exceptions import TwilioException
import datetime


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
    return render_template('menu.html',
                           allow_delivery=query(model_column=Delivery.allow_delivery),
                           delivery_taxes=query(model_column=Delivery.delivery_tax),
                           delivery_charges=query(model_column=Delivery.delivery_charges),
                           min_amount=query(model_column=Delivery.min_amount),
                           max_amount=query(model_column=Delivery.max_amount)
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
    delivery_customer_details_form = DeliveryCustomerDetailsForm()
    # if current day and time within the opening hours and days range that the owner specified then proceed
    # if not, customer can pick menu items but, can not place an order
    # a flash must indicate:
    # (you can place order within the restaurant opening hours\days dau1, day2, day3,... from 00:00 to 00:00)
    # just reroute to the same page (few_steps) with the aforementioned flash
    if request.method == 'POST':
        order_method = request.values.get('order-method')
        verified = False



        if order_method == 'Pick-up' and customer_details_form.validate():
            order_array = eval(request.cookies.get('order'))
            customer_name = customer_details_form.customer_name.data
            customer_phone = customer_details_form.customer_phone.data
            session['customer_phone'] = customer_phone
            customer_email = customer_details_form.customer_email.data
            address_line1 = ''
            address_line2 = ''
            state = ''
            zipcode = ''
            notes = ''

            try:
                is_number_valid(customer_phone)

                customer = Customers(customer_name=customer_name,
                                     customer_phone=customer_phone,
                                     customer_email=customer_email,
                                     customer_verified=verified)
                db_session.add(customer)
                db_session.commit()
                session['customer_id'] = customer.customer_id

                order = Orders(customer_id=customer.customer_id,
                               order_method=order_method.lower(),
                               datetime_made=datetime.datetime.now(),
                               status='pending',
                               notes=notes)

                db_session.add(order)
                db_session.commit()

                for item in order_array:
                    item = OrderItems(order_id=order.order_id,
                                      item_name=item['item_name'],
                                      item_quantity=item['item_qty'],
                                      item_size=item['item_size'],
                                      item_price=item['item_price'])
                    db_session.add(item)
                    db_session.commit()

            except exc.SQLAlchemyError as e:
                print('exc.SQLAlchemyError: ', e)
                flash('there was an error submitting your order, please try again later', 'danger')
            except TwilioException as e:
                print('TwilioException: ', e)
                flash('there was an error submitting your order, please include country key with your phone number and try again', 'danger')
            except:
                print('an error occurred :)')
            else:
                print('return success')
                return redirect(url_for('.phone_validation'))
            print('return failure')
            db_session.rollback()
            return render_template('few_steps.html',
                                   customer_details_form=customer_details_form,
                                   delivery_customer_details_form=delivery_customer_details_form,
                                   allow_delivery=query(model_column=Delivery.allow_delivery),
                                   delivery_taxes=query(model_column=Delivery.delivery_tax),
                                   delivery_charges=query(model_column=Delivery.delivery_charges),
                                   min_amount=query(model_column=Delivery.min_amount),
                                   max_amount=query(model_column=Delivery.max_amount)
                                   )
        elif order_method == 'Delivery' and delivery_customer_details_form.validate():
            order_array = eval(request.cookies.get('order'))

            customer_name = customer_details_form.customer_name.data
            customer_phone = customer_details_form.customer_phone.data
            session['customer_phone'] = customer_phone
            customer_email = customer_details_form.customer_email.data
            address_line1 = delivery_customer_details_form.address_line1.data
            address_line2 = delivery_customer_details_form.address_line2.data
            state = delivery_customer_details_form.state.data
            zipcode = delivery_customer_details_form.zipcode.data
            notes = delivery_customer_details_form.notes.data

            try:
                is_number_valid(customer_phone)

                customer = Customers(customer_name=customer_name,
                                     customer_phone=customer_phone,
                                     customer_email=customer_email,
                                     customer_verified=verified)
                db_session.add(customer)
                db_session.commit()
                session['customer_id'] = customer.customer_id

                order = Orders(customer_id=customer.customer_id,
                               order_method=order_method.lower(),
                               datetime_made=datetime.datetime.now(),
                               address_line1=address_line1,
                               address_line2=address_line2,
                               state=state,
                               zipcode=zipcode,
                               status='pending',
                               notes=notes)

                db_session.add(order)
                db_session.commit()

                for item in order_array:
                    item = OrderItems(order_id=order.order_id,
                                      item_name=item['item_name'],
                                      item_quantity=item['item_qty'],
                                      item_size=item['item_size'],
                                      item_price=item['item_price'])
                    db_session.add(item)
                    db_session.commit()

            except exc.SQLAlchemyError as e:
                print('exc.SQLAlchemyError: ', e)
                flash('there was an error submitting your order, please try again later', 'danger')
            except TwilioException as e:
                print('TwilioException: ', e)
                flash('there was an error submitting your order, please include country key with your phone number and try again',
                      'danger')
            except:
                print('an error occurred :)')
            else:
                print('return success')
                return redirect(url_for('.phone_validation'))
            print('return failure')
            db_session.rollback()
            return render_template('few_steps.html',
                                   customer_details_form=customer_details_form,
                                   delivery_customer_details_form=delivery_customer_details_form,
                                   allow_delivery=query(model_column=Delivery.allow_delivery),
                                   delivery_taxes=query(model_column=Delivery.delivery_tax),
                                   delivery_charges=query(model_column=Delivery.delivery_charges),
                                   min_amount=query(model_column=Delivery.min_amount),
                                   max_amount=query(model_column=Delivery.max_amount)
                                   )
        return render_template('few_steps.html',
                               customer_details_form=customer_details_form,
                               delivery_customer_details_form=delivery_customer_details_form,
                               allow_delivery=query(model_column=Delivery.allow_delivery),
                               delivery_taxes=query(model_column=Delivery.delivery_tax),
                               delivery_charges=query(model_column=Delivery.delivery_charges),
                               min_amount=query(model_column=Delivery.min_amount),
                               max_amount=query(model_column=Delivery.max_amount)
                               )
    return redirect(url_for('.menu',
                            allow_delivery=query(model_column=Delivery.allow_delivery),
                            delivery_taxes=query(model_column=Delivery.delivery_tax),
                            delivery_charges=query(model_column=Delivery.delivery_charges),
                            min_amount=query(model_column=Delivery.min_amount),
                            max_amount=query(model_column=Delivery.max_amount)))


@Cmod.route("/phone_validation", methods=['GET', 'POST'])
def phone_validation():
    print('inside phone validation function')
    print('request.method: ', request.method, 'session.get("customer_phone"): ',
          session.get('customer_phone'), 'customer id: ,', session.get('customer_id'))
    if request.method == 'POST' and session.get('customer_phone'):
        if request.form['verification_code'] == session.get('verification_code'):
            session['verified'] = True
            return redirect(url_for('.order_received'))
        elif session.get('verification_code') is None:
            send_confirmation_code(session['customer_phone'])
            return render_template('phone_validation.html', customer_phone=session['customer_phone'])
        else:
            flash('Wrong code. Please try again.', 'danger')
            return render_template('phone_validation.html', customer_phone=session['customer_phone'])
    elif request.method == 'GET' and session.get('customer_phone'):
        send_confirmation_code(session['customer_phone'])
        return render_template('phone_validation.html', customer_phone=session['customer_phone'])
    elif session.get('customer_phone') is None:
        return redirect(url_for('.menu',
                                allow_delivery=query(model_column=Delivery.allow_delivery),
                                delivery_taxes=query(model_column=Delivery.delivery_tax),
                                delivery_charges=query(model_column=Delivery.delivery_charges),
                                min_amount=query(model_column=Delivery.min_amount),
                                max_amount=query(model_column=Delivery.max_amount)))


@Cmod.route("/order_received", methods=['GET'])
def order_received():
    if session.get('verified'):
        customer_info = db_session.query(Customers).filter(Customers.customer_id == session['customer_id']).one()
        customer_order_info = db_session.query(Orders).filter(Orders.customer_id == session['customer_id']).one()
        customer_order_items = db_session.query(OrderItems).filter(OrderItems.order_id == customer_order_info.order_id).all()
        delivery_taxes = query(model_column=Delivery.delivery_tax)
        delivery_charges = query(model_column=Delivery.delivery_charges)
        total = 0
        for item in customer_order_items:
            total += (float(item.item_price) * item.item_quantity)
        if customer_order_info.order_method == 'delivery':
            a = float(total) + delivery_charges
            b = a * (float(delivery_taxes) / 100)
            total = a + b
        return render_template('order_received.html',
                               customer_info=customer_info,
                               customer_order_info=customer_order_info,
                               customer_order_items=customer_order_items,
                               total=total,
                               delivery_taxes=delivery_taxes,
                               delivery_charges=delivery_charges
                               )
    else:
        return redirect(url_for('/'))
