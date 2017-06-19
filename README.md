# svnit-tnp
Managing SVNIT's Training and Placement Data effectively.

Steps to set up local development environment for this project!

### 1) Install System Dependencies
```sh
sudo apt-get update
sudo apt-get install python3-pip python3-dev
sudo apt-get install mysql-server libmysqlclient-dev
```
*Keep the password for MySQL root user as 'root' for simplicity.*

### 2) Set up Virtual Environment for development
```sh
sudo -H pip3 install --upgrade pip
sudo -H pip3 install virtualenv
```
```sh
mkdir ~/tnp3
virtualenv ~/tnp3/tnp3
source ~/tnp3/tnp3/bin/activate    #For activating the virtualenv
```

The next steps assume that you are in the activated virtualenv.

### 3) Django Application Setup
```sh
cd ~
git clone https://github.com/aakashrana1995/svnit-tnp.git
cd svnit-tnp/tnp
pip install -r requirements.txt
```

### 4) Database setup
```sh
mysql -u root -p    #Enter your password on prompt
```
Now, in your mysql shell `mysql>`,
```mysql
create database tnp;
exit
```
Create required tables using migration.
```sh
python manage.py migrate
```

### 5) Running the development server
Change the first line in ```tnp/settings/__init__.py``` to following:
```python
from .dev import *
```
Now run the development server
```sh
python manage.py runserver
```
Go to ```http://127.0.0.1:8000``` to see the homepage!
