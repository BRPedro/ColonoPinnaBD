# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-09 15:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TC_PATRON',
            fields=[
                ('idpatron', models.AutoField(primary_key=True, serialize=False)),
                ('xp', models.IntegerField(null=True)),
                ('yp', models.IntegerField(null=True)),
                ('contadorp', models.IntegerField(default=0)),
            ],
        ),
    ]