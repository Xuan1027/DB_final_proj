from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Employee)
admin.site.register(DayOff)
admin.site.register(DayOffDep)
admin.site.register(Department)
admin.site.register(Salary)
admin.site.register(CheckIn)
admin.site.register(Project)
