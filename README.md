# booking-sys

[![Build and deploy container app to Azure Web App - booking-sys](https://github.com/conorheffron/booking-sys/actions/workflows/main_booking-sys.yml/badge.svg)](https://github.com/conorheffron/booking-sys/actions/workflows/main_booking-sys.yml)

[![Django CI](https://github.com/conorheffron/booking-sys/actions/workflows/django.yml/badge.svg)](https://github.com/conorheffron/booking-sys/actions/workflows/django.yml)

[![Pylint](https://github.com/conorheffron/booking-sys/actions/workflows/pylint.yml/badge.svg)](https://github.com/conorheffron/booking-sys/actions/workflows/pylint.yml)

[![Node.js CI](https://github.com/conorheffron/booking-sys/actions/workflows/node.js.yml/badge.svg)](https://github.com/conorheffron/booking-sys/actions/workflows/node.js.yml)

[![Docker Image CI](https://github.com/conorheffron/booking-sys/actions/workflows/docker-image.yml/badge.svg)](https://github.com/conorheffron/booking-sys/actions/workflows/docker-image.yml)

[![Docker Publish](https://github.com/conorheffron/booking-sys/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/conorheffron/booking-sys/actions/workflows/docker-publish.yml)

[![CodeQL Advanced](https://github.com/conorheffron/booking-sys/actions/workflows/codeql.yml/badge.svg)](https://github.com/conorheffron/booking-sys/actions/workflows/codeql.yml)

## Technologies
python3, django 5 admin/framework, django.test, & MySQL Server / Sqlite2

### Buil & Run via Docker
#### - Update 'DEBUG' in .env to True
```shell
docker image build -t booking-sys .
docker compose up -d
docker compose down
```

##### Expose API & UI
```shell
docker build -t booking-sys .
docker run -p 8000:8000 -p 5173:5173 booking-sys
```

##### Expose UI only oustide container
```shell
# dont need to expose API, can reach within container
docker build -t booking-sys .
docker run -p 5173:5173 booking-sys
```

## Generate requirements.txt
```shell
pipenv run pip freeze > requirements.txt
```

## Build Steps for pip environment.
```shell
cd booking-sys/backend/
sudo pipenv shell
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
pipenv run pylint $(git ls-files '*.py') --generated-members=objects --fail-under=9.2
```

## Run All Unit Tests
```shell
python3 manage.py test
```

## Run Test Class or specific Test Case
```shell
python3 manage.py test hr.test_apis.ApiTests
python3 manage.py test hr.test_apis.ApiTests.test_version_success
python3 manage.py test hr.test_forms.TestEditReservationForm
python3 manage.py test hr.test_forms.TestReservationForm
```

## Run Django Application
```shell
python3 manage.py runserver
```

## Sample Logs from VS Code Console via `docker compose up`
```shell
Compose can now delegate builds to bake for better performance.
 To do so, set COMPOSE_BAKE=true.
[+] Building 40.0s (12/12) FINISHED                                                                                                                                                docker:desktop-linux
 => [web internal] load build definition from Dockerfile                                                                                                                                           0.0s
 => => transferring dockerfile: 500B                                                                                                                                                               0.0s
 => [web internal] load metadata for docker.io/library/python:3.13                                                                                                                                 0.8s
 => [web internal] load .dockerignore                                                                                                                                                              0.0s
 => => transferring context: 2B                                                                                                                                                                    0.0s
 => [web internal] load build context                                                                                                                                                              0.3s
 => => transferring context: 178.02kB                                                                                                                                                              0.3s
 => CACHED [web 1/7] FROM docker.io/library/python:3.13@sha256:653b0cf8fc50366277a21657209ddd54edd125499d20f3520c6b277eb8c828d3                                                                    0.0s
 => => resolve docker.io/library/python:3.13@sha256:653b0cf8fc50366277a21657209ddd54edd125499d20f3520c6b277eb8c828d3                                                                               0.0s
 => [web 2/7] COPY . /                                                                                                                                                                             0.7s
 => [web 3/7] RUN pip install --no-cache-dir -r requirements.txt                                                                                                                                  25.4s
 => [web 4/7] RUN python3 manage.py makemigrations                                                                                                                                                 1.5s 
 => [web 5/7] RUN python3 manage.py migrate                                                                                                                                                        1.4s 
 => [web 6/7] RUN python3 manage.py test                                                                                                                                                           1.9s 
 => [web] exporting to image                                                                                                                                                                       7.6s 
 => => exporting layers                                                                                                                                                                            4.7s 
 => => exporting manifest sha256:943441684d370b85fbff87df1c20a4c1a994992c64aa83af5f396d9c76841332                                                                                                  0.0s 
 => => exporting config sha256:9339546d6634a21058ea22e3d7fef743b639919fdf252f07e596fe127e6ea3c7                                                                                                    0.0s 
 => => exporting attestation manifest sha256:b33ad238937463924650e5c74133b8a7016d62497ff80d3e85e2f52dfe80f778                                                                                      0.0s 
 => => exporting manifest list sha256:59d3cb23c1cd60b09b2433572d319257c0ce1644d5207050fdadaa3e2c680c2b                                                                                             0.0s
 => => naming to docker.io/library/booking-sys-web:latest                                                                                                                                          0.0s
 => => unpacking to docker.io/library/booking-sys-web:latest                                                                                                                                       2.8s
 => [web] resolving provenance for metadata file                                                                                                                                                   0.0s
[+] Running 3/3
 ✔ web                          Built                                                                                                                                                              0.0s 
 ✔ Network booking-sys_default  Created                                                                                                                                                            0.1s 
 ✔ Container booking-sys-web-1  Created                                                                                                                                                            0.4s 
Attaching to web-1
web-1  | INFO 2025-05-19 20:15:55,580 autoreload 7 140309415111552 Watching for file changes with StatReloader
web-1  | Performing system checks...
web-1  | 
web-1  | System check identified some issues:
web-1  | 
web-1  | WARNINGS:
web-1  | ?: (staticfiles.W004) The directory '/staticfiles' in the STATICFILES_DIRS setting does not exist.
web-1  | 
web-1  | System check identified 1 issue (0 silenced).
web-1  | May 19, 2025 - 20:15:55
web-1  | Django version 5.2.1, using settings 'booking-sys.settings'
web-1  | Starting development server at http://0.0.0.0:8000/
web-1  | Quit the server with CONTROL-C.
web-1  | 
web-1  | WARNING: This is a development server. Do not use it in a production setting. Use a production WSGI or ASGI server instead.
web-1  | For more information on production servers see: https://docs.djangoproject.com/en/5.2/howto/deployment/
.
.
.
web-1  | INFO 2025-05-19 20:16:07,210 views 7 140309358970560 GET Query set results: [(1, 'Conor Heffron', datetime.date(2025, 3, 9), datetime.time(2, 15)), (2, 'Sade Sings', datetime.date(2025, 3, 11), datetime.time(3, 1)), (3, 'Sade Song', datetime.date(2025, 3, 10), datetime.time(7, 0)), (4, 'Conor Heffron', datetime.date(2025, 3, 11), datetime.time(9, 0)), (5, 'Sade Sings', datetime.date(2025, 5, 9), datetime.time(22, 0)), (6, 'Sade Song', datetime.date(2025, 5, 23), datetime.time(20, 16)), (7, 'Conor', datetime.date(2025, 5, 22), datetime.time(22, 23)), (8, 'Sade Sings', datetime.date(2025, 5, 23), datetime.time(21, 34)), (9, 'Sade Sings', datetime.date(2025, 5, 20), datetime.time(21, 3)), (10, 'Halle Movie', datetime.date(2025, 5, 25), datetime.time(0, 21)), (11, 'Sade Sings', datetime.date(2025, 5, 19), datetime.time(22, 12))]
web-1  | INFO 2025-05-19 20:16:07,231 basehttp 7 140309358970560 "GET / HTTP/1.1" 200 2842
web-1  | INFO 2025-05-19 20:16:07,285 views 7 140309358970560 Request information (<WSGIRequest: GET '/version/'>)
web-1  | INFO 2025-05-19 20:16:07,285 views 7 140309358970560 Application version (2.8.5)
web-1  | INFO 2025-05-19 20:16:07,286 basehttp 7 140309358970560 "GET /version/ HTTP/1.1" 200 5
web-1  | INFO 2025-05-19 20:16:07,297 views 7 140309348484800 GET by date (2025-05-19) Query set results: [{'id': 11, 'first_name': 'Sade Sings', 'reservation_date': datetime.date(2025, 5, 19), 'reservation_slot': datetime.time(22, 12)}]
web-1  | INFO 2025-05-19 20:16:07,298 basehttp 7 140309348484800 "GET /bookings?date=2025-05-19 HTTP/1.1" 200 146
web-1  | INFO 2025-05-19 20:16:16,748 views 7 140309348484800 GET by date (2025-05-19) Query set results: [{'id': 11, 'first_name': 'Sade Sings', 'reservation_date': datetime.date(2025, 5, 19), 'reservation_slot': datetime.time(22, 12)}]
web-1  | INFO 2025-05-19 20:16:16,749 basehttp 7 140309348484800 "GET /bookings?date=2025-05-19 HTTP/1.1" 200 146
web-1  | INFO 2025-05-19 20:16:23,378 views 7 140309348484800 GET by date (2025-05-26) Query set results: []
web-1  | INFO 2025-05-19 20:16:23,379 basehttp 7 140309348484800 "GET /bookings?date=2025-05-26 HTTP/1.1" 200 42
web-1  | INFO 2025-05-19 20:16:25,316 views 7 140309348484800 GET by date (2025-05-26) Query set results: []
web-1  | INFO 2025-05-19 20:16:25,316 basehttp 7 140309348484800 "GET /bookings?date=2025-05-26 HTTP/1.1" 200 42
web-1  | INFO 2025-05-19 20:16:25,449 views 7 140309348484800 GET by date (2025-05-26) Query set results: []
web-1  | INFO 2025-05-19 20:16:25,449 basehttp 7 140309348484800 "GET /bookings?date=2025-05-26 HTTP/1.1" 200 42
web-1  | INFO 2025-05-19 20:16:25,655 views 7 140309348484800 GET by date (2025-05-26) Query set results: []
web-1  | INFO 2025-05-19 20:16:25,656 basehttp 7 140309348484800 "GET /bookings?date=2025-05-26 HTTP/1.1" 200 42
web-1  | INFO 2025-05-19 20:16:27,579 views 7 140309348484800 <QueryDict: {'csrfmiddlewaretoken': ['D2xErQeoWoWLOFaXu4MIaRbmzHicXeGckJ6RVHMSblzbsPEL7b0Iwk9fWr30tOHU'], 'first_name': ['Cleopatra'], 'reservation_date': ['2025-05-26'], 'reservation_slot': ['22:00']}>
web-1  | INFO 2025-05-19 20:16:27,604 views 7 140309348484800 POST Query set results: [{'id': 12, 'first_name': 'Cleopatra', 'reservation_date': datetime.date(2025, 5, 26), 'reservation_slot': datetime.time(22, 0)}]
web-1  | INFO 2025-05-19 20:16:27,605 basehttp 7 140309348484800 "POST / HTTP/1.1" 200 192
```

## Alternatively, Debug Django Application
- Go to 'Run and Debug' View in VS code
- Select launch.json confirguration 'Python: Current File' & Run
- Set breakpoints in views.py

![debug](./screenshots/debug.png?raw=true "Debug GET Bookings Request")

Free to use icon image at: [lemon](https://www.flaticon.com/free-animated-icon/lemon_14385026?term=lemon&page=1&position=5&origin=tag&related_id=14385026)


## Functionality Demo

###  App Home Address
- [http://localhost:5173/](http://localhost:5173/)

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

- [http://localhost:8000/api/bookings/2024-08-22/](http://localhost:8000/bookings/2024-08-22/)

  and

- [http://localhost:8000/api/bookings/2024-09-01/](http://localhost:8000/bookings/2024-09-01/)

Or using `request parameter 'date'`:

- [http://localhost:8000/api/bookings?date=2024-08-22](http://localhost:8000/bookings?date=2024-08-22)

  and

- [http://localhost:8000/api/bookings?date=2024-09-01](http://localhost:8000/bookings?date=2024-09-01)



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
% sudo pipenv shell              
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
