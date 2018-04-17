from app import db_session, app
from app.models import RestaurantBaseInformation, OpeningHours, SocialMedia, \
    MenuSetUp, PickUp, Delivery, OrdersTiming
import pyotp, random
from twilio.rest import Client
from flask import session


# Twilio setup
# sends confirmation code to customer phone
def send_confirmation_code(to_number):
    verification_code = generate_code()
    send_sms(to_number, verification_code)
    session['verification_code'] = verification_code
    return verification_code


# for generating verification code
def generate_code():
    return str(random.randrange(100000, 999999))


# for sending SMS
def send_sms(to_number, body):
    account_sid = app.config['TWILIO_ACCOUNT_SID']
    auth_token = app.config['TWILIO_AUTH_TOKEN']
    twilio_number = app.config['TWILIO_NUMBER']
    client = Client(account_sid, auth_token)
    client.api.messages.create("+" + to_number,
                               from_=twilio_number,
                               body=body)


# check phone number is valid number
def is_number_valid(phone_number):
    client = Client(app.config['TWILIO_ACCOUNT_SID'], app.config['TWILIO_AUTH_TOKEN'])
    return client.lookups.phone_numbers(phone_number).fetch()


def query(model_column,  model_filter=None, filter_by=None):
    """
    model_column: model.column column you want to query
    model_filter: model.filter coulumn you want to filter, defaults to None
    filter_by: value you want to filter by, defaults to None
    """
    if model_filter:
        return db_session.query(model_column).filter(model_filter == filter_by).one()[0]
    else:
        return db_session.query(model_column).one()[0]


restaurant_options = {
	'restaurant_name': query(model_column=RestaurantBaseInformation.restaurant_name),
	'restaurant_about': query(model_column=RestaurantBaseInformation.restaurant_about),
	'restaurant_img': query(model_column=RestaurantBaseInformation.restaurant_img),
	'restaurant_address_line': query(model_column=RestaurantBaseInformation.restaurant_address_line),
	'restaurant_city': query(model_column=RestaurantBaseInformation.restaurant_city),
	'restaurant_country': query(model_column=RestaurantBaseInformation.restaurant_country),
	'restaurant_zipcode': query(model_column=RestaurantBaseInformation.restaurant_zipcode),
	'restaurant_email': query(model_column=RestaurantBaseInformation.restaurant_email),
	'restaurant_phone_number': query(model_column=RestaurantBaseInformation.restaurant_phone_number),
	'restaurant_logo': query(model_column=RestaurantBaseInformation.restaurant_logo),
	}
opening_hours_options = {
	'from_date': query(model_column=OpeningHours.from_date),
	'to_date': query(model_column=OpeningHours.to_date),
	'saturday': query(model_column=OpeningHours.saturday),
	'sunday': query(model_column=OpeningHours.sunday),
	'monday': query(model_column=OpeningHours.monday),
	'tuesday': query(model_column=OpeningHours.tuesday),
	'wednesday': query(model_column=OpeningHours.wednesday),
	'thursday': query(model_column=OpeningHours.thursday),
	'friday': query(model_column=OpeningHours.friday),
	}
print(opening_hours_options['from_date'], opening_hours_options['to_date'], opening_hours_options['saturday'])
social_media_options = {
	'facebook': query(model_column=SocialMedia.site_link, model_filter=SocialMedia.site_name, filter_by='facebook'),
	'twitter': query(model_column=SocialMedia.site_link, model_filter=SocialMedia.site_name, filter_by='twitter'),
	'snapchat': query(model_column=SocialMedia.site_link, model_filter=SocialMedia.site_name, filter_by='snapchat'),
	'instagram': query(model_column=SocialMedia.site_link, model_filter=SocialMedia.site_name, filter_by='instagram'),
	'yelp': query(model_column=SocialMedia.site_link, model_filter=SocialMedia.site_name, filter_by='yelp'),	
	}
menu_setup_options = {
	'menu_image': query(model_column=MenuSetUp.restaurant_image),
	'menu_description': query(model_column=MenuSetUp.restaurant_description),
	}
pickup_options = {
	'pickup_allowed': query(model_column=PickUp.allow_pickup),
	'pickup_tax': query(model_column=PickUp.pickup_tax),
	}
# delivery_options = {
# 	'delivery_allowed': query(model_column=Delivery.allow_delivery),
# 	'delivery_tax': query(model_column=Delivery.delivery_tax),
# 	'delivery_charges': query(model_column=Delivery.delivery_charges),
# 	'min_amount': query(model_column=Delivery.min_amount),
# 	'max_amount': query(model_column=Delivery.max_amount),
# 	}
orders_timing_options = {
	'delviery_time': query(model_column=OrdersTiming.delivery_time),
	'preparing_time': query(model_column=OrdersTiming.preparing_time),
	'pending_time': query(model_column=OrdersTiming.pending_time),
	}







