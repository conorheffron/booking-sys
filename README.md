# booking-sys

[![Build and deploy container app to Azure Web App - booking-sys](https://github.com/conorheffron/booking-sys/actions/workflows/main_booking-sys.yml/badge.svg)](https://github.com/conorheffron/booking-sys/actions/workflows/main_booking-sys.yml)

[![Django CI](https://github.com/conorheffron/booking-sys/actions/workflows/django.yml/badge.svg)](https://github.com/conorheffron/booking-sys/actions/workflows/django.yml)

[![Pylint](https://github.com/conorheffron/booking-sys/actions/workflows/pylint.yml/badge.svg)](https://github.com/conorheffron/booking-sys/actions/workflows/pylint.yml)

[![Node.js CI](https://github.com/conorheffron/booking-sys/actions/workflows/node.js.yml/badge.svg)](https://github.com/conorheffron/booking-sys/actions/workflows/node.js.yml)

[![Node.js Package](https://github.com/conorheffron/booking-sys/actions/workflows/npm-publish-packages.yml/badge.svg)](https://github.com/conorheffron/booking-sys/actions/workflows/npm-publish-packages.yml)

[![Docker Image CI](https://github.com/conorheffron/booking-sys/actions/workflows/docker-image.yml/badge.svg)](https://github.com/conorheffron/booking-sys/actions/workflows/docker-image.yml)

[![Docker Publish](https://github.com/conorheffron/booking-sys/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/conorheffron/booking-sys/actions/workflows/docker-publish.yml)

[![CodeQL Advanced](https://github.com/conorheffron/booking-sys/actions/workflows/codeql.yml/badge.svg)](https://github.com/conorheffron/booking-sys/actions/workflows/codeql.yml)

### SonarQube

[![Build](https://github.com/conorheffron/booking-sys/actions/workflows/sonar.yml/badge.svg)](https://github.com/conorheffron/booking-sys/actions/workflows/sonar.yml)

[Sonar Cloud Overall Code Summary](https://sonarcloud.io/summary/overall?id=conorheffron_booking-sys&branch=main)

## Technologies
python3, django 5 admin/framework, django.test, React 18, & MySQL Server / Sqlite2

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
[+] Running 1/1
 ! app Warning pull access denied for booking-sys, repository does not exist or may require 'docker login'                                                                                       1.3s 
Compose can now delegate builds to bake for better performance.
 To do so, set COMPOSE_BAKE=true.
[+] Building 16.1s (17/17) FINISHED                                                                                                                                              docker:desktop-linux
 => [app internal] load build definition from Dockerfile                                                                                                                                         0.0s
 => => transferring dockerfile: 983B                                                                                                                                                             0.0s
 => [app internal] load metadata for docker.io/library/python:3.13-slim                                                                                                                          0.6s
 => [app internal] load .dockerignore                                                                                                                                                            0.0s
 => => transferring context: 2B                                                                                                                                                                  0.0s
 => [app  1/11] FROM docker.io/library/python:3.13-slim@sha256:f2fdaec50160418e0c2867ba3e254755edd067171725886d5d303fd7057bbf81                                                                  0.0s
 => => resolve docker.io/library/python:3.13-slim@sha256:f2fdaec50160418e0c2867ba3e254755edd067171725886d5d303fd7057bbf81                                                                        0.0s
 => [app internal] load build context                                                                                                                                                            1.2s
 => => transferring context: 1.02MB                                                                                                                                                              1.2s
 => CACHED [app  2/11] RUN apt-get update &&     apt-get install -y --no-install-recommends       default-libmysqlclient-dev build-essential pkg-config curl &&     curl -fsSL https://deb.node  0.0s
 => CACHED [app  3/11] COPY backend/requirements.txt /backend/                                                                                                                                   0.0s
 => CACHED [app  4/11] RUN pip install --upgrade pip && pip install -r /backend/requirements.txt                                                                                                 0.0s
 => CACHED [app  5/11] COPY frontend/package*.json /frontend/                                                                                                                                    0.0s
 => CACHED [app  6/11] RUN npm --prefix /frontend install                                                                                                                                        0.0s
 => CACHED [app  7/11] COPY backend/ /backend/                                                                                                                                                   0.0s
 => CACHED [app  8/11] COPY frontend/ /frontend/                                                                                                                                                 0.0s
 => CACHED [app  9/11] RUN cd backend && python manage.py collectstatic --noinput                                                                                                                0.0s
 => CACHED [app 10/11] COPY entrypoint.sh /entrypoint.sh                                                                                                                                         0.0s
 => CACHED [app 11/11] RUN chmod +x /entrypoint.sh                                                                                                                                               0.0s
 => [app] exporting to image                                                                                                                                                                    14.0s
 => => exporting layers                                                                                                                                                                          0.0s
 => => exporting manifest sha256:cce67f7a8e97f6268c4d90b21f31c57393184d0e75ad9a9f22acdf15b0ee3a3f                                                                                                0.0s
 => => exporting config sha256:d3cdf8db09be519aa45c11a4e5f0f64011c2ce287921f972860b4789e9b43f27                                                                                                  0.0s
 => => naming to docker.io/library/booking-sys:latest                                                                                                                                            0.0s
 => => unpacking to docker.io/library/booking-sys:latest                                                                                                                                        14.0s
 => [app] resolving provenance for metadata file                                                                                                                                                 0.0s
[+] Running 3/3
 ✔ app                          Built                                                                                                                                                            0.0s 
 ✔ Network booking-sys_default  Created                                                                                                                                                          0.1s 
 ✔ Container booking-sys        Created                                                                                                                                                          1.0s 
Attaching to booking-sys
booking-sys  | System check identified some issues:
booking-sys  | 
booking-sys  | WARNINGS:
booking-sys  | ?: (staticfiles.W004) The directory '/backend/staticfiles' in the STATICFILES_DIRS setting does not exist.
booking-sys  | 
booking-sys  | 0 static files copied to '/backend/hr/static', 127 unmodified.
booking-sys  | INFO 2025-06-15 00:04:28,827 autoreload 10 140691409173376 Watching for file changes with StatReloader
booking-sys  | System check identified some issues:
booking-sys  | 
booking-sys  | WARNINGS:
booking-sys  | ?: (staticfiles.W004) The directory '/backend/staticfiles' in the STATICFILES_DIRS setting does not exist.
booking-sys  | 
booking-sys  | System check identified 1 issue (0 silenced).
booking-sys  | 
booking-sys  | > booking-sys-frontend@3.0.2 dev
booking-sys  | > vite --host
booking-sys  | 
booking-sys  | 
booking-sys  |   VITE v6.3.5  ready in 269 ms
booking-sys  | 
booking-sys  |   ➜  Local:   http://localhost:5173/
booking-sys  |   ➜  Network: http://172.18.0.2:5173/
.
.
.
booking-sys  | INFO 2025-06-15 00:04:36,341 views 10 140691355207360 Request information (<WSGIRequest: GET '/api/version/'>)
booking-sys  | INFO 2025-06-15 00:04:36,362 views 10 140691355207360 Application version (3.0.3)
booking-sys  | INFO 2025-06-15 00:04:36,364 basehttp 10 140691355207360 "GET /api/version/ HTTP/1.1" 200 5
booking-sys  | INFO 2025-06-15 00:04:36,379 views 10 140691344721600 GET by date (2025-06-15) Query set results: [{'id': 2, 'first_name': 'Halle Movie', 'reservation_date': datetime.date(2025, 6, 15), 'reservation_slot': datetime.time(12, 30)}]
booking-sys  | INFO 2025-06-15 00:04:36,385 views 10 140691334235840 Request information (<WSGIRequest: GET '/api/version/'>)
booking-sys  | INFO 2025-06-15 00:04:36,388 views 10 140691334235840 Application version (3.0.3)
booking-sys  | INFO 2025-06-15 00:04:36,385 basehttp 10 140691344721600 "GET /api/bookings?date=2025-06-15 HTTP/1.1" 200 146
booking-sys  | INFO 2025-06-15 00:04:36,392 basehttp 10 140691334235840 "GET /api/version/ HTTP/1.1" 200 5
booking-sys  | INFO 2025-06-15 00:04:36,412 views 10 140691248252608 GET by date (2025-06-15) Query set results: [{'id': 2, 'first_name': 'Halle Movie', 'reservation_date': datetime.date(2025, 6, 15), 'reservation_slot': datetime.time(12, 30)}]
booking-sys  | INFO 2025-06-15 00:04:36,414 basehttp 10 140691248252608 "GET /api/bookings?date=2025-06-15 HTTP/1.1" 200 146
booking-sys  | INFO 2025-06-15 00:04:36,431 views 10 140691237766848 GET by date (2025-06-15) Query set results: [{'id': 2, 'first_name': 'Halle Movie', 'reservation_date': datetime.date(2025, 6, 15), 'reservation_slot': datetime.time(12, 30)}]
booking-sys  | INFO 2025-06-15 00:04:36,434 basehttp 10 140691237766848 "GET /api/bookings?date=2025-06-15 HTTP/1.1" 200 146
booking-sys  | INFO 2025-06-15 00:04:36,447 views 10 140691227281088 GET by date (2025-06-15) Query set results: [{'id': 2, 'first_name': 'Halle Movie', 'reservation_date': datetime.date(2025, 6, 15), 'reservation_slot': datetime.time(12, 30)}]
booking-sys  | INFO 2025-06-15 00:04:36,449 basehttp 10 140691227281088 "GET /api/bookings?date=2025-06-15 HTTP/1.1" 200 146
booking-sys  | INFO 2025-06-15 00:04:43,893 views 10 140691227281088 Request information (<WSGIRequest: GET '/api/version/'>)
booking-sys  | INFO 2025-06-15 00:04:43,894 views 10 140691227281088 Application version (3.0.3)
booking-sys  | INFO 2025-06-15 00:04:43,895 basehttp 10 140691227281088 "GET /api/version/ HTTP/1.1" 200 5
booking-sys  | INFO 2025-06-15 00:04:43,903 views 10 140691237766848 GET by future date (after 2025-06-15) Query set results: []
booking-sys  | INFO 2025-06-15 00:04:43,906 views 10 140691248252608 Request information (<WSGIRequest: GET '/api/version/'>)
booking-sys  | INFO 2025-06-15 00:04:43,906 views 10 140691248252608 Application version (3.0.3)
booking-sys  | INFO 2025-06-15 00:04:43,908 basehttp 10 140691237766848 "GET /api/bookings HTTP/1.1" 200 42
booking-sys  | INFO 2025-06-15 00:04:43,911 basehttp 10 140691248252608 "GET /api/version/ HTTP/1.1" 200 5
booking-sys  | INFO 2025-06-15 00:04:43,925 views 10 140691334235840 GET by future date (after 2025-06-15) Query set results: []
booking-sys  | INFO 2025-06-15 00:04:43,928 basehttp 10 140691334235840 "GET /api/bookings HTTP/1.1" 200 42
booking-sys  | INFO 2025-06-15 00:04:45,813 views 10 140691353110208 Request information (<WSGIRequest: GET '/api/version/'>)
booking-sys  | INFO 2025-06-15 00:04:45,813 views 10 140691353110208 Application version (3.0.3)
booking-sys  | INFO 2025-06-15 00:04:45,818 basehttp 10 140691353110208 "GET /api/version/ HTTP/1.1" 200 5
booking-sys  | INFO 2025-06-15 00:04:45,821 views 10 140691216795328 GET by date (2025-06-15) Query set results: [{'id': 2, 'first_name': 'Halle Movie', 'reservation_date': datetime.date(2025, 6, 15), 'reservation_slot': datetime.time(12, 30)}]
booking-sys  | INFO 2025-06-15 00:04:45,825 basehttp 10 140691216795328 "GET /api/bookings?date=2025-06-15 HTTP/1.1" 200 146
booking-sys  | INFO 2025-06-15 00:04:45,830 views 10 140691206309568 Request information (<WSGIRequest: GET '/api/version/'>)
booking-sys  | INFO 2025-06-15 00:04:45,830 views 10 140691206309568 Application version (3.0.3)
booking-sys  | INFO 2025-06-15 00:04:45,833 basehttp 10 140691206309568 "GET /api/version/ HTTP/1.1" 200 5
booking-sys  | INFO 2025-06-15 00:04:45,838 views 10 140691195823808 GET by date (2025-06-15) Query set results: [{'id': 2, 'first_name': 'Halle Movie', 'reservation_date': datetime.date(2025, 6, 15), 'reservation_slot': datetime.time(12, 30)}]
booking-sys  | INFO 2025-06-15 00:04:45,841 basehttp 10 140691195823808 "GET /api/bookings?date=2025-06-15 HTTP/1.1" 200 146
booking-sys  | INFO 2025-06-15 00:04:45,851 views 10 140691046926016 GET by date (2025-06-15) Query set results: [{'id': 2, 'first_name': 'Halle Movie', 'reservation_date': datetime.date(2025, 6, 15), 'reservation_slot': datetime.time(12, 30)}]
booking-sys  | INFO 2025-06-15 00:04:45,853 basehttp 10 140691046926016 "GET /api/bookings?date=2025-06-15 HTTP/1.1" 200 146
booking-sys  | INFO 2025-06-15 00:04:45,865 views 10 140691036440256 GET by date (2025-06-15) Query set results: [{'id': 2, 'first_name': 'Halle Movie', 'reservation_date': datetime.date(2025, 6, 15), 'reservation_slot': datetime.time(12, 30)}]
booking-sys  | INFO 2025-06-15 00:04:45,867 basehttp 10 140691036440256 "GET /api/bookings?date=2025-06-15 HTTP/1.1" 200 146
booking-sys  | INFO 2025-06-15 00:04:50,749 views 10 140691046926016 GET by date (2025-06-16) Query set results: []
booking-sys  | INFO 2025-06-15 00:04:50,751 basehttp 10 140691046926016 "GET /api/bookings?date=2025-06-16 HTTP/1.1" 200 42
booking-sys  | INFO 2025-06-15 00:04:53,700 basehttp 10 140691195823808 "GET /api/csrf/ HTTP/1.1" 200 49
booking-sys  | INFO 2025-06-15 00:04:53,722 basehttp 10 140691206309568 "PUT /api/reservations HTTP/1.1" 201 119
booking-sys  | INFO 2025-06-15 00:04:53,730 views 10 140691216795328 GET by date (2025-06-16) Query set results: [{'id': 3, 'first_name': 'Sade Song', 'reservation_date': datetime.date(2025, 6, 16), 'reservation_slot': datetime.time(11, 0)}]
booking-sys  | INFO 2025-06-15 00:04:53,732 basehttp 10 140691216795328 "GET /api/bookings?date=2025-06-16 HTTP/1.1" 200 144
booking-sys  | INFO 2025-06-15 00:05:00,536 views 10 140691353110208 GET by date (2025-06-19) Query set results: []
booking-sys  | INFO 2025-06-15 00:05:00,544 basehttp 10 140691353110208 "GET /api/bookings?date=2025-06-19 HTTP/1.1" 200 42
booking-sys  | INFO 2025-06-15 00:05:01,504 basehttp 10 140691342624448 "GET /api/csrf/ HTTP/1.1" 200 49
booking-sys  | INFO 2025-06-15 00:05:01,526 basehttp 10 140691332138688 "PUT /api/reservations HTTP/1.1" 201 121
booking-sys  | INFO 2025-06-15 00:05:01,536 views 10 140691248252608 GET by date (2025-06-19) Query set results: [{'id': 4, 'first_name': 'Halle Movie', 'reservation_date': datetime.date(2025, 6, 19), 'reservation_slot': datetime.time(11, 0)}]
booking-sys  | INFO 2025-06-15 00:05:01,537 basehttp 10 140691248252608 "GET /api/bookings?date=2025-06-19 HTTP/1.1" 200 146
booking-sys  | INFO 2025-06-15 00:05:02,919 views 10 140691237766848 Request information (<WSGIRequest: GET '/api/version/'>)
booking-sys  | INFO 2025-06-15 00:05:02,920 views 10 140691237766848 Application version (3.0.3)
booking-sys  | INFO 2025-06-15 00:05:02,928 basehttp 10 140691237766848 "GET /api/version/ HTTP/1.1" 200 5
booking-sys  | INFO 2025-06-15 00:05:02,930 views 10 140691248252608 GET by future date (after 2025-06-15) Query set results: [{'id': 4, 'first_name': 'Halle Movie', 'reservation_date': datetime.date(2025, 6, 19), 'reservation_slot': datetime.time(11, 0)}, {'id': 3, 'first_name': 'Sade Song', 'reservation_date': datetime.date(2025, 6, 16), 'reservation_slot': datetime.time(11, 0)}]
booking-sys  | INFO 2025-06-15 00:05:02,933 basehttp 10 140691248252608 "GET /api/bookings HTTP/1.1" 200 250
booking-sys  | INFO 2025-06-15 00:05:02,941 views 10 140691332138688 Request information (<WSGIRequest: GET '/api/version/'>)
booking-sys  | INFO 2025-06-15 00:05:02,941 views 10 140691332138688 Application version (3.0.3)
booking-sys  | INFO 2025-06-15 00:05:02,951 basehttp 10 140691332138688 "GET /api/version/ HTTP/1.1" 200 5
booking-sys  | INFO 2025-06-15 00:05:02,952 views 10 140691342624448 GET by future date (after 2025-06-15) Query set results: [{'id': 4, 'first_name': 'Halle Movie', 'reservation_date': datetime.date(2025, 6, 19), 'reservation_slot': datetime.time(11, 0)}, {'id': 3, 'first_name': 'Sade Song', 'reservation_date': datetime.date(2025, 6, 16), 'reservation_slot': datetime.time(11, 0)}]
booking-sys  | INFO 2025-06-15 00:05:02,954 basehttp 10 140691342624448 "GET /api/bookings HTTP/1.1" 200 250
```

## Alternatively, Debug Django Application
- Go to 'Run and Debug' View in VS code
- Select launch.json confirguration 'Python: Bookings API' & Run
- Set breakpoints in views.py

![debug](./screenshots/debug.png?raw=true "Debug GET Bookings Request")

## Functionality Demo

###  App Frontend Home Address
- [http://localhost:5173/](http://localhost:5173/)

###  API End-point
- [http://localhost:8000/api/](http://localhost:8000/api/)

###  Django Admin UI
- [http://localhost:5173/admin](http://localhost:5173/admin)

###  Make a Reservation Form
![reserve](./screenshots/reserve.png?raw=true "Make a Reservation")

###  Date Picker
![date-picker](./screenshots/date-picker.png?raw=true "Date Picker")

###  Booking Complete Confirmation / Alert
![booking-complete](./screenshots/booking-complete.png?raw=true "Booking Complete")

###  View Current Bookings for Date Change in Booking Form
![bookings-by-date](./screenshots/bookings-by-date.png?raw=true "View Bookings By Date Change")

###  Bookings By Date REST API End-point (used for view template above)
Using `request parameter 'date'`:

- [http://localhost:8000/api/bookings?date=2024-08-22](http://localhost:8000/api/bookings?date=2024-08-22)

  and

- [http://localhost:8000/api/bookings?date=2024-09-01](http://localhost:8000/api/bookings?date=2024-09-01)



![postman](./screenshots/postman.png?raw=true "Postman GET Bookings Request")

###  Duplicate Booking Fail by Date & Time Value
![duplicate-booking-fail](./screenshots/duplicate-booking-fail.png?raw=true "Duplicate Booking Fail")

###  Date/Time in the Past Booking Fail 
![past-date-time-booking-fail](./screenshots/booking-date-in-past-fail.png?raw=true "Past Date/Time Booking Fail")

###  Dynamic JSON Table Update on Date Change
![dynamic-table-update](./screenshots/dynamic-table-update.png?raw=true "JSON Table Update")

###  View All Bookings Page
- [http://localhost:8000/api/bookings](http://localhost:8000/api/bookings)

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
Found 23 test(s).
Creating test database for alias 'default'...
System check identified some issues:

WARNINGS:
?: (staticfiles.W004) The directory '******/booking-sys/backend/staticfiles' in the STATICFILES_DIRS setting does not exist.

System check identified 1 issue (0 silenced).
..............INFO 2025-06-15 00:17:20,300 views 43359 140704407604672 Request information (<WSGIRequest: GET '/version'>)
INFO 2025-06-15 00:17:20,300 views 43359 140704407604672 Application version (3.0.3)
.........
----------------------------------------------------------------------
Ran 23 tests in 0.049s

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
### Test Coverage
```shell
(booking-sys) backend(base) % pipenv run coverage run manage.py test
Found 23 test(s).
.
.
.
Ran 23 tests in 0.112s

OK
Destroying test database for alias 'default'...


(booking-sys) backend(base) % pipenv run coverage report
Name                                         Stmts   Miss  Cover
----------------------------------------------------------------
booking-sys/__init__.py                          0      0   100%
booking-sys/settings.py                         41      7    83%
booking-sys/urls.py                              5      0   100%
hr/__init__.py                                   6      0   100%
hr/admin.py                                      0      0   100%
hr/apps.py                                       4      0   100%
hr/forms.py                                     13      0   100%
hr/migrations/0001_initial.py                    5      0   100%
hr/migrations/0002_alter_reservation_id.py       4      0   100%
hr/migrations/__init__.py                        0      0   100%
hr/models.py                                     6      0   100%
hr/test_apis.py                                115      0   100%
hr/test_forms.py                                53      0   100%
hr/time_utils.py                                21      1    95%
hr/urls.py                                       3      0   100%
hr/views.py                                    129     42    67%
manage.py                                        8      0   100%
----------------------------------------------------------------
TOTAL                                          413     50    88%
```
