from django.contrib import admin
from .models import DataSchema, User, Column
from django.contrib.auth import get_user_model

# Register your models here.
admin.site.register(DataSchema)
admin.site.register(Column)
admin.site.register(User)
