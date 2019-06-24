"""forum URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('sections/<section_id>/threads', views.threads),
    path('threads/<thread_id>', views.show_thread),
    path('threads/<thread_id>/post', views.post_reply),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register', views.register),
    path('edit/<post_id>', views.post_edit),
    path('edit/<post_id>/go', views.post_edit_go),
    path('delete/<delete_id>', views.post_delete),
    path('deleteThread', views.delete_thread),
    path('u/<userid>', views.user),
    path('deactivate', views.deactivate),
    path('upvote', views.post_upvote),
    path('search', views.search),
    path('adminpan', views.admin_panel)
]
