from django.shortcuts import render
from .handle import *


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
        handle_DayOffDep(request.FILES["DayOffDep"])

    if Department.is_valid():
        handle_Department(request.FILES["Department"])

    if Employee.is_valid():
        handle_Employee(request.FILES["Employee"])

    if DayOff.is_valid():
        handle_DayOff(request.FILES["DayOff"])

    if CheckIn.is_valid():
        handle_CheckIn(request.FILES["CheckIn"])

    if Project.is_valid():
        handle_Project(request.FILES["Project"])

    if Salary.is_valid():
        handle_Salary(request.FILES["Salary"])


def employee_evaluation(request):
    if request.method != "POST":
        return render(request, "HRmanage/employee_evaluation/index.html")

    if not query_id_valid(request.POST["query_id"]):
        return render(request, "HRmanage/employee_evaluation.html")
    worktime = handle_employee_evaluation_worktime(request.POST["query_id"])
    projects = handle_employee_evaluation_project(request.POST["query_id"])
    context = {
        "worktime": worktime,
        "projects": projects,
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

    if not query_pay_ratio_valid(request.POST["pay_ratio"]):
        return render(request, "HRmanage/overtime_pay/index.html")

    result = handle_overtime_pay_query(request.POST)
    result["overtime_pay"] = int(result.get("overtime")) * int(
        request.POST["pay_ratio"]
    )
    return render(request, "HRmanage/overtime_pay/result.html", context=result)


def vacancies(request):
    if request.method != "POST":
        return render(request, "HRmanage/vacancies/index.html")

    result = handle_vacancies()
    context = {"department": result}
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
