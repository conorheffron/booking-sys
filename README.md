# booking-sys

## Technologies
python3, django admin/framework, django.test, & MySQL

## Build
```
cd booking-sys
pipenv shell
pipenv install 
```

## Apply form/model changes to DB
```
python manage.py makemigrations
python manage.py migrate
```

## Run All Tests
```
python3 manage.py test
```

## Run Django Application
```
python3 manage.py runserver
```

Frre to use icon image at: [lemon](https://www.flaticon.com/free-animated-icon/lemon_14385026?term=lemon&page=1&position=5&origin=tag&related_id=14385026)


## Functionality Demo

###  Make a Reservation Form
![reserve](./screenshots/reserve.png?raw=true "Make a Reservation")

###  Date Picker
![date-picker](./screenshots/date-picker.png?raw=true "Date Picker")

###  Booking Complete Confirmation / Alert
![booking-complete](./screenshots/booking-complete.png?raw=true "Booking Complete")

###  View Current Bookings for Date Change in Booking Form
![bookings-by-date](./screenshots/bookings-by-date.png?raw=true "View Bookings By Date Change")

###  Duplicate Booking Fail by Date & Time Value
![duplicate-booking-fail](./screenshots/duplicate-booking-fail.png?raw=true "Duplicate Booking Fail")

###  Dynamic JSON Table Update on Date Change (1st Sept --> 22nd August)
![dynamic-table-update](./screenshots/dynamic-table-update.png?raw=true "JSON Table Update")

###  View All Bookings Page
![all-bookings](./screenshots/all-bookings.png?raw=true "View All Resrvations")
