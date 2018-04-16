# import random 
# from twilio.rest import Client
# from flask import session


# # sends confirmation code to customer phone
# def send_confirmation_code(to_number):
#     verification_code = generate_code()
#     send_sms(to_number, verification_code)
#     session['verification_code'] = verification_code
#     return verification_code


# # for generating verification code
# def generate_code():
#     return str(random.randrange(100000, 999999))


# # for sending SMS
# def send_sms(to_number, body):
#     account_sid = app.config['TWILIO_ACCOUNT_SID']
#     auth_token = app.config['TWILIO_AUTH_TOKEN']
#     twilio_number = app.config['TWILIO_NUMBER']
#     client = Client(account_sid, auth_token)
#     client.api.messages.create(to_number,
#                            from_=twilio_number,
#                            body=body)


# #############################

# from flask import Flask , render_template, request
# from flask_wtf import FlaskForm
# from wtforms.fields.html5 import TelField
# from flask_wtf.csrf import CSRFProtect


# app = Flask(__name__)
# app.config.update(dict(
#     SECRET_KEY="powerful secretkey",
#     WTF_CSRF_SECRET_KEY="a csrf secret key"
# ))

# class UserForm(FlaskForm):
#     phone_number = TelField('sdafsdfasdf')

# @app.route('/test', methods=["POST", "GET"])
# def test():
# 	form = UserForm()
# 	print(form.errors, form.validate_on_submit())
# 	if form.validate_on_submit() and request.method == "POST":
# 		return "Horayyy!"
# 	return render_template("test.html",
# 		form=form)

# if __name__ == "__main__":
# 	app.run(debug=True)
#
# from app.models import Employee
# from app import db_session
# new_employee = Employee(employee_username='hhh',
#                         employee_email='hhh@domain.com',
#                         employee_status='active')
# print(type('hhh'))
# new_employee._set_password = 'hhh'
# db_session.add(new_employee)
# db_session.commit()
