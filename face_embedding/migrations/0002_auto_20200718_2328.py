# Generated by Django 3.0.8 on 2020-07-18 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('face_embedding', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='end_time',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_time',
            field=models.TimeField(),
        ),
    ]
