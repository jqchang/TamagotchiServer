# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-22 22:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mapserver', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batch',
            name='berries',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='batch', to='mapserver.Berry'),
        ),
    ]
