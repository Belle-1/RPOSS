from app import db_session
from app.models import RestaurantBaseInformation, OpeningHours, SocialMedia, \
    MenuSetUp, PickUp, Delivery, OrdersTiming
import os


# class Options():

print(db_session.query(RestaurantBaseInformation).all())