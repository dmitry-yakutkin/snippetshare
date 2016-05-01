from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    user = models.ForeignKey(User)
    text = models.CharField(max_length=150)
    date = models.DateTimeField(auto_now_add=True)


class Snippet(models.Model):
    LANGUAGES = (
        ('PY', 'Python'),
        ('JS', 'Javascript'),
    )
    text = models.CharField(max_length=10000)
    languages = models.CharField(max_length=2, choices=LANGUAGES)
    user = models.ForeignKey(User)


class Review(models.Model):
    snippet = models.ForeignKey(Snippet)
    user = models.ForeignKey(User)
    rating = models.IntegerField()


class Comment(models.Model):
    snippet = models.ForeignKey(Snippet)
    user = models.ForeignKey(User)
    text = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now_add=True)
