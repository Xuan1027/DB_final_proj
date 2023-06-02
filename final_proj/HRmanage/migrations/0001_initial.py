# Generated by Django 4.2.1 on 2023-05-31 15:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('job', models.CharField(max_length=40)),
                ('esti_num', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('ID', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('gender', models.CharField(max_length=1)),
                ('hire_date', models.DateField()),
                ('address', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=10)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HRmanage.department')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_title', to='HRmanage.department')),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upload_file', models.FileField(upload_to='file/')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('name', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('principal', models.CharField(max_length=10)),
                ('deadline', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Salary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.CharField(max_length=7)),
                ('basic', models.IntegerField()),
                ('overtime', models.IntegerField()),
                ('miscellaneous', models.IntegerField()),
                ('ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HRmanage.employee')),
            ],
        ),
        migrations.CreateModel(
            name='DayOff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.CharField(max_length=4)),
                ('RestDay', models.IntegerField()),
                ('ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HRmanage.employee')),
            ],
        ),
        migrations.CreateModel(
            name='CheckIn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('checkin', models.DateTimeField()),
                ('checkout', models.DateTimeField()),
                ('ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HRmanage.employee')),
            ],
        ),
    ]