# Generated by Django 4.2.1 on 2023-06-01 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HRmanage', '0003_dayoffdep_alter_checkin_checkin_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salary',
            name='month',
            field=models.DateField(),
        ),
    ]
