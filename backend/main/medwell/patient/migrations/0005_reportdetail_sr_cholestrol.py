# Generated by Django 4.2 on 2024-09-29 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0004_remove_reportdetail_summary_report_summary'),
    ]

    operations = [
        migrations.AddField(
            model_name='reportdetail',
            name='sr_cholestrol',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
