# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog_engine', '0007_theme'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='short_descripcion',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tag',
            name='short_descripcion',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
