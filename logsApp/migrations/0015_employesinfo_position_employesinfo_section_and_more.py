# Generated by Django 5.1.1 on 2024-09-20 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logsApp', '0014_rename_carname_registredcars_vtype_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='employesinfo',
            name='position',
            field=models.TextField(default='الوظيفه'),
        ),
        migrations.AddField(
            model_name='employesinfo',
            name='section',
            field=models.TextField(default='القسم'),
        ),
        migrations.AlterField(
            model_name='employesinfo',
            name='phoneNumber',
            field=models.TextField(default='0000000000'),
        ),
    ]
