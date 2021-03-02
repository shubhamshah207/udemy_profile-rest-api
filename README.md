# Profiles REST API

.md stands for mark down
Profiles REST API course file.

git commit -am "Comments"

a stands for all and m stands for message.

ssh-keygen -t rsa -b 4096 -C "shubhamshah207@gmail.com"
t = type
b = bytes
C = Comment


After adding public key and creating new repository...
git remote add origin https://github.com/shubhamshah207/udemy_profile-rest-api.git
git branch -M main
git push -u origin main


Create vagrant file
vagrant init ubuntu/bionic64

in git bash
vagrant up (download os create machine using virtualbox and run the commands mention in vagrantfile) or to start virtual box

to connect to guest server
vagrant ssh

Synchronized project files in devlopment server - how vagrant works
cd /vagrant/

https://python-guide.readthedocs.io/en/latest/dev/virtualenvs/

pip install -r requirements.txt (r means requirements)

django-admin.py startproject projectname pathtocreate

python manage.py startapp profiles_api
Enable app by settings.py INSTALLED_APPS append ["rest_framework", "rest_framework.authtoken"]

python manage.py runserver 0.0.0.0:8000
