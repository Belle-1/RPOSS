from flask import Blueprint, render_template, jsonify, session, redirect, url_for
from sqlalchemy import exc, and_, or_
from app import db_session
from app.models import Orders, Customers, OrdersTiming, OrderItems, Delivery, RestaurantBaseInformation
from app.utilities import pending_time, preparing_time, delivery_time, delivery_charges, delivery_tax
import datetime
from instance.config import confirm_customer


Smod = Blueprint('staff', __name__,
                 template_folder='templates',
                 static_folder='static',
                 static_url_path='../static')


@Smod.route("/all_orders", methods=['GET'])
def all_orders():
    if session.get('employee_logged_in'):
        return render_template('all_orders.html')
    return redirect(url_for('RPOSS.login'))


@Smod.route("/pending_orders", methods=['GET'])
def pending_orders():
    if session.get('employee_logged_in'):
        return render_template('pending_orders.html')
    return redirect(url_for('RPOSS.login'))


@Smod.route("/in_progress_orders", methods=["GET"])
def in_progress_orders():
    if session.get('employee_logged_in'):
        return render_template('in_progress_orders.html')
    return redirect(url_for('RPOSS.login'))


@Smod.route("/finished_orders", methods=["GET"])
def finished_orders():
    if session.get('employee_logged_in'):
        return render_template('finished_orders.html')
    return redirect(url_for('RPOSS.login'))


@Smod.route("/missed_orders", methods=["GET"])
def missed_orders():
    if session.get('employee_logged_in'):
        return render_template('missed_orders.html')
    return redirect(url_for('RPOSS.login'))


@Smod.route('/get_orders/<page>', methods=['GET'])
def get_orders(page):
    return jsonify(fetch_orders(page))


@Smod.route('/modify_order/<order_id>/<status>', methods=['PUT'])
def modify_menu_item(order_id, status):
    on_success = jsonify({'success': True}), 200, {'ContentType': 'application/json'}

    # the commented code below is used for sending confirmation and rejection/missed emails to the customers,
    # I commented them because they were taking a whole lot of time to perform, according to that the database was
    # missing/rejecting/confirming order on its own
    # customer = db_session.query(Customers).filter(Customers.customer_id == Orders.customer_id).first()
    # restaurant_name = query(model_column=RestaurantBaseInformation.restaurant_name)
    # preparing_time = query(model_column=OrdersTiming.preparing_time)
    if status == 'missed':
        db_session.query(Orders).filter(Orders.order_id == int(order_id)).update({"status": status, "datetime_confirmed": datetime.datetime.now()})
        db_session.commit()
        # confirm_customer(customer.customer_name, customer.customer_email, order_id, restaurant_name, 'missed',preparing_time)
        return on_success
    elif status == 'in_progress':
        db_session.query(Orders).filter(Orders.order_id == int(order_id)).update({"status": status, "datetime_confirmed": datetime.datetime.now()})
        db_session.commit()
        # confirm_customer(customer.customer_name, customer.customer_email, order_id, restaurant_name, 'confirmed',preparing_time)
        return on_success
    elif status == 'rejected':
        db_session.query(Orders).filter(Orders.order_id == int(order_id)).update({"status": status, "datetime_confirmed": datetime.datetime.now()})
        db_session.commit()
        # confirm_customer(customer.customer_name, customer.customer_email, order_id, restaurant_name, 'rejected',preparing_time)
        return on_success
    elif status == 'finished':
        db_session.query(Orders).filter(Orders.order_id == int(order_id)).update({"status": status, "datetime_confirmed": datetime.datetime.now()})
        db_session.commit()
        # confirm_customer(customer.customer_name, customer.customer_email, order_id, restaurant_name, 'finished',preparing_time)
        return on_success


def fetch_orders(page):
    customers = db_session.query(Customers).all()
    orders = db_session.query(Orders).all()
    data = {}

    if page == 'all_orders':
        for customer in customers:
            order = db_session.query(Orders).filter(Orders.customer_id == customer.customer_id).first()
            if order:
                data[order.order_id] = {'customer_name': customer.customer_name,
                                        'customer_phone': customer.customer_phone,
                                        'order_id': order.order_id,
                                        'by': order.by,
                                        'status': order.status,
                                        'date_made':  order.datetime_made.strftime('%b %d, %Y') if order.datetime_made else '',
                                        'time_made': order.datetime_made.strftime('%H:%M %p') if order.datetime_made else '',
                                        'order_method': order.order_method,
                                        'date_confirmed': order.datetime_confirmed.strftime('%b %d, %Y') if order.datetime_confirmed else '',
                                        'time_confirmed': order.datetime_confirmed.strftime('%H:%M %p') if order.datetime_confirmed else '',
                                        }
    elif page == 'pending_orders':
        for customer in customers:
            order = db_session.query(Orders).filter(and_(Orders.customer_id == customer.customer_id,
                                                    Orders.status == 'pending')).first()
            if order:
                data[order.order_id] = {'customer_name': customer.customer_name,
                                        'customer_phone': customer.customer_phone,
                                        'customer_email': customer.customer_email,
                                        'order_id': order.order_id,
                                        'status': 'pending',
                                        'pending_remaining_time': pending_time,
                                        'date_made':  order.datetime_made.strftime('%b %d, %Y') if order.datetime_made else '',
                                        'time_made': order.datetime_made.strftime('%H:%M %p') if order.datetime_made else '',
                                        'order_method': order.order_method,
                                        'address_line1': order.address_line1,
                                        'address_line2': order.address_line2,
                                        'state': order.state,
                                        'zipcode': order.zipcode,
                                        'notes': order.notes,
                                        'delivery_charges': delivery_charges,
                                        'delivery_taxes': delivery_tax,
                                        'items': [item.serialize for item in db_session.query(OrderItems).filter(OrderItems.order_id == order.order_id).all()],
                                        'total': sum(float(item.item_price) * item.item_quantity for item in db_session.query(OrderItems).filter(OrderItems.order_id == order.order_id).all())}

    elif page == 'in_progress_orders':
        for customer in customers:
            order = db_session.query(Orders).filter(and_(Orders.customer_id == customer.customer_id),
                                                    (Orders.status == 'in_progress')).first()
            if order:
                data[order.order_id] = {'order_id': order.order_id,
                                        'order_method': order.order_method,
                                        'preparing_remaining_time': preparing_time,
                                        'delivery_remaining_time': delivery_time,
                                        'date_made':  order.datetime_confirmed.strftime('%b %d, %Y') if order.datetime_confirmed else '',
                                        'time_made': order.datetime_confirmed.strftime('%H:%M %p') if order.datetime_confirmed else '',
                                        'notes': order.notes,
                                        'items': [item.serialize for item in db_session.query(OrderItems).filter(OrderItems.order_id == order.order_id).all()]}

    elif page == 'finished_orders':
        for customer in customers:
            order = db_session.query(Orders).filter(and_(Orders.customer_id == customer.customer_id,
                                                    Orders.status == 'finished')).first()
            if order:
                data[order.order_id] = {'customer_name': customer.customer_name,
                                        'customer_phone': customer.customer_phone,
                                        'order_id': order.order_id,
                                        'by': order.by,
                                        'status': 'delivered',
                                        'date_made':  order.datetime_made.strftime('%b %d, %Y') if order.datetime_made else '',
                                        'time_made': order.datetime_made.strftime('%H:%M %p') if order.datetime_made else '',
                                        'order_method': order.order_method,
                                        'date_confirmed': order.datetime_confirmed.strftime('%b %d, %Y') if order.datetime_confirmed else '',
                                        'time_confirmed': order.datetime_confirmed.strftime('%H:%M %p') if order.datetime_confirmed else ''}
    elif page == 'missed_orders':
        for customer in customers:
            order = db_session.query(Orders).filter(and_(Orders.customer_id == customer.customer_id, or_(Orders.status == 'missed', Orders.status == 'rejected'))).first()
            if order:
                data[order.order_id] = {'customer_name': customer.customer_name,
                                        'customer_phone': customer.customer_phone,
                                        'order_id': order.order_id,
                                        'by': order.by,
                                        'status': order.status,
                                        'date_made':  order.datetime_made.strftime('%b %d, %Y') if order.datetime_made else '',
                                        'time_made': order.datetime_made.strftime('%H:%M %p') if order.datetime_made else '',
                                        'order_method': order.order_method,
                                        'date_confirmed': order.datetime_confirmed.strftime('%b %d, %Y') if order.datetime_confirmed else '',
                                        'time_confirmed': order.datetime_confirmed.strftime('%H:%M %p') if order.datetime_confirmed else ''}
    import operator
    return sorted(data.items(), key=operator.itemgetter(0), reverse=True)














