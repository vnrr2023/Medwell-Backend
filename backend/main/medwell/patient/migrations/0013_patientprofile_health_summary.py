# Generated by Django 4.2 on 2024-10-31 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0012_alter_patientprofile_profile_qr'),
    ]

    operations = [
        migrations.AddField(
            model_name='patientprofile',
            name='health_summary',
            field=models.TextField(default=' '),
        ),
    ]
