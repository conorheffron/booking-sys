# booking-sys

[![Build and deploy to Azure Web App - booking-sys](https://github.com/conorheffron/booking-sys/actions/workflows/main_booking-sys.yml/badge.svg)](https://github.com/conorheffron/booking-sys/actions/workflows/main_booking-sys.yml)

[![Django CI](https://github.com/conorheffron/booking-sys/actions/workflows/django.yml/badge.svg)](https://github.com/conorheffron/booking-sys/actions/workflows/django.yml)

[![Pylint](https://github.com/conorheffron/booking-sys/actions/workflows/pylint.yml/badge.svg)](https://github.com/conorheffron/booking-sys/actions/workflows/pylint.yml)

## Technologies
python3, django 5 admin/framework, django.test, & MySQL Server / Sqlite2

### Buil & Run via Docker
#### - Update 'DEBUG' in .env to True
```shell
docker image build -t booking-sys .
docker compose up -d  
docker compose down
```

## Generate requirements.txt
```shell
pipenv run pip freeze > requirements.txt
```

## Build Steps for pip environment.
```shell
cd booking-sys
pipenv shell
pipenv install -r  requirements.txt
```

## Create DB Schema on MySQL via Mac (mysql client for CLI)
### Start MySQL server
```shell
brew services start mysql
```

### Create `reservations` DB
```sql
mysql -u root -p 
CREATE DATABASE reservations;
exit;
```

### Restart or Stop MySQL server as needed
```shell
brew services stop mysql
```

## Apply model changes to DB
```shell
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py showmigrations
```

## Run Pylint
```shell
 pipenv run pylint $(git ls-files '*.py') --generated-members=objects --fail-under=9
```

## Run All Unit Tests
```shell
python3 manage.py test
```

## Run Test Class or specific Test Case
```shell
python3 manage.py test hr.tests.HrTests
python3 manage.py test hr.tests.HrTests.test_create_booking
```

## Run Django Application
```shell
python3 manage.py runserver
```

## Alternatively, Debug Django Application
- Go to 'Run and Debug' View in VS code
- Select launch.json confirguration 'Python: Current File' & Run
- Set breakpoints in views.py

![debug](./screenshots/debug.png?raw=true "Debug GET Bookings Request")

Free to use icon image at: [lemon](https://www.flaticon.com/free-animated-icon/lemon_14385026?term=lemon&page=1&position=5&origin=tag&related_id=14385026)


## Functionality Demo

###  App Home Address
- [http://localhost:8000/](http://localhost:8000/)

  or 

- [http://localhost:8000/book/](http://localhost:8000/book/)

###  Make a Reservation Form
![reserve](./screenshots/reserve.png?raw=true "Make a Reservation")

###  Date Picker
![date-picker](./screenshots/date-picker.png?raw=true "Date Picker")

###  Booking Complete Confirmation / Alert
![booking-complete](./screenshots/booking-complete.png?raw=true "Booking Complete")

###  View Current Bookings for Date Change in Booking Form
![bookings-by-date](./screenshots/bookings-by-date.png?raw=true "View Bookings By Date Change")

###  Bookings By Date REST API End-point (used for view template above)
Using `request path variable`:

- [http://localhost:8000/bookings/2024-08-22/](http://localhost:8000/bookings/2024-08-22/)

  and

- [http://localhost:8000/bookings/2024-09-01/](http://localhost:8000/bookings/2024-09-01/)

Or using `request parameter 'date'`:

- [http://localhost:8000/bookings?date=2024-08-22](http://localhost:8000/bookings?date=2024-08-22)

  and

- [http://localhost:8000/bookings?date=2024-09-01](http://localhost:8000/bookings?date=2024-09-01)



![postman](./screenshots/postman.png?raw=true "Postman GET Bookings Request")

###  Duplicate Booking Fail by Date & Time Value
![duplicate-booking-fail](./screenshots/duplicate-booking-fail.png?raw=true "Duplicate Booking Fail")

###  Date/Time in the Past Booking Fail 
![past-date-time-booking-fail](./screenshots/booking-date-in-past-fail.png?raw=true "Past Date/Time Booking Fail")

###  Dynamic JSON Table Update on Date Change
![dynamic-table-update](./screenshots/dynamic-table-update.png?raw=true "JSON Table Update")

###  View All Bookings Page
- [http://localhost:8000/reservations/](http://localhost:8000/reservations/)

![all-bookings](./screenshots/all-bookings.png?raw=true "View All Resrvations")

###  Hanlder 404
![handler404](./screenshots/handler404.png?raw=true "Handle Page Not Found Exception")


### Terminal Logs

####  - MySQL
```sql
% mysql -u root -p  
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 1610
Server version: 9.0.1 Homebrew

Copyright (c) 2000, 2018, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> USE reservations;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed

mysql> SHOW TABLES;
+----------------------------+
| Tables_in_reservations     |
+----------------------------+
| auth_group                 |
| auth_group_permissions     |
| auth_permission            |
| auth_user                  |
| auth_user_groups           |
| auth_user_user_permissions |
| django_admin_log           |
| django_content_type        |
| django_migrations          |
| django_session             |
| hr_reservation     |
+----------------------------+
11 rows in set (0.00 sec)

mysql> SELECT * FROM hr_reservation;
+----+------------+------------------+------------------+
| id | first_name | reservation_date | reservation_slot |
+----+------------+------------------+------------------+
| 48 | Test       | 2024-09-04       | 15:41:00.000000  |
| 49 | Test       | 2024-09-04       | 15:42:00.000000  |
| 50 | Test 2     | 2024-09-07       | 16:42:00.000000  |
+----+------------+------------------+------------------+
3 rows in set (0.00 sec)

mysql> DELETE FROM hr_reservation WHERE first_name='Test';
Query OK, 2 rows affected (0.01 sec)

mysql> SELECT * FROM hr_reservation;
+----+------------+------------------+------------------+
| id | first_name | reservation_date | reservation_slot |
+----+------------+------------------+------------------+
| 50 | Test 2     | 2024-09-07       | 16:42:00.000000  |
+----+------------+------------------+------------------+
1 row in set (0.00 sec)

mysql> SELECT DISTINCT first_name FROM hr_reservation;
+------------+
| first_name |
+------------+
| Test 2     |
+------------+
1 row in set (0.01 sec)

mysql> SELECT DISTINCT first_name FROM hr_reservation;
+------------+
| first_name |
+------------+
| Test 2     |
| Test 3     |
| Test       |
+------------+
3 rows in set (0.00 sec)

mysql> SELECT * FROM hr_reservation;
+----+------------+------------------+------------------+
| id | first_name | reservation_date | reservation_slot |
+----+------------+------------------+------------------+
| 50 | Test 2     | 2024-09-07       | 16:42:00.000000  |
| 51 | Test 3     | 2024-09-04       | 16:42:00.000000  |
| 52 | Test       | 2024-09-26       | 20:54:00.000000  |
+----+------------+------------------+------------------+
3 rows in set (0.00 sec)
```

####  - Bash for pip / python3
```shell
% pipenv shell              
Creating a virtualenv for this project...
Pipfile: /.../workspace/booking-sys/Pipfile
Using /usr/local/bin/python3 (3.12.4) to create virtualenv...
⠙ Creating virtual environment...created virtual environment CPython3.12.4.final.0-64 in 795ms
  creator CPython3macOsBrew(dest=/.../.local/share/virtualenvs/booking-sys-PIHfCB-G, clear=False, no_vcs_ignore=False, global=False)
  seeder FromAppData(download=False, pip=bundle, via=copy, app_data_dir=/.../Library/Application Support/virtualenv)
    added seed packages: pip==24.2
  activators BashActivator,CShellActivator,FishActivator,NushellActivator,PowerShellActivator,PythonActivator

% pipenv install
Installing dependencies from Pipfile.lock (84d28c)...

✔ Successfully created virtual environment!
Virtualenv location: /.../.local/share/virtualenvs/booking-sys-PIHfCB-G
Launching subshell in virtual environment...
 . /.../.local/share/virtualenvs/booking-sys-.../bin/activate
zsh compinit: insecure directories, run compaudit for list.

% python3 manage.py makemigrations
No changes detected

% python3 manage.py migrate       
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, hr, sessions
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
  Applying hr.0001_initial... OK
  Applying hr.0002_reservation_delete_menu... OK
  Applying sessions.0001_initial... OK

% python3 manage.py showmigrations
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
hr
 [ ] 0001_initial
 [ ] 0002_reservation_delete_menu
sessions
 [ ] 0001_initial

% python3 manage.py test          
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
Django version 5.1, using settings 'booking-sys.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```
