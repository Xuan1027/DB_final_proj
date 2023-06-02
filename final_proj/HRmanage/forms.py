from django import forms


class Upload_Employee(forms.Form):
    Employee = forms.FileField()

class Upload_DayOff(forms.Form):
    DayOff = forms.FileField()

class Upload_DayOffDep(forms.Form):
    DayOffDep = forms.FileField()

class Upload_Department(forms.Form):
    Department = forms.FileField()

class Upload_Salary(forms.Form):
    Salary = forms.FileField()

class Upload_CheckIn(forms.Form):
    CheckIn = forms.FileField()

class Upload_Project(forms.Form):
    Project = forms.FileField()
