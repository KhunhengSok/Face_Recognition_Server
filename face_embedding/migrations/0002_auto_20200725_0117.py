# Generated by Django 3.0.8 on 2020-07-24 18:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('face_embedding', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee_event',
            name='attend_time',
            field=models.TimeField(default=datetime.datetime(2020, 7, 25, 1, 17, 12, 646808), editable=False),
        ),
        migrations.AlterField(
            model_name='faceembedding',
            name='face_embedding',
            field=models.TextField(editable=False),
        ),
        migrations.AlterField(
            model_name='faceembedding',
            name='image_url',
            field=models.TextField(editable=False),
        ),
    ]
