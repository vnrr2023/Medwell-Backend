# Generated by Django 4.2 on 2024-10-26 14:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0008_patientprofile_allergies_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='patientprofile',
            old_name='family_hsitory',
            new_name='family_history',
        ),
    ]
