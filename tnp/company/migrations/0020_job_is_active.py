# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-27 15:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0019_job_added_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
