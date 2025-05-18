@echo off
echo Starting Django server with CORS support...
echo.
echo API will be accessible at:
echo - http://localhost:8000/api/logs/
echo.
echo For local network access, use one of these IP addresses:
ipconfig | findstr "IPv4"
echo.
echo Remember to append :8000/api/logs/ to the IP address
echo.
echo Press Ctrl+C to stop the server
echo.

cd %~dp0
python manage.py runserver 0.0.0.0:8000