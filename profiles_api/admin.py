from django.contrib import admin

from profiles_api import models
# Register your models here.

# to register the user profile model to django admin
admin.site.register(models.UserProfile)
