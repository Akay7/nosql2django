from django.db import models


class User(models.Model):
    nick_name = models.CharField(max_length=256)

    def __str__(self):
        return self.nick_name


class Tag(models.Model):
    title = models.CharField(max_length=256)

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=256)
    summary = models.TextField()
    updated = models.DateTimeField()
    author = models.ForeignKey(User, related_name='posts')
    tags = models.ManyToManyField(Tag, related_name='posts')

    def __str__(self):
        return self.title
