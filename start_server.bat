@echo off
echo Starting Django Development Server...
cd /d "%~dp0"
python manage.py runserver
pause

