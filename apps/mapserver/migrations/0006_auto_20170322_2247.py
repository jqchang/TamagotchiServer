# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-22 22:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mapserver', '0005_auto_20170322_2227'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='batch',
            name='berries',
        ),
        migrations.AddField(
            model_name='berry',
            name='batch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='berries', to='mapserver.Batch'),
        ),
        migrations.AddField(
            model_name='berry',
            name='color',
            field=models.IntegerField(default=0),
        ),
    ]