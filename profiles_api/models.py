from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings


class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, email, name, password=None):
        """Create a new user profile"""
        if not email:
            raise ValueError('Users much have an email address')

        # normalizing email meaning second half of the email it will convert to lower case.
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        # password will be saved in an encrypted manner. (hashed password)
        user.set_password(password)

        #specify the database you want to use. django can support multiple databases.
        user.save(using=self._db)

        return user


    def create_superuser(self, email, name, password):
        """Create and save a new superuser with given details"""
        user = self.create_user(email, name=name, password=password)

        # automatically created by PermissionMixin
        user.is_superuser = True

        user.is_staff = True
        user.save(using=self._db)

        return user

class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)

    # is it an active user or not. We can mark some users inactive.
    is_active = models.BooleanField(default=True)

    # if the user is staff member or not
    is_staff = models.BooleanField(default=False)

    #manager is required to manage users for instance create user, modify user, etc.
    objects = UserProfileManager()

    # to override the defaults
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    # custom methods to get custom fields integrate with djnago
    def get_full_name(self):
        """Retrieve full name of user"""
        return self.name

    # give ability to django to get this details
    def get_short_name(self):
        """Retrieve short name of user"""
        return self.name

    # executed when the object is printed...
    def __str__(self):
        """Return string representation of our user"""
        return self.email

class ProfileFeedItem(models.Model):
    """Profile status update"""
    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete= models.CASCADE
    )
    status_text = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True) # automatically give the creation time

    def __str__(self):
        """Return the model as a string"""
        return self.status_text
