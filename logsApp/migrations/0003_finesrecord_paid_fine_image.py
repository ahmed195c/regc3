# Generated by Django 5.1.2 on 2025-01-08 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logsApp', '0002_finesrecord'),
    ]

    operations = [
        migrations.AddField(
            model_name='finesrecord',
            name='paid_fine_image',
            field=models.ImageField(blank=True, null=True, upload_to='paid_fines/'),
        ),
    ]
