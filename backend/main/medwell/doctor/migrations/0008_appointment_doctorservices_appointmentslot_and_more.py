# Generated by Django 4.2 on 2025-01-31 06:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('doctor', '0007_doctoraddress_timings'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booked_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DoctorServices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_name', models.CharField(blank=True, max_length=300, null=True)),
                ('service_amount', models.CharField(blank=True, max_length=100, null=True)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AppointmentSlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timing', models.CharField(blank=True, max_length=200, null=True)),
                ('status', models.CharField(blank=True, max_length=200, null=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointment_slots', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AppointmentPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.CharField(blank=True, max_length=100, null=True)),
                ('payment_method', models.CharField(blank=True, max_length=200, null=True)),
                ('transaction_id', models.CharField(blank=True, max_length=200, null=True)),
                ('appointment', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='doctor.appointment')),
            ],
        ),
        migrations.AddField(
            model_name='appointment',
            name='appointment_slot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doctor.appointmentslot'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='appointment',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments_as_patient', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='appointment',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doctor.doctorservices'),
        ),
    ]
