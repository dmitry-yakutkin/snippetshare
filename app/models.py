import os

from django.db import models
from django.contrib.auth.models import User

from django.conf import settings


class Message(models.Model):
    user = models.ForeignKey(User)
    text = models.CharField(max_length=150)
    date = models.DateTimeField(auto_now_add=True)


class Snippet(models.Model):
    LANGUAGES = (
        ('python', 'Python'),
        ('go', 'Golang'),
        ('javascript', 'Javascript'),
        ('ruby', 'Ruby'),
        ('htmlmixed', 'HTML'),
    )
    text = models.CharField(max_length=10000)
    language = models.CharField(
        max_length=2, choices=LANGUAGES, null=True, blank=True)
    user = models.ForeignKey(User)

    @property
    def language_image_url(self):
        for l in self.LANGUAGES:
            print(os.path.join('/static/images/',  l[0] + '.png'))
            if l[0] == self.language:

                return os.path.join(settings.MEDIA_URL, '/static/images/',  l[0] + '.png')


class Review(models.Model):
    snippet = models.ForeignKey(Snippet)
    user = models.ForeignKey(User)
    rating = models.IntegerField()


class Comment(models.Model):
    snippet = models.ForeignKey(Snippet)
    user = models.ForeignKey(User)
    text = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now_add=True)
