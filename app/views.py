from flask import Blueprint, request, render_template, session, redirect, url_for
from app.forms import LogInForm, RestaurantBaseForm, RestaurantSocialMediaForm, RestaurantOpeningHoursForm
from app.models import Employee
from app import db_session


Rmod = Blueprint('RPOSS', __name__,
                 template_folder='templates',
                 static_folder='static')


@Rmod.route('/login', methods=['GET', 'POST'])
def login():
    form = LogInForm()
    if request.method == 'POST' and form.validate():
        user_name = form.user_name.data
        password = form.password.data

        # user name exist in db and its password is valid
        user = db_session.query(Employee).filter_by(employee_username=user_name).first()
        if user is not None and user.is_correct_password(password):
            # user is owner -> transmit to owner panel
            if user.employee_id == 1:
                session['owner_logged_in'] = True
                session['owner_username'] = user.employee_username
                return render_template('owner_restaurant.html',
                                       base_form=RestaurantBaseForm(),
                                       opening_form=RestaurantOpeningHoursForm(),
                                       media_form=RestaurantSocialMediaForm(),
                                       owner_username=session['owner_username'])
            # user is employee -> transmit to progressive panel
            else:
                session['employee_logged_in'] = True
                session['employee_username'] = user.employee_username
                return redirect(url_for('staff.all_orders'))
    return render_template('log_in.html',
                           form=form)

# log out function
