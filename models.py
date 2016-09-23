from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import models as auth_models
# Create your models here.


class Tag(models.Model):
    name = models.CharField(
        max_length=100,
    )

    short_description = models.TextField()

    slug = models.SlugField(blank=True, unique=True)

    def __unicode__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(
        max_length=250,
    )

    slug = models.SlugField(blank=True, unique=True)

    short_description = models.TextField()

    body = models.TextField(

    )

    body_markdown = models.TextField(
    )

    author = models.ForeignKey(
        auth_models.User,
    )

    tags = models.ManyToManyField(
        Tag,
        blank=True
    )

    visible = models.BooleanField(
        default=True
    )

    removed = models.BooleanField(
        default=False
    )

    created = models.DateTimeField(
        auto_now_add=True,
    )

    modified = models.DateTimeField(
        auto_now=True,
    )

    def __unicode__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
    )

    comment = models.TextField(
    )

    author = models.ForeignKey(
        auth_models.User,
    )


class ReplyToComment(models.Model):
    comment = models.ForeignKey(
        Comment,
    )

    reply_comment = models.TextField(
    )

    author = models.ForeignKey(
        auth_models.User,
    )


class Theme(models.Model):
    name = models.CharField(
        max_length=100
    )

    selected = models.BooleanField(
        default=False
    )
    folder = models.CharField(
        max_length=20
    )

    def __unicode__(self):
        return self.name