@echo off
echo "Installing requirements:"
pip install mod_wsgi django mysqlclient phonenumbers django-macaddress django-phonenumber-field django-recaptcha
cd ..
echo "Making the migration now:"
python manage.py migrate
echo "Create super user:"
python manage.py createsuperuser
pause