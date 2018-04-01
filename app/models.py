from app import bcrypt
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Enum, DateTime, CHAR, Boolean, Time
from sqlalchemy.orm import relationship
from app import db_session


Base = declarative_base()


class Employee(Base):
    __tablename__ = 'employee'

    employee_id = Column(Integer, primary_key=True, autoincrement=True)
    employee_username = Column(String(64), unique=True)
    employee_email = Column(String(150), unique=True)
    _password = Column(String(128))
    employee_status = Column(Enum('active', 'inactive'))

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def _set_password(self, plaintext):
        self._password = bcrypt.generate_password_hash(plaintext)

    def is_correct_password(self, candidatepassword):
        return bcrypt.check_password_hash(self._password, candidatepassword)

    @property
    def serialize(self):
        """returns object data in easily serializable format"""
        return {
            'employee_id': self.employee_id,
            'employee_username': self.employee_username,
            'employee_email': self.employee_email,
            'employee_status': self.employee_status,
        }


class RestaurantBaseInformation(Base):
    __tablename__ = 'restaurant_base_information'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    restaurant_name = Column(String(150))
    restaurant_about = Column(String(240))
    restaurant_img = Column(String(240))
    restaurant_address_line = Column(String(150))
    restaurant_city = Column(String(64))
    restaurant_country = Column(String(64))
    restaurant_zipcode = Column(Integer())
    restaurant_email = Column(String(150))
    restaurant_phone_number = Column(Integer())
    restaurant_logo = Column(String(240))

    @property
    def serialize(self):
        """returns object data in easily serializable format"""
        return {
            'restaurant_name': self.restaurant_name,
            'restaurant_about': self.restaurant_about,
            'restaurant_img': self.restaurant_img,
            'restaurant_address_line': self.restaurant_address_line,
            'restaurant_city': self.restaurant_city,
            'restaurant_country': self.restaurant_country,
            'restaurant_zipcode': self.restaurant_zipcode,
            'restaurant_email': self.restaurant_email,
            'restaurant_phone_number': self.restaurant_phone_number,
            'restaurant_logo': self.restaurant_logo,
        }


class OpeningHours(Base):
    __tablename__ = 'opening_hours'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    from_date = Column(Time())
    to_date = Column(Time())
    saturday = Column(Boolean())
    sunday = Column(Boolean())
    monday = Column(Boolean())
    tuesday = Column(Boolean())
    wednesday = Column(Boolean())
    thursday = Column(Boolean())
    friday = Column(Boolean())

    @property
    def serialize(self):
        """returns object data in easily serializable format"""
        return {
            'from_date': self.from_date,
            'to_date': self.to_date,
            'saturday': self.saturday,
            'sunday': self.sunday,
            'monday': self.monday,
            'tuesday': self.tuesday,
            'wednesday': self.wednesday,
            'thursday': self.thursday,
            'friday': self.friday,
        }


class SocialMedia(Base):
    __tablename__ = 'social_media'

    site_id = Column(Integer(), primary_key=True, autoincrement=True)
    site_name = Column(String(24))
    site_link = Column(String(240))

    @property
    def serialize(self):
        """returns object data in easily serializable format"""
        return {
            'site_name': self.site_name,
            'site_link': self.site_link,
        }


class PickUp(Base):
    __tablename__ = 'pick_up'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    allow_pickup = Column(Boolean())
    pickup_tax = Column(Integer())

    @property
    def serialize(self):
        """returns object data in easily serializable format"""
        return {
            'allow_pickup': self.allow_pickup,
            'pickup_tax': self.pickup_tax,
        }


class Delivery(Base):
    __tablename__ = 'delivery'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    allow_delivery = Column(Boolean())
    delivery_tax = Column(Integer())
    delivery_charges = Column(Float())
    min_amount = Column(Float())
    max_amount = Column(Float())

    @property
    def serialize(self):
        """returns object data in easily serializable format"""
        return {
            'allow_delivery': self.allow_delivery,
            'deliver_tax': self.deliver_tax,
            'delivery_charges': self.delivery_charges,
            'min_amount': self.min_amount,
            'max_amount': self.max_amount,
        }


class MenuSetUp(Base):
    __tablename__ = 'menu_set_up'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    restaurant_image = Column(String(240))
    restaurant_description = Column(String(240))

    @property
    def serialize(self):
        """returns object data in easily serializable format"""
        return {
            'restaurant_image': self.restaurant_image,
            'restaurant_description': self.restaurant_description,
        }


class MenuItems(Base):
    __tablename__ = 'menu_items'

    item_id = Column(Integer(), primary_key=True, autoincrement=True)
    item_name = Column(String(60), unique=True)
    item_category = Column(String(60))
    item_status = Column(Enum('active', 'inactive'))
    item_price = Column(Float())
    item_size = Column(Enum('s', 'm', 'l'))
    item_image = Column(String(240))

    @property
    def serialize(self):
        """returns object data in easily serializable format"""
        return {
            'item_id': self.item_id,
            'item_name': self.item_name,
            'item_category': self.item_category,
            'item_status': self.item_status,
            'item_price': self.item_price,
            'item_size': self.item_size,
            'item_image': self.item_image,
        }


class OrdersTiming(Base):
    __tablename__ = 'orders_timing'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    delivery_time = Column(Integer())
    preparing_time = Column(Integer())
    pending_time = Column(Integer())

    @property
    def serialize(self):
        """returns object data in easily serializable format"""
        return {
            'delivery_time': self.delivery_time,
            'preparing_time': self.preparing_time,
            'pending_time': self.pending_time,
        }


class Customers(Base):
    __tablename__ = 'customers'

    customer_id = Column(Integer(), primary_key=True, autoincrement=True)
    customer_name = Column(String(64))
    customer_phone = Column(Integer())
    customer_email = Column(String(150))
    customer_verified = Column(Boolean())
    order = relationship('Orders')

    @property
    def serialize(self):
        """returns object data in easily serializable format"""
        return {
            'customer_id': self.customer_id,
            'customer_name': self.customer_name,
            'customer_phone': self.customer_phone,
            'customer_email': self.customer_email,
            'customer_verified': self.customer_verified,
            'customer_order': self.customer_order,
        }


class Orders(Base):
    __tablename__ = 'orders'

    order_id = Column(Integer(), primary_key=True, autoincrement=True)
    customer_id = Column(Integer(), ForeignKey('customers.customer_id'))
    items = relationship('OrderItems')
    order_method = Column(Enum('pick_up', 'delivery'))
    datetime_made = Column(DateTime())
    address_line = Column(String(150))
    state = Column(String(64))
    zipcode = Column(Integer())
    notes = Column(String(150))
    status = Column(Enum('pending', 'in_progress', 'missed', 'rejected', 'finished'))
    by = Column(String(64))

    @property
    def serialize(self):
        """returns object data in easily serializable format"""
        return {
            'order_id': self.order_id,
            'customer_id': self.customer_id,
            'items': self.items,
            'order_method': self.order_method,
            'datetime_made': self.datetime_made,
            'address_line': self.address_line,
            'state': self.state,
            'zipcode': self.zipcode,
            'notes': self.notes,
            'status': self.status,
            'by': self.by,
        }


class OrderItems(Base):
    __tablename__ = 'order_items'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    order_id = Column(Integer(), ForeignKey('orders.order_id'))
    item_name = Column(String(64))
    item_category = Column(String(64))
    item_quantity = Column(Integer())
    item_size = Column(Enum('s', 'm', 'l'))
    item_price = Column(Integer())

    @property
    def serialize(self):
        """returns object data in easily serializable format"""
        return {
            'id': self.id,
            'order_id': self.order_id,
            'item_name ': self.item_name ,
            'item_category': self.item_category,
            'item_quantity': self.item_quantity,
            'item_size ': self.item_size ,
            'item_price': self.item_price,
        }


from app import engine
Base.metadata.create_all(engine)











