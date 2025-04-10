# Generated by Django 4.2 on 2024-11-03 12:02

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
            name='DoctorProfile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=400)),
                ('phone_number', models.CharField(max_length=12)),
                ('age', models.CharField(blank=True, max_length=4, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('state', models.CharField(blank=True, max_length=100, null=True)),
                ('pin', models.CharField(blank=True, max_length=10, null=True)),
                ('dob', models.DateField(blank=True, null=True)),
                ('verified', models.BooleanField(default=False)),
                ('profile_qr', models.CharField(blank=True, max_length=500, null=True)),
                ('registeration_number', models.CharField(blank=True, max_length=300, null=True)),
                ('adhaar_card', models.FileField(blank=True, null=True, upload_to='doctors_adhaar_card/')),
                ('registeration_card_image', models.FileField(blank=True, null=True, upload_to='reg_cards/')),
                ('passport_size_image', models.FileField(blank=True, null=True, upload_to='doctor_images/')),
                ('profile_pic', models.FileField(default='profile_pics/default_pp.jpg', upload_to='profilepics/')),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
