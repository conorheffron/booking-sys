# booking-sys

[![Django CI](https://github.com/conorheffron/booking-sys/actions/workflows/django.yml/badge.svg)](https://github.com/conorheffron/booking-sys/actions/workflows/django.yml)

## Technologies
python3, django admin/framework, django.test, & MySQL

## Build
```
cd booking-sys
pipenv shell
pipenv install 
```

## Create DB Schema
```
mysql -u root -p 

CREATE DATABASE reservations;
```

## Apply form/model changes to DB
```
python manage.py makemigrations
python manage.py migrate
python manage.py showmigrations
```

## Run All Tests
```
python3 manage.py test
```

## Run Django Application
```
python3 manage.py runserver
```

## Alternatively, Debug Django Application
- Go to 'Run and Debug' View in VS code
- Select launch.json confirguration 'Python: Current File' & Run
- Set breakpoints in views.py
![debug](./screenshots/debug.png?raw=true "Debug GET Bookings Request")

Frre to use icon image at: [lemon](https://www.flaticon.com/free-animated-icon/lemon_14385026?term=lemon&page=1&position=5&origin=tag&related_id=14385026)


## Functionality Demo

###  App Home Address
```
http://localhost:8000/
http://localhost:8000/book/

or 

http://127.0.0.1:8000/
http://127.0.0.1:8000/book/
```

###  Make a Reservation Form
![reserve](./screenshots/reserve.png?raw=true "Make a Reservation")

###  Date Picker
![date-picker](./screenshots/date-picker.png?raw=true "Date Picker")

###  Booking Complete Confirmation / Alert
![booking-complete](./screenshots/booking-complete.png?raw=true "Booking Complete")

###  View Current Bookings for Date Change in Booking Form
![bookings-by-date](./screenshots/bookings-by-date.png?raw=true "View Bookings By Date Change")

###  Bookings By Date REST API End-point (used for view template above)
Using request path variable:
```
http://localhost:8000/bookings/2024-08-22/

and

http://localhost:8000/bookings/2024-09-01/
```
Or using request parameter 'date':
```
http://127.0.0.1:8000/bookings?date=2024-08-22

and

http://127.0.0.1:8000/bookings?date=2024-09-01
```


![postman](./screenshots/postman.png?raw=true "Postman GET Bookings Request")

###  Duplicate Booking Fail by Date & Time Value
![duplicate-booking-fail](./screenshots/duplicate-booking-fail.png?raw=true "Duplicate Booking Fail")

###  Dynamic JSON Table Update on Date Change (1st Sept --> 22nd August)
![dynamic-table-update](./screenshots/dynamic-table-update.png?raw=true "JSON Table Update")

###  View All Bookings Page
![all-bookings](./screenshots/all-bookings.png?raw=true "View All Resrvations")

```
http://localhost:8000/reservations/
```

### Terminal Logs
```
% pipenv shell              
Creating a virtualenv for this project...
Pipfile: /.../workspace/littlelemon/Pipfile
Using /usr/local/bin/python3 (3.12.4) to create virtualenv...
⠙ Creating virtual environment...created virtual environment CPython3.12.4.final.0-64 in 795ms
  creator CPython3macOsBrew(dest=/.../.local/share/virtualenvs/littlelemon-PIHfCB-G, clear=False, no_vcs_ignore=False, global=False)
  seeder FromAppData(download=False, pip=bundle, via=copy, app_data_dir=/.../Library/Application Support/virtualenv)
    added seed packages: pip==24.2
  activators BashActivator,CShellActivator,FishActivator,NushellActivator,PowerShellActivator,PythonActivator

✔ Successfully created virtual environment!
Virtualenv location: /.../.local/share/virtualenvs/littlelemon-PIHfCB-G
Launching subshell in virtual environment...
 . /.../.local/share/virtualenvs/littlelemon-.../bin/activate
zsh compinit: insecure directories, run compaudit for list.

% python manage.py makemigrations
No changes detected

% python manage.py migrate       
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, restaurant, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying restaurant.0001_initial... OK
  Applying restaurant.0002_reservation_delete_menu... OK
  Applying sessions.0001_initial... OK

% python manage.py showmigrations
admin
 [ ] 0001_initial
 [ ] 0002_logentry_remove_auto_add
 [ ] 0003_logentry_add_action_flag_choices
auth
 [ ] 0001_initial
 [ ] 0002_alter_permission_name_max_length
 [ ] 0003_alter_user_email_max_length
 [ ] 0004_alter_user_username_opts
 [ ] 0005_alter_user_last_login_null
 [ ] 0006_require_contenttypes_0002
 [ ] 0007_alter_validators_add_error_messages
 [ ] 0008_alter_user_username_max_length
 [ ] 0009_alter_user_last_name_max_length
 [ ] 0010_alter_group_name_max_length
 [ ] 0011_update_proxy_permissions
 [ ] 0012_alter_user_first_name_max_length
contenttypes
 [ ] 0001_initial
 [ ] 0002_remove_content_type_name
restaurant
 [ ] 0001_initial
 [ ] 0002_reservation_delete_menu
sessions
 [ ] 0001_initial

% python manage.py test          
Found 2 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
..
----------------------------------------------------------------------
Ran 2 tests in 0.022s

OK
Destroying test database for alias 'default'...

% python manage.py runserver     
Watching for file changes with StatReloader
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
September 01, 2024 - 20:28:22
Django version 5.1, using settings 'littlelemon.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

