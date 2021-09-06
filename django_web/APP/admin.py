from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Database_users)
admin.site.register(Destination)


