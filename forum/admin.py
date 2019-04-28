from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Section

admin.site.register(User, UserAdmin)
admin.site.register(Section)
