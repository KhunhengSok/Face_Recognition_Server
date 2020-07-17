# Generated by Django 3.0.3 on 2020-07-17 10:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('birth_of_date', models.DateField(blank=True, null=True)),
                ('position', models.CharField(max_length=64)),
                ('department', models.CharField(max_length=64)),
                ('role', models.CharField(choices=[('member', 'Member'), ('admin', 'Admin')], default='member', max_length=8)),
                ('email', models.CharField(max_length=64, null=True)),
                ('employed_date', models.DateField(null=True)),
                ('profile_url', models.TextField(null=True)),
                ('created_at', models.DateTimeField(editable=False, null=True)),
                ('updated_at', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=64)),
                ('last_name', models.CharField(max_length=64)),
                ('created_at', models.DateTimeField(editable=False, null=True)),
                ('update_at', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('created_at', models.DateTimeField(editable=False, null=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='organization', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FaceEmbedding',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('face_embedding', models.TextField()),
                ('image_url', models.TextField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='face', to='face_embedding.Employee')),
            ],
        ),
        migrations.CreateModel(
            name='EventTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('repeated_every', models.BigIntegerField(default=None)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_template', to=settings.AUTH_USER_MODEL)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_template', to='face_embedding.Organization')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('date', models.DateField()),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('attendees', models.ManyToManyField(related_name='event', to='face_embedding.Employee')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event', to=settings.AUTH_USER_MODEL)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event', to='face_embedding.Organization')),
            ],
        ),
        migrations.AddField(
            model_name='employee',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employee', to='face_embedding.Organization'),
        ),
    ]
