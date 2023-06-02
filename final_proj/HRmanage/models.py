from django.db import models


# Create your models here.
class Employee(models.Model):
    ID = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=30)
    department = models.ForeignKey("Department", on_delete=models.CASCADE)
    job = models.ForeignKey(
        "Department", related_name="job_title", on_delete=models.CASCADE
    )
    gender = models.CharField(max_length=1)
    hire_date = models.DateField()
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10)


class DayOff(models.Model):
    ID = models.ForeignKey("Employee", on_delete=models.CASCADE)
    year = models.CharField(max_length=4)
    RestDay = models.IntegerField()


class DayOffDep(models.Model):
    year = models.IntegerField(primary_key=True)
    RestDay = models.IntegerField()


class Department(models.Model):
    name = models.CharField(max_length=40)
    job = models.CharField(max_length=40)
    esti_num = models.IntegerField()


class Salary(models.Model):
    ID = models.ForeignKey("Employee", on_delete=models.CASCADE)
    month = models.DateField()
    basic = models.IntegerField()
    overtime = models.IntegerField()
    miscellaneous = models.IntegerField()


class CheckIn(models.Model):
    ID = models.ForeignKey("Employee", on_delete=models.CASCADE)
    date = models.DateField()
    checkin = models.TimeField()
    checkout = models.TimeField()


class Project(models.Model):
    name = models.CharField(max_length=20, primary_key=True)
    principal = models.ForeignKey("Employee", on_delete=models.CASCADE)
    deadline = models.DateField()


# class File(models.Model):
#     upload_file = models.FileField(upload_to='file/')
