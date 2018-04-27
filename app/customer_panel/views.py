from flask import Blueprint, request, render_template, jsonify, redirect, url_for, flash, session
from ..forms import ContactUsForm, CustomerDetailsForm, DeliveryCustomerDetailsForm
from instance.config import send_mail
from app import db_session
from app.models import MenuItems, Delivery, OpeningHours, Orders, OrderItems, Customers, OrdersTiming, SocialMedia,\
    RestaurantBaseInformation, MenuSetUp, PickUp
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
        try:
            is_number_valid(customer_phone)
            send_mail(customer_name, customer_message, customer_email, customer_phone)
            flash('Message sent successfully.', 'success')
        except:
            flash('There was an error sending your message. Please, try again later.', 'danger')
    days = {
        'saturday':  query(model_column=OpeningHours.saturday),
        'sunday':  query(model_column=OpeningHours.sunday),
        'monday':  query(model_column=OpeningHours.monday),
        'tuesday':  query(model_column=OpeningHours.tuesday),
        'wednesday':  query(model_column=OpeningHours.wednesday),
        'thursday':  query(model_column=OpeningHours.thursday),
        'friday':  query(model_column=OpeningHours.friday),
    }
    working_days = [day for day, value in days.items() if value]

    return render_template('index.html',
                           contact_us_form=contact_us_form,
                           social_media=db_session.query(SocialMedia).all(),
                           restaurant_name=query(model_column=RestaurantBaseInformation.restaurant_name),
                           restaurant_img=query(model_column=RestaurantBaseInformation.restaurant_img),
                           restaurant_about=query(model_column=RestaurantBaseInformation.restaurant_about),
                           restaurant_menu_description=query(model_column=MenuSetUp.restaurant_description),
                           restaurant_logo=query(model_column=RestaurantBaseInformation.restaurant_logo),
                           restaurant_address_line=query(model_column=RestaurantBaseInformation.restaurant_address_line),
                           restaurant_city=query(model_column=RestaurantBaseInformation.restaurant_city),
                           menu_image=query(model_column=MenuSetUp.restaurant_image),
                           restaurant_country=query(model_column=RestaurantBaseInformation.restaurant_country),
                           restaurant_zipcode=query(model_column=RestaurantBaseInformation.restaurant_zipcode),
                           restaurant_email=query(model_column=RestaurantBaseInformation.restaurant_email),
                           restaurant_phone_number=query(model_column=RestaurantBaseInformation.restaurant_phone_number),
                           working_days=', '.join(working_days).title(),
                           from_date=query(model_column=OpeningHours.from_date).strftime('%H:%M %p'),
                           to_date=query(model_column=OpeningHours.to_date).strftime('%H:%M %p'),
                           )


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
    from_date = query(model_column=OpeningHours.from_date)
    to_date = query(model_column=OpeningHours.to_date)
    days = {
        'saturday':  query(model_column=OpeningHours.saturday),
        'sunday':  query(model_column=OpeningHours.sunday),
        'monday':  query(model_column=OpeningHours.monday),
        'tuesday':  query(model_column=OpeningHours.tuesday),
        'wednesday':  query(model_column=OpeningHours.wednesday),
        'thursday':  query(model_column=OpeningHours.thursday),
        'friday':  query(model_column=OpeningHours.friday),
    }
    working_days = [day for day, value in days.items() if value]

    # checks if the customer's POST request is within restaurant's opening days/hours
    within_working_day = ((from_date < datetime.datetime.now().time() < to_date) and datetime.datetime.now().strftime('%A').lower() in working_days)
    if request.method == 'POST' and within_working_day:
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
                flash('there was an error submitting your order, please try again later', 'danger')
            except TwilioException as e:
                flash('there was an error submitting your order, please include country key with your phone number and try again', 'danger')
            except:
                print('an error occurred :)')
            else:
                return redirect(url_for('.phone_validation'))
            db_session.rollback()
            return render_template('few_steps.html',
                                   customer_details_form=customer_details_form,
                                   delivery_customer_details_form=delivery_customer_details_form,
                                   allow_delivery=query(model_column=Delivery.allow_delivery),
                                   allow_pickup=query(model_column=PickUp.allow_pickup),
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
                flash('there was an error submitting your order, please try again later', 'danger')
            except TwilioException as e:
                flash('there was an error submitting your order, please include country key with your phone number and try again',
                      'danger')
            except:
                print('an error occurred :)')
            else:
                return redirect(url_for('.phone_validation'))
            db_session.rollback()
            return render_template('few_steps.html',
                                   customer_details_form=customer_details_form,
                                   delivery_customer_details_form=delivery_customer_details_form,
                                   allow_delivery=query(model_column=Delivery.allow_delivery),
                                   allow_pickup=query(model_column=PickUp.allow_pickup),
                                   delivery_taxes=query(model_column=Delivery.delivery_tax),
                                   delivery_charges=query(model_column=Delivery.delivery_charges),
                                   min_amount=query(model_column=Delivery.min_amount),
                                   max_amount=query(model_column=Delivery.max_amount)
                                   )
        return render_template('few_steps.html',
                               customer_details_form=customer_details_form,
                               delivery_customer_details_form=delivery_customer_details_form,
                               allow_delivery=query(model_column=Delivery.allow_delivery),
                               allow_pickup=query(model_column=PickUp.allow_pickup),
                               delivery_taxes=query(model_column=Delivery.delivery_tax),
                               delivery_charges=query(model_column=Delivery.delivery_charges),
                               min_amount=query(model_column=Delivery.min_amount),
                               max_amount=query(model_column=Delivery.max_amount)
                               )
    elif request.method == 'POST' and within_working_day is False:
        flash('You can place orders within working hours/days: {}, From {} To {}.'.format(', '.join(working_days).title(),
                                                                                          from_date.strftime('%H:%M %p'),
                                                                                          to_date.strftime('%H:%M %p')),
              'warning')

        return render_template('few_steps.html',
                               customer_details_form=customer_details_form,
                               delivery_customer_details_form=delivery_customer_details_form,
                               allow_pickup=query(model_column=PickUp.allow_pickup),
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
    if request.method == 'POST' and session.get('customer_phone'):
        if request.form['verification_code'] == session.get('verification_code'):
            session['verified'] = True
            try:
                customer = db_session.query(Customers).filter(Customers.customer_id == session['customer_id']).one()
                customer.customer_verified = True
                db_session.commit()
                return redirect(url_for('.order_received'))
            except:
                flash('There was an error verifying your account. Please, try again later.', 'danger')
                return render_template('phone_validation.html')
        elif session.get('verification_code') is None:
            send_confirmation_code(session['customer_phone'])
            return render_template('phone_validation.html')
        else:
            flash('Wrong code. Please try again.', 'danger')
            return render_template('phone_validation.html')

    elif request.method == 'GET' and session.get('customer_phone'):
        send_confirmation_code(session['customer_phone'])
        return render_template('phone_validation.html')

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

        session.pop('customer_id', None)
        session.pop('customer_phone', None)
        session.pop('verification_code', None)
        session.pop('verified', None)

        return render_template('order_received.html',
                               customer_info=customer_info,
                               customer_order_info=customer_order_info,
                               customer_order_items=customer_order_items,
                               total=total,
                               delivery_taxes=delivery_taxes,
                               delivery_charges=delivery_charges,
                               pending_time=query(model_column=OrdersTiming.pending_time),
                               delivery_time=datetime.timedelta(minutes=query(model_column=OrdersTiming.delivery_time)),
                               preparing_time=datetime.timedelta(minutes=query(model_column=OrdersTiming.preparing_time)),
                               )
    else:
        return redirect(url_for('.index'))
