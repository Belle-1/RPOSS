from flask import Blueprint, render_template, jsonify
from sqlalchemy import exc, and_, or_
from app import db_session
from app.models import Orders, Customers, OrdersTiming, OrderItems, Delivery
from app.utilities import query


Smod = Blueprint('staff', __name__,
                 template_folder='templates',
                 static_folder='static',
                 static_url_path='../static')


@Smod.route("/all_orders", methods=['GET'])
def all_orders():
    return render_template('all_orders.html')


@Smod.route("/pending_orders", methods=['GET'])
def pending_orders():
    return render_template('pending_orders.html')


@Smod.route("/in_progress_orders", methods=["GET"])
def in_progress_orders():
    return render_template('in_progress_orders.html')


@Smod.route("/finished_orders", methods=["GET"])
def finished_orders():
    return render_template('finished_orders.html')


@Smod.route("/missed_orders", methods=["GET"])
def missed_orders():
    return render_template('missed_orders.html')


@Smod.route('/get_orders/<page>', methods=['GET'])
def get_orders(page):
    return jsonify(fetch_orders(page))


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
                                        'pending_remaining_time': query(model_column=OrdersTiming.pending_time),
                                        'date_made':  order.datetime_made.strftime('%b %d, %Y') if order.datetime_made else '',
                                        'time_made': order.datetime_made.strftime('%H:%M %p') if order.datetime_made else '',
                                        'order_method': order.order_method,
                                        'address_line1': order.address_line1,
                                        'address_line2': order.address_line2,
                                        'state': order.state,
                                        'zipcode': order.zipcode,
                                        'notes': order.notes,
                                        'delivery_charges': query(model_column=Delivery.delivery_charges),
                                        'delivery_taxes': query(model_column=Delivery.delivery_tax),
                                        'items': [item.serialize for item in db_session.query(OrderItems).filter(OrderItems.order_id == order.order_id).all()],
                                        'total': sum(float(item.item_price) * item.item_quantity for item in db_session.query(OrderItems).filter(OrderItems.order_id == order.order_id).all())}

    elif page == 'in_progress_orders':
        for customer in customers:
            order = db_session.query(Orders).filter(and_(Orders.customer_id == customer.customer_id),
                                                    (Orders.status == 'in_progress')).first()
            if order:
                data[order.order_id] = {'order_id': order.order_id,
                                        'pending_remaining_time': query(model_column=OrdersTiming.pending_time),
                                        'date_made':  order.datetime_made.strftime('%b %d, %Y') if order.datetime_made else '',
                                        'time_made': order.datetime_made.strftime('%H:%M %p') if order.datetime_made else '',
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
            order = db_session.query(Orders).filter(and_(Orders.customer_id == customer.customer_id,
                                                    or_(Orders.status == 'missed'),
                                                    (Orders.status == 'rejected'))).first()
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

print(fetch_orders('in_progress_orders'))














