from flask import Blueprint
from sqlalchemy import exc
from app import db_session
from app.models import Orders


Smod = Blueprint('staff', __name__,
                 template_folder='templates',
                 static_folder='static',
                 static_url_path='../static')


@Smod.route("/all_orders", methods=['GET'])
def index():
    return "all orders shall show here"


@Smod.route("/pending_orders", methods=['GET'])
def menu():
    return "pending orders shall show here"


@Smod.route("/in_progress_orders", methods=["GET"])
def few_steps():
    return "in progress orders shall show here"


@Smod.route("/finished_orders", methods=["GET"])
def phone_validation():
    return "finished orders shall show here"


@Smod.route("/missed_orders", methods=["GET"])
def order_received():
    return "missed orders shall show here"
