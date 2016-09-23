# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog_engine', '0008_auto_20160915_0411'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='short_descripcion',
            new_name='short_description',
        ),
        migrations.RenameField(
            model_name='tag',
            old_name='short_descripcion',
            new_name='short_description',
        ),
    ]
