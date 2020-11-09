from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ('username',)

class Group(models.Model):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(User)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)