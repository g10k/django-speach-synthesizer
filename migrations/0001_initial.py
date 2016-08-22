# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-26 13:43
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SoundFile',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('file', models.FileField(upload_to='/home/telminov/github/voice-synthesizer/generated')),
                ('text', models.TextField()),
                ('command', models.CharField(blank=True, max_length=255)),
            ],
        ),
    ]