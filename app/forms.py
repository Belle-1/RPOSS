from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, SelectMultipleField, IntegerField,\
    SelectField, BooleanField, PasswordField, SubmitField, RadioField, FloatField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms_components import TimeField, TimeRange
import datetime


# --- OWNER & STAFF LOGIN ---
class LogInForm(FlaskForm):
    user_name = StringField('user name', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])


# ---- OWNER PANEL ---
class RestaurantBaseForm(FlaskForm):
    restaurant_name = StringField('Restaurant Name',
                                  validators=[DataRequired("please provide your restaurant name.")])
    restaurant_about = TextAreaField('restaurant about',
                                     validators=[DataRequired()])
    restaurant_welcome_img = FileField('restaurant built-in welcome section image',
                                       validators=[DataRequired()])
    restaurant_address_line = StringField('restaurant address line',
                                          validators=[DataRequired('please provide restaurant street address')])
    restaurant_city = StringField('city',
                                  validators=[DataRequired()])
    restaurant_country = StringField('country',
                                     validators=[DataRequired()])
    restaurant_zipcode = StringField('ZIP code',
                                     validators=[DataRequired()])
    restaurant_email = StringField('restaurant e-mail address',
                                   validators=[DataRequired(), Email()])
    restaurant_phone = StringField('restaurant phone number',
                                   validators=[DataRequired()])
    restaurant_logo = FileField('restaurant logo',
                                validators=[DataRequired()])
    base_submit = SubmitField('commit changes')


class RestaurantOpeningHoursForm(FlaskForm):
    from_hour = TimeField('from',
                          validators=[DataRequired("please use the 'kk-kkk' format")],
                          default=datetime.time())
    to_hour = TimeField('to',
                        validators=[DataRequired("please use the 'kk-kkk' format")])
    opening_days = SelectMultipleField("select opening days",
                                       validators=[DataRequired()],
                                       choices=[('saturday', 'saturday'),
                                                ('sunday', 'sunday'),
                                                ('monday', 'monday'),
                                                ('tuesday', 'tuesday'),
                                                ('wednesday', 'wednesday'),
                                                ('thursday', 'thursday'),
                                                ('friday', 'friday')
                                                ])
    opening_submit = SubmitField('commit changes')


class RestaurantSocialMediaForm(FlaskForm):
    restaurant_facebook = StringField('facebook')
    restaurant_twitter = StringField('twitter')
    restaurant_instagram = StringField('instagram')
    restaurant_snapchat = StringField('snapchat')
    restaurant_yelp = StringField('yelp')
    media_submit = SubmitField('commit changes')


class MenuSetup(FlaskForm):
    restaurant_menu_image = FileField('restaurant built-in menu section image',
                                      validators=[DataRequired()])
    restaurant_menu_description = TextAreaField('restaurant menu description',
                                                validators=[DataRequired()])
    menu_setup_submit = SubmitField('commit changes')


class MenuItems(FlaskForm):
    item_name = StringField('item name',
                            validators=[DataRequired()])
    item_category = StringField('item category',
                                validators=[DataRequired()])
    item_status = SelectField('item status',
                              choices=[('active', 'active'), ('inactive', 'inactive')],
                              validators=[DataRequired()])
    item_price = FloatField('item price',
                            validators=[DataRequired()])
    item_size = SelectField('item size',
                            choices=[('l', 'l'), ('m', 'm'), ('s', 's')],
                            validators=[DataRequired()])
    item_image = FileField('item photo',
                           validators=[DataRequired()])
    menu_items_submit = SubmitField('add item')


class OrdersHampersMethods(FlaskForm):
    allow_pickup = BooleanField('allow pick-up orders', default=True)
    pickup_payment_methods = SelectField('payment methods', choices=[('COD', 'COD')])
    pickup_tax = IntegerField('tax')
    allow_delivery = BooleanField('allow delivery orders', default=True)
    delivery_payment_methods = SelectField('payment methods', choices=[('COD', 'COD')])
    delivery_tax = IntegerField('tax')
    delivery_charges = FloatField('Delivery charges')
    min_order_amount = FloatField('minimum order amount')
    max_order_amount = FloatField('maximum order amount')
    methods_submit = SubmitField('commit changes')


timing_options = list((str(v), str(l)) for v, l in enumerate(range(60)))


class OrdersHampersTiming(FlaskForm):
    delivery_time = SelectField('Delivery time (min)',
                                choices=timing_options)
    preparing_time = SelectField('Preparing time (min)',
                                 choices=timing_options)
    pending_time = SelectField('Pending time (min)',
                               choices=timing_options)
    timing_submit = SubmitField('commit changes')


class Employees(FlaskForm):
    employee_name = StringField('employee name', validators=[DataRequired()])
    employee_email = StringField('employee e-mail', validators=[DataRequired(), Email()])
    employee_password = PasswordField('employee password',
                                      validators=[DataRequired(),
                                                  EqualTo('confirm_password', 'passwords must match')])
    confirm_password = PasswordField('Confirm employee password')
    employee_submit = SubmitField('add employee')


# ---- RESTAURANT CUSTOMERS ---
class ContactUsForm(FlaskForm):
    customer_name = StringField('Name', validators=[DataRequired()])
    customer_phone = StringField('Phone number', validators=[DataRequired()])
    customer_email = StringField('E-mail', validators=[DataRequired(), Email()])
    customer_message = TextAreaField('Message', validators=[DataRequired()])
    submit_message = SubmitField('send')


class CustomerDetailsForm(FlaskForm):
    customer_name = StringField('Name',
                                validators=[DataRequired()])
    customer_phone = StringField('Phone number',
                                 validators=[DataRequired()])
    customer_email = StringField('E-mail',
                                 validators=[DataRequired(), Email()])


class DeliveryCustomerDetailsForm(FlaskForm):
    address_line1 = StringField('Address line1',
                                validators=[DataRequired()])
    address_line2 = StringField('Address line2')
    state = StringField('State/provinces/region',
                        validators=[DataRequired()])
    zipcode = StringField('ZIP/postal code',
                          validators=[DataRequired()])
    notes = TextAreaField('Special instruction')
    place_order = SubmitField('Place order')










