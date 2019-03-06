@echo off
echo "Installing requirements:"
pip install django
pip install django-macaddress
cd ..
echo "Preparing the migration now:"
python manage.py makemigrations
echo "Making the migration now:"
python manage.py migrate
echo "Create super user:"
python manage.py createsuperuser
pause