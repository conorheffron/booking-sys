# booking-sys

cd booking-sys
pipenv shell
pipenv install 

python manage.py makemigrations
python manage.py migrate

python3 manage.py test

python3 manage.py runserver