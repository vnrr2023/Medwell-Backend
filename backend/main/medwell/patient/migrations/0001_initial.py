# Generated by Django 4.2 on 2024-09-27 19:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PatientProfile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('age', models.CharField(blank=True, max_length=5, null=True)),
                ('blood_group', models.CharField(blank=True, max_length=10, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('state', models.CharField(blank=True, max_length=100, null=True)),
                ('pin', models.CharField(blank=True, max_length=10, null=True)),
                ('profile_pic', models.FileField(blank=True, null=True, upload_to='profilepics/')),
                ('profile_qr', models.FileField(blank=True, null=True, upload_to='user_qrs/')),
                ('adhaar_card', models.FileField(blank=True, null=True, upload_to='addhaar_cards/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
