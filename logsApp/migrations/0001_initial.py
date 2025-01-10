<<<<<<< HEAD
# Generated by Django 5.1.1 on 2025-01-04 15:59
=======
# Generated by Django 5.1.2 on 2025-01-05 07:28
>>>>>>> 5a276268bfc23f779f5a7629ffe6bfc6ad0b957c

import django.db.models.deletion
import logsApp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmployesInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('EmpHaveCar', models.BooleanField(default=False)),
                ('ceoNumber', models.CharField(default='0', max_length=100, unique=True)),
                ('ceoName', models.CharField(max_length=100)),
                ('phoneNumber', models.CharField(default='0000000000', max_length=100)),
                ('position', models.CharField(default='الوظيفه', max_length=100)),
                ('section', models.CharField(default='القسم', max_length=100)),
                ('email', models.EmailField(default='example@example.com', max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='RegistredCars',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('carYear', models.IntegerField(null=True)),
                ('cownerEmpNumber', models.IntegerField(null=True)),
                ('cownerName', models.TextField(null=True)),
                ('cownerPhone', models.TextField(null=True)),
                ('section', models.TextField(null=True)),
                ('carNumber', models.TextField(default='0')),
                ('vType', models.TextField(max_length=100, null=True)),
                ('carIsInparking', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='FinesAccidents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('report_date', models.DateField(blank=True, null=True)),
                ('fixin_date', models.DateField(blank=True, null=True)),
                ('report_pdf_file', models.FileField(blank=True, max_length=500, null=True, upload_to=logsApp.models.fines_accident_pdf_upload_to)),
                ('car_paperwork_file', models.FileField(blank=True, max_length=500, null=True, upload_to=logsApp.models.fines_accident_pdf_upload_to)),
                ('employees', models.ManyToManyField(blank=True, to='logsApp.employesinfo')),
<<<<<<< HEAD
                ('car', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='finess', to='logsApp.registredcars')),
=======
                ('car', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='logsApp.registredcars')),
>>>>>>> 5a276268bfc23f779f5a7629ffe6bfc6ad0b957c
            ],
        ),
        migrations.CreateModel(
            name='FinesAccidentsImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=logsApp.models.fines_accident_file_upload_to)),
                ('fines_accident', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='logsApp.finesaccidents')),
            ],
        ),
        migrations.CreateModel(
            name='LicenseFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=logsApp.models.fines_accident_file_upload_to)),
                ('fines_accident', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='license_files', to='logsApp.finesaccidents')),
            ],
        ),
        migrations.CreateModel(
            name='LogsC',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('carIsInUse', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('ended_at', models.DateTimeField(blank=True, null=True)),
                ('return_date', models.DateField(blank=True, null=True)),
                ('return_time', models.TimeField(blank=True, null=True)),
                ('carNote', models.TextField(blank=True, null=True)),
                ('taken_date', models.DateField(blank=True, null=True)),
                ('taken_time', models.TimeField(blank=True, null=True)),
                ('Logs_employee_ins', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='logsApp.employesinfo')),
                ('Logs_car_ins', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='logsApp.registredcars')),
            ],
        ),
        migrations.CreateModel(
            name='InUseCars',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='logsApp.employesinfo')),
                ('logsc_ley', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='logsApp.logsc')),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='logsApp.registredcars')),
            ],
        ),
<<<<<<< HEAD
=======

>>>>>>> 5a276268bfc23f779f5a7629ffe6bfc6ad0b957c
        migrations.AddIndex(
            model_name='logsc',
            index=models.Index(fields=['Logs_employee_ins', 'carIsInUse'], name='logsApp_log_Logs_em_1a66d2_idx'),
        ),
        migrations.AddIndex(
            model_name='logsc',
            index=models.Index(fields=['Logs_car_ins', 'carIsInUse'], name='logsApp_log_Logs_ca_ec6033_idx'),
        ),
        migrations.AddIndex(
            model_name='logsc',
            index=models.Index(fields=['created_at'], name='logsApp_log_created_d07337_idx'),
        ),
        migrations.AddIndex(
            model_name='logsc',
            index=models.Index(fields=['ended_at'], name='logsApp_log_ended_a_476991_idx'),
        ),
    ]
