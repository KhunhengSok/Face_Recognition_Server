# Generated by Django 3.0.8 on 2020-07-18 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('face_embedding', '0004_auto_20200719_0109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventtemplate',
            name='end_time',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='eventtemplate',
            name='start_time',
            field=models.TimeField(),
        ),
    ]
