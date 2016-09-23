from django.contrib import admin

from . import models as blog_engine_models
# Register your models here.
admin.site.register(blog_engine_models.Post)
admin.site.register(blog_engine_models.Tag)
admin.site.register(blog_engine_models.Theme)
