Welcome to our Spring 2025 Senior Capstone Project Website! 
Contributors: Mason McKnight, Ashith Reddy Alla, Adithya Gowda, Yu Hung Liang

Project dependencies are listed in requirements.txt.

In order to establish a local instance of the project database, you will need to install MySQL and MySQL Workbench.
You can download the installer here: https://dev.mysql.com/downloads/installer/
After downloading, run the installer and install both the latest version of MySQL Server and MySQL Workbench.
In the MySQL Server Configurator, take note of your admin user's username and password. These will need to be adjusted
in CapstoneSp25\settings.py in order to establish the database connection.

Once your local database is running, execute the SQL query "CREATE DATABASE Capstone".
Then, navigate to the folder containing manage.py and run the command "python manage.py makemigrations",
followed by command "python manage.py migrate". This will construct the full local instance of the database.

Once this is done and you've ensured your local MySQL Server is running, from the manage.py directory run
"python manage.py runserver". Then, in a web browser, navigate to "localhost:8000" to access the site! Note that you won't be able to make payments as there are no default expenses on the user. You may enter insurance details and create,
edit, and delete accounts, however.

