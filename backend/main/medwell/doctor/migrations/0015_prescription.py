# Generated by Django 4.2 on 2025-03-16 12:43

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0014_servicemarketting_customer_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prescription',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('other_info', models.TextField(blank=True, null=True)),
                ('prescription', models.JSONField(blank=True, null=True)),
                ('appointment', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='doctor.appointment')),
            ],
        ),
    ]
