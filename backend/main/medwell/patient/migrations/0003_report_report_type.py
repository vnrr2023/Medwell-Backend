# Generated by Django 4.2 on 2024-09-29 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0002_report_reportdetail'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='report_type',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
