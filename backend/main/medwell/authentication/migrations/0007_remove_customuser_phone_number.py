# Generated by Django 4.2 on 2024-10-26 16:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_remove_customuser_profile_pic_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='phone_number',
        ),
    ]
