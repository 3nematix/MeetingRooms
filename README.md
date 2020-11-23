# About Meeting Rooms
Company needs an internal service for its’ employees which helps them to reserve companies
meeting room for internal or external meetings. Each employee should be able to check each
room’s availability, book or cancel a reservation through an API.
This project is built using: Django and Python3, Django Rest Framework, SQL.

# API 
This API includes:
* Token Authentication & Logout
* Employee system
* Meeting Rooms and Reservations
* Invitation system


# Preparation & Installation
This guide will be following installation steps on a Linux Ubuntu 18.04.4 (<a href="https://www.virtualbox.org/">Oracle VM VirtualBox</a>).

<b>1. Install Required linux packages:</b>

* We will be Working with Python3, so we need to install the package-management system for it
<br/>`sudo apt-get install python3-pip`.

* I personally love working with PostgreSQL, so for this tutorial I'm going to use it. You can install PostgreSQL and its library with `sudo apt-get install -y libpq-dev postgresq`.

<b>2. PostgreSQL Configuration</b>

Now, we need to set-up the default Postgres user so that we would be able to use it locally on our Django server. By default PostgreSQL server should automatically start after installation, if something goes wrong you can always check its status by typing
<br/>`sudo service postgresql status`.

The default authentication mode for PostgreSQL is set to ident, so we are going to set the postgres password manually.

* To set a password for postgres, we need to send some queries by using our terminal-based front-end for PostgreSQL. To do that, we actually need to switch to the Super User DO, we can do that by typing <br/>`sudo su postgres psql`.

* Now, I'm going to set postgres user password to 'Testpass1234'<br/>`ALTER USER postgres WITH PASSWORD 'Testpass1234';`. After successfull Query in your terminal, you should see `ALTER ROLE`.

* Don't forget to create a Database, in this case I will create a Database named - `meetingsapi`, `CREATE DATABASE meetingsapi;`.

* So far we got everything up and running, now we need to change `HBA` and `CONFIG` files, to get their location we simply send few queries `SHOW HBA_FILE;` and `SHOW CONFIG_FILE;`, you can exit with `ctrl + d`. 

* I'm going to use a simple line text editor for Unix and Linux `sudo nano /etc/postgresql/10/main/pg_hba.conf`, scroll to the bottom and add a line `host all all 0.0.0.0/00 md5`, this will let PostgreSQL to accept the connections not only from localhost.

* Also we need to specify the TCP/IP address(es) on which the server will listen for connections from client applications, we can do that by typing `sudo nano /etc/postgresql/10/main/postgresql.conf` and then adding `listen_addresses = '*'` to the bottom line.

* After all these changes made, we need to restart the PostgreSQL server with `sudo service postgresql restart`.

<b>3. Setting up the project</b>

* Navigate to your home directory with `cd` and clone the repository and cd into it <br/>`git clone https://github.com/3nematix/MeetingRooms.git && cd MeetingRooms`.

* I'm going to keep all my private settings & configs in .env file `sudo touch .env && sudo nano .env`. These are the settings which I used, make sure to follow this format! <br/> <img src="https://i.gyazo.com/3cd6bb55e107bb074faecf2d1e5156f8.png" alt="env_file"/>

* Install virtualenv `sudo -H pip3 install -U pipenv`, then activate it `pipenv shell` to exit `exit`. Install from Pipfile, if there is one: `pipenv install`.

<b>4. Launching The Project</b>

* Make sure to create the migrations `python manage.py makemigrations` and apply them `python manage.py migrate`.

* To run the Django server locally - `sh run_server.sh`.

# Documentation
