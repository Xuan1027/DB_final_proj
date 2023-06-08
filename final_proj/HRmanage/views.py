from django.shortcuts import render
from .handle import *
from .forms import *


# Create your views here.
def index(request):
    if request.method != "POST":
        return render(
            request,
            "HRmanage/upload_page/index.html",
        )

    DayOffDep = Upload_DayOffDep(request.POST, request.FILES)
    DayOff = Upload_DayOff(request.POST, request.FILES)
    CheckIn = Upload_CheckIn(request.POST, request.FILES)
    Department = Upload_Department(request.POST, request.FILES)
    Employee = Upload_Employee(request.POST, request.FILES)
    Project = Upload_Project(request.POST, request.FILES)
    Salary = Upload_Salary(request.POST, request.FILES)

    if DayOffDep.is_valid():
        print("DayOffDep is valid")
        handle_DayOffDep(request.FILES["DayOffDep"])

    if Department.is_valid():
        print("Department is valid")
        handle_Department(request.FILES["Department"])

    if Employee.is_valid():
        print("Employee is valid")
        handle_Employee(request.FILES["Employee"])

    if DayOff.is_valid():
        print("DayOff is valid")
        handle_DayOff(request.FILES["DayOff"])

    if CheckIn.is_valid():
        print("CheckIn is valid")
        handle_CheckIn(request.FILES["CheckIn"])

    if Project.is_valid():
        print("Project is valid")
        handle_Project(request.FILES["Project"])

    if Salary.is_valid():
        print("Salary is valid")
        handle_Salary(request.FILES["Salary"])

    return render(
        request,
        "HRmanage/upload_page/index.html",
    )


def employee_evaluation(request):
    if request.method != "POST":
        return render(request, "HRmanage/employee_evaluation/index.html")

    if not query_id_valid(request.POST["query_id"]):
        return render(request, "HRmanage/employee_evaluation/index.html")
    worktime = handle_employee_evaluation_worktime(request.POST["query_id"])
    projects = handle_employee_evaluation_project(request.POST["query_id"])
    try:
        info = Employee.objects.get(ID=request.POST["query_id"])
    except Employee.DoesNotExist:
        pass
    context = {
        "worktime": worktime,
        "projects": projects,
        "person": info,
    }
    return render(request, "HRmanage/employee_evaluation/result.html", context)


def overtime_pay(request):
    if request.method != "POST":
        return render(request, "HRmanage/overtime_pay/index.html")

    if not query_id_valid(request.POST["query_id"]):
        return render(request, "HRmanage/overtime_pay/index.html")

    if not query_year_valid(request.POST["query_year"]):
        return render(request, "HRmanage/overtime_pay/index.html")

    if not query_month_valid(request.POST["query_month"]):
        return render(request, "HRmanage/overtime_pay/index.html")

    # if not query_pay_ratio_valid(request.POST["pay_ratio"]):
    #     return render(request, "HRmanage/overtime_pay/index.html")

    try:
        info = Employee.objects.get(ID=request.POST["query_id"])
    except Employee.DoesNotExist:
        pass

    basic_salary = handle_overtime_pay_basic_salary(request.POST)
    result = handle_overtime_pay_query(request.POST)

    result["overtime_pay"] = int(result.get("overtime")) * int(basic_salary / 180)
    result["person"] = info

    # result["overtime_pay"] = int(result.get("overtime")) * int(
    #     request.POST["pay_ratio"]
    # )

    return render(request, "HRmanage/overtime_pay/result.html", context=result)


def vacancies(request):
    queryset = Department.objects.values("name").distinct()
    context = {"departments": queryset}
    if request.method != "POST":
        return render(request, "HRmanage/vacancies/index.html", context)

    result = handle_vacancies(request.POST)
    result = handle_basic_salary_range(result)
    context["department"] = result
    context["query_dep"] = request.POST["query_dep"]
    return render(request, "HRmanage/vacancies/result.html", context)


def spacial_holiday(request):
    if request.method != "POST":
        return render(request, "HRmanage/spacial_holiday/index.html")

    if not query_id_valid(request.POST["query_id"]):
        return render(request, "HRmanage/spacial_holiday/index.html")

    if not query_year_valid(request.POST["query_year"]):
        return render(request, "HRmanage/spacial_holiday/index.html")

    context = handle_spacial_holiday(request.POST)
    return render(request, "HRmanage/spacial_holiday/result.html", context)


def participation(request):
    queryset = Department.objects.values("name").distinct()
    context = {"departments": queryset}
    if request.method != "POST":
        return render(request, "HRmanage/participation/index.html", context)

    result = handle_participation(request.POST["query_dep"])
    context["result"] = result
    context["dep_choice"] = request.POST["query_dep"]
    return render(request, "HRmanage/participation/result.html", context)
