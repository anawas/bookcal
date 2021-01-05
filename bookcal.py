from flask import Flask
from flask import render_template, request, flash, redirect
from config import Config
from forms import LoginForm  # Temporary for testing form with Bootstrap
from booking import BookingForm, Booking
from mongodb import MongoDb
from datetime import datetime
import logging

flaskapp = Flask(__name__)
flaskapp.config.from_object(Config)
mongo = MongoDb(flaskapp.config['MONGO_DB'], flaskapp.config['DATABASE'], flaskapp.config['COLLECTION'])

# if __name__ != '__main__':
#     gunicorn_logger = logging.getLogger('gunicorn.error')
#     flaskapp.logger.handlers = gunicorn_logger.handlers
#     flaskapp.logger.setLevel(gunicorn_logger.level)

@flaskapp.route('/', methods=['GET', 'POST'])
def index():
    bookedDays = []
    for booking in mongo.get({'roomName': 'Elodie'}):
        bookedDays += [[booking['startDate'].strftime('%Y-%m-%d'),booking['endDate'].strftime('%Y-%m-%d')]]
        # print(booking['startDate'], booking['endDate'])
        # [['2021-01-10', '2021-01-20']]
    # print(bookedDays)
    form = BookingForm()
    print(form.startDate, form.endDate, form.name, form.mail, form.phone)
    if form.validate_on_submit():
        print('Form validated')
        flaskapp.logger.debug('this is a DEBUG message')
        flaskapp.logger.info('this is an INFO message')
        flaskapp.logger.warning('this is a WARNING message')
        flaskapp.logger.error('this is an ERROR message')
        flaskapp.logger.critical('this is a CRITICAL message')
        # flash('Got booking for user name={}, mail={}, startDate={}, endDate={}'.format(
        #     form.name.data, form.mail.data, form.startDate.data, form.endDate.data))
        # Register this booking in database
        print(datetime.strptime(form.startDate.data, '%Y-%m-%d'), datetime.strptime(form.endDate.data, '%Y-%m-%d'))
        mongo.add({
            'roomName': 'Elodie',
            'startDate': datetime.strptime(form.startDate.data, '%Y-%m-%d'), # datetime(form.startDate.data),
            'endDate': datetime.strptime(form.endDate.data, '%Y-%m-%d'), #form.endDate.data,
            'customerName': form.name.data,
            'customerMail': form.mail.data,
            'customerPhone': form.phone.data
        })
    else:
        for error in form.startDate.errors:
            print('startdate Error', error)
        for error in form.endDate.errors:
            print('enddate Error', error)
        for error in form.name.errors:
            print('name Error', error)
        for error in form.mail.errors:
            print('mail Error', error)
        for error in form.phone.errors:
            print('phone Error', error)

    return render_template('index.html', form=form, bookedDays=bookedDays)

@flaskapp.route('/bookinglist')
def bookinglist():
    bookingList = []
    for bookingRecord in mongo.get({'roomName': 'Elodie'}):
        booking = Booking(bookingRecord['startDate'], bookingRecord['endDate'], bookingRecord['roomName'], bookingRecord['customerName'], bookingRecord['customerMail'], bookingRecord['customerPhone'])
        bookingList += [booking]
    return render_template('bookinglist.html', bookingList=bookingList)

@flaskapp.route('/test', methods=['GET', 'POST'])
def test():
    form = BookingForm()
    if form.validate_on_submit():
        flash('Got booking for user name={}, mail={}'.format(
            form.name.data, form.mail))
    return render_template('test.html', form=form)    

@flaskapp.route('/test2', methods=['GET', 'POST'])
def test2():
    form = BookingForm()
    if form.validate_on_submit():
        flash('Got booking for user name={}, mail={}'.format(
            form.name.data, form.mail))
    return render_template('test2.html', form=form)    


@flaskapp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/')
    return render_template('login.html', title='Sign In', form=form)