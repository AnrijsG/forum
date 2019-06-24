from django.contrib.auth.models import AbstractUser, Group
from django.db import models


class User(AbstractUser):
    dark_mode = models.BooleanField(default=False)


class UserGroup(Group):
    pass


class Section(models.Model):
    title = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.title


class Thread(models.Model):
    title = models.CharField(max_length=150)
    section = models.ForeignKey(to=Section, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Post(models.Model):
    thread = models.ForeignKey(to=Thread, on_delete=models.CASCADE)
    author = models.ForeignKey(to=User, on_delete=models.DO_NOTHING)
    text = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    last_edited_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text


class Upvote(models.Model):
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.DO_NOTHING)


class LogItem(models.Model):
    INSERTED = 'INS'
    UPDATED = 'UPD'
    DELETED = 'DEL'

    ACTION_CHOICES = [
        (INSERTED, 'Inserted'),
        (UPDATED, 'Updated'),
        (DELETED, 'Deleted')
    ]

    action = models.CharField(max_length=3, choices=ACTION_CHOICES)
    user = models.ForeignKey(to=User, on_delete=models.DO_NOTHING)
    table = models.CharField(max_length=255)
    old_value = models.TextField(null=True)
    new_value = models.TextField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
