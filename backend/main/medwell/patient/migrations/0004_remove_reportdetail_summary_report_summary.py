# Generated by Django 4.2 on 2024-09-29 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0003_report_report_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reportdetail',
            name='summary',
        ),
        migrations.AddField(
            model_name='report',
            name='summary',
            field=models.TextField(blank=True, null=True),
        ),
    ]
