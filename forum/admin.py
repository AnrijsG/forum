from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Section, Thread, Post

admin.site.register(User, UserAdmin)
admin.site.register(Section)
admin.site.register(Thread)
admin.site.register(Post)

