from django.contrib import admin
from .models import *

# @admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    Legal_fields = ('id', 'name', 'department', 'job', 'gender', 'hire_date', 'address', 'phone_number')
    list_display = []
    for field in Employee._meta.get_fields():
        if field.name.lower() in Legal_fields:
            list_display.append(field.name)

    search_fields = ('name',)
    # print(list_display, type(list_display))


class DayOffAdmin(admin.ModelAdmin):
    Legal_fields = ('id', 'year', 'RestDay')
    Legal_fields = [name.lower() for name in Legal_fields]
    list_display = []
    for field in DayOff._meta.get_fields():
        if field.name.lower() in Legal_fields:
            list_display.append(field.name)
    list_display.remove('ID')

class DayOffDepAdmin(admin.ModelAdmin):
    Legal_fields = ('year', 'RestDay')
    Legal_fields = [name.lower() for name in Legal_fields]
    list_display = []
    for field in DayOff._meta.get_fields():
        if field.name.lower() in Legal_fields:
            list_display.append(field.name)
    
    search_fields = ('year',)
    # print(list_display, type(list_display))

class DepartmentAdmin(admin.ModelAdmin):
    Legal_fields = ('name', 'job', 'esti_num')
    list_display = []
    for field in Department._meta.get_fields():
        if field.name.lower() in Legal_fields:
            list_display.append(field.name)
            
    search_fields = ('name',)
    # print(list_display, type(list_display))

class SalaryAdmin(admin.ModelAdmin):
    Legal_fields = ('id', 'month', 'basic', 'overtime', 'miscellaneous')
    list_display = []
    for field in Salary._meta.get_fields():
        if field.name.lower() in Legal_fields:
            list_display.append(field.name)
    list_display.remove('ID')
    search_fields = ('name',)
    # print(list_display, type(list_display))

class CheckInAdmin(admin.ModelAdmin):
    Legal_fields = ('id', 'date', 'checkin', 'checkout')
    list_display = []
    for field in CheckIn._meta.get_fields():
        if field.name.lower() in Legal_fields:
            list_display.append(field.name)
    list_display.remove('ID')
    search_fields = ('id',)
    # print(list_display, type(list_display))

class ProjectAdmin(admin.ModelAdmin):
    Legal_fields = ('name', 'principal', 'deadline')
    list_display = []
    for field in Project._meta.get_fields():
        if field.name.lower() in Legal_fields:
            list_display.append(field.name)
            
    # search_fields = ('name',)
    # print(list_display, type(list_display))



# Register your models here.
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(DayOff, DayOffAdmin)
admin.site.register(DayOffDep, DayOffDepAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Salary, SalaryAdmin)
admin.site.register(CheckIn, CheckInAdmin)
admin.site.register(Project, ProjectAdmin)
