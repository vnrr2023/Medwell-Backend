# Generated by Django 4.2 on 2025-01-31 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0006_doctorprofile_education'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctoraddress',
            name='timings',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
