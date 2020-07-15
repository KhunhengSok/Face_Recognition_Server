# Generated by Django 3.0.3 on 2020-07-14 19:43

from django.db import migrations, models
import django.db.models.deletion
from face_embedding.models import Organization


class Migration(migrations.Migration):

    dependencies = [
        ('face_embedding', '0009_auto_20200715_0127'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='person',
        ),
        migrations.AddField(
            model_name='employee',
            name='birth_of_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='created_at',
            field=models.DateTimeField(editable=False, null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='name',
            field=models.CharField(default='Khunheng', max_length=64),
        ),
        migrations.AddField(
            model_name='employee',
            name='organization',
            field=models.ForeignKey(default=Organization.objects.first().id, on_delete=django.db.models.deletion.CASCADE, related_name='Employee', to='face_embedding.Organization'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='employee',
            name='update_at',
            field=models.DateTimeField(null=True),
        ),
    ]
