# Generated by Django 4.2 on 2025-02-02 14:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('doctor', '0011_appointmentslot_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceMarketting',
            fields=[
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('html', models.TextField(blank=True, null=True)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
