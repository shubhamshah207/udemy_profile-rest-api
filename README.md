git config --global user.email "shubhamshah207@gmail.com"
git config --global user.name "Shubham Shah"
git init
git add .
# Profiles REST API

.md stands for mark down
Profiles REST API course file.

git commit -am "Comments"

a stands for all and m stands for message.

ls ~/.ssh

to generate public and private key in unix
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

to create new project in django
django-admin.py startproject projectname pathtocreate

python manage.py startapp profiles_api
Enable app by settings.py INSTALLED_APPS append ["rest_framework", "rest_framework.authtoken"]

python manage.py runserver 0.0.0.0:8000

models meaning tables in database

models.py
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionMixin

create manager and user in models.py

AUTH_USER_MODEL = 'prifiles_api.UserProfile' in settings.py to use custom user model

django manages database with the use of migration files(stores all of the steps required to make our database match our django models)
python manage.py makemigrations profiles_api
if you add a new model to our project then it will be able to create new table in the database.
this steps are done in migration files.

To run migration files
python manage.py migrate

To enable django admin for our user profile model. By default django admin is already enabled on all new projects.
However you need to register any newly created models with the django admin so it knows that you want to display that model in the admin interface.
Add to django admin by adding site to admin.py


Django REST framework views:
1. APIView
2. ViewSet


API View
Describe logic to make API endpoint

What is APIView?
Uses the standard HTTP methods for functions
Give you the most control over logic:
	Perfect for implementing complex logic
	Calling other apis
	Working with other files

When to use APIViews?
	Need full control over the logic
	Processing files and rendering a synchronous response
	You are calling other apis/services
	Accessing local files or data


APIView in views.py


set urls using include in urls.py

from rest_framework import serializers

extend serializers.Serializer

Sealizers -- allows to convert data inputs to python objects and vice verca.
Similar to django forms.


ViewSets:
What are view sets?
	use model operations for functions(methods related to objects like list, create, etc.)
	takes care of a lot of typical logic for you.
	perfect for standard database operations.
	fastest way to make a database interface.

When to use ViewSets?
 	API that performs a simple crud operation. (A simple CRUD interface to your database)
	need a quick and simple api
	Little to no customization on the logic.
	when you are working with standard data structure.

import rest_framework import viewsets
extends viewsets.ViewSet

to register viewset we need to use router
from rest_framework.routers import DefaultRouter (Check urls.py)
router = DefaultRouter()
router.register('hello-viewset', views.HelloViewset, base_name='hello-viewset')

#######################################################
basename - The base to use for the URL names that are created. If unset the basename will be automatically generated based on the queryset attribute of the viewset, if it has one. Note that if the viewset does not include a queryset attribute then you must set basename when registering the viewset.
The example above would generate the following URL patterns:

URL pattern: ^users/$ Name: 'user-list'
URL pattern: ^users/{pk}/$ Name: 'user-detail'
URL pattern: ^accounts/$ Name: 'account-list'
URL pattern: ^accounts/{pk}/$ Name: 'account-detail'
#######################################################

if you specify a primary key in url then it will go for Put, patch and delete requests
_______________________________________________________________________________________________________________________
USER PROFILE API (Description)

1. Create new profile
	Handle registration of new users
	Validate profile data

2. Listing existing profiles
	search for profiles by Email and Name

3. Viewing a specific profiles
	Profile Id

4. Update the profile of a logged in user
	Change name email and password

5. Delete profile

API URLS

/api/profile/ - 							list all profiles when HTTP GET Method is called.
															Create a new profile when HTTP POST method is called.

/api/profile/<profile_id>/ - 	view specific profile details by using HTTP GET.
															update object using HTTP PUT/PATCH
															remove completely from the system using HTTP DELETE
______________________________________________________________________________________________________________________
SERIALIZER - UserProfileSerializer

extend serializers.ModelSerializer (to user model)
use a Meta class to configure the serializer to point to a specific model

you need to specify a list of fields in our model that we want to manage through our serializer

we need to make password field write only, for security it shouldn't be fetched or retrieved.
extra_kwargs = {
	'password': {
		'write_only': True,
		'style':{ 'input_type': 'password'} # to hide while typing same as html input type password
	}
}

override the create function, by default model serializer allows you to create simple objects in the databases. So it uses the default create function of the object manager to create the object. we need to override this with create_user function
just create new function create in the serializer class.

We will use model view set for our UserProfile model
extends viewsets.ModelViewSet

from profiles_api import models

override queryset variable to define model for ViewSet
queryset = models.UserProfile.objects.all()

add user to router (urls.py)

as we have queryset object in our viewset we do not need to provide base_name in urls.py
Django can figure out the name from the model assigned to it.
So you only need to give base_class for the viewsets, for which you are not defining the queryset.

We will do the user profile security part(so that logged in user can only update his own profile) using django permissions class

from rest_framework import permissions

PERMISSION CLASS - UpdateOwnProfile
extends BasePermission

safe methods are the methods which do not change the object value for an instance HTTP GET

when you authenticate a request in django rest rest_framework it will assign the authenticated user profile to the request and we can use this to compare it to the object that is being updated

from rest_framework.authentication import TokenAuthentication
It is a type of authentication that we use for users to authenticate themselves with our API.
It works by generating a random token string when user logs in and then every request we make to their api that we need to authenticate we add this tokenstring to request.

Effectively token can be the type of password to check the every request made is authenticated correctly.

To authenticate the user
authentication_classes = (TokenAuthentication,) # so that this gets created as a tuple.
you can append all the authentication classes to this tuple which we want to use.

To check permissions
permission_classes = (permissions.UpdateOwnProfile,)


SEARCH FUNCTIONALITY
from rest_framework import filters
override variable as below
filter_backends = (filers.SearchFilter,)
search_fields = ('name', 'email',)

url changed for filter
http://127.0.0.1:8000/api/profile/?search=StringWantToSearch HTTP GET request

USER LOGIN API VIEW - UserLoginApiView
extends ObtainAuthToken
to add log in api we can use auth token view from djangorestframework

from rest_framework.authtoken.views import ObtainAuthToken # to get authentication token
from rest_framework.settings import api_settings

ObtainAuthToken is not enabled in browsable admin site
so we need to override this class and customize it so its visible in browsable api so it makes it easier for us.
override as below
renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
it adds the renderer classes to our obtain auth token view, which will enable it in the Django Admin

add url to enable this view

using login api we will get token, which we need to use for authentication in header of the request
Authorization 724dbdee50ac9ccb21bd3d58d40a5eaad775a81a
___________________________________________________________________________________________________________________

USER PROFILE FEED ITEMS

Creating a new feed ITEMS
	logged in user only
Updating feed items
	logged in user only
Deleting profile feed items
	logged in user only
Viewing other profile status updates
	All users

API URLS
/api/feed/ 									- list all feed items
														-	GET (list feed items)
														- POST (create feed item for logged in user)
/api/feed/<feed_item_id>/		- Manage specific feed items
														- GET (get the details of a specific feed item)
														- PUT/PATCH (update the feed item)
														- DELETE (deleting the feed item)

_________________________________________________________________________________________________________________
from django.conf import settings
to get the settings of the project

we need to use foreign key
    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete= models.CASCADE
    )

Serializer

_______________________________________________________________________________________________________________
Deploy it on aws

Services -> EC2 -> KeyPair -> Import Key -> Paste Public key

when aws create an instance the port is 82 for ssh access
We need to open port 80 so that we can connect to web server once we create it.
Services -> EC2 -> create Instance -> Ubuntu Server 18.04 -> select -> Configure -> Configure Security group -> Add HTTP -> Review





apt-get install -y python3-dev python3-venv sqlite python-pip supervisor nginx git

git for version control and clone the project
python3-venv for python virtual environment
nginx is the web server that is going to serve the static files and act as a proxy to our uWISGI service that is going to run in supervisor

$PROJECT_BASE_PATH/env/bin/pip install uwsgi==2.0.18
uwsgi is python daemon for running python code as a webserver


collectstatic will gather all of the static files for all of the apps in our project into one.
when you use django development server it will do this automatically for you
$PROJECT_BASE_PATH/env/bin/python manage.py collectstatic --noinput

but we will not be using django development server on production we need to create a location with all of the static files that we can use to serve the css and JavaScript for the django admin and django rest framework browsable api.

Supervisor is a application on linux that allows you to manage processes. this is what's going to manage our python process or uwsgi server

reread to update the supervisor
update to update all the processes
next we restart our profiles api


we will use setup.sh once and then we will use update.sh whenever we changes the code.

DEBUG = bool(int(os.environ.get('DEBUG', 1))) # commenting coz deploying to aws
#env is there in supervisor_profiles_api


To change the permissions of executable files
$ chmod +x deploy/*.sh

we need Public IPv4 DNS to ssh to aws instance

ssh ubuntu@ec2-18-116-203-66.us-east-2.compute.amazonaws.com

here ubantu is the user.

to run setup file we need to take url of raw file
https://raw.githubusercontent.com/shubhamshah207/udemy_profile-rest-api/main/deploy/setup.sh

curl -sL https://raw.githubusercontent.com/shubhamshah207/udemy_profile-rest-api/main/deploy/setup.sh | sudo bash -

curl to download the file and then passes it into sudo bash
curl used to retrieve contents from a url so its basically a http client in linux
-s is for running it in silent mode. Meaning it wont update us with all of the steps white downloading the file.
L is for following redirects.
sudo is used to run command as administartor
bash is what we are going to use to run our script
- is used to signal the end of the options provided for bash. so that it knows anything we pass in is to be ran on bash.

when we paste Public IPv4 DNS url to browser we will get error 400. That is because we haven't added the host name to the allowed hosts on our settings.py

to fix bad request error
ALLOWED_HOSTS allows us to enable access via specific domain names.
Its a security feature to make sure if somebody just finds a random ip address for our server they cant access the application unless they use the valid hostname
