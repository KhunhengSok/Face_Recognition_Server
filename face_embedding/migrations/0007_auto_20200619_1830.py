# Generated by Django 3.0.3 on 2020-06-19 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('face_embedding', '0006_auto_20200619_1737'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faceembedding',
            name='face_embedding',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='faceembedding',
            name='image_url',
            field=models.TextField(),
        ),
    ]
