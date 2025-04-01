To run it, 
cd email_app
python manage.py startapp emailer

You also need to create .env file in the project root with below info.

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=465
EMAIL_USE_SSL=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

Replace the last 2 lines with your info, The password means Security > App Passwords (We created in lab3)
