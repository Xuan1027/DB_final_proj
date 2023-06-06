from .forms import *
from .models import *
from datetime import datetime
from django.db.models.functions import TruncMonth
from django.db.models import F, Sum, Count, ExpressionWrapper, Max, Min

# import codecs
from io import TextIOWrapper
import csv
import random

def handle_csv(r):
    csv_file = TextIOWrapper(r, encoding="utf-8-sig")
    reader = csv.DictReader(csv_file)
    return reader


def handle_DayOffDep(f):
    needs = [
        "JOB_TENURE",
        "DAY_OFF",
    ]
    reader = handle_csv(f)
    if not all(field in reader.fieldnames for field in needs):
        return
    for row in reader:
        JOB_TENURE = int(row["JOB_TENURE"])
        DAY_OFF = int(row["DAY_OFF"])
        # print(JOB_TENURE, DAY_OFF)
        DayOffDep.objects.create(year=JOB_TENURE, RestDay=DAY_OFF)


def handle_DayOff(f):
    needs = [
        "ID",
        "YEAR",
        "DAY",
    ]
    reader = handle_csv(f)
    if not all(field in reader.fieldnames for field in needs):
        return
    for row in reader:
        ID = Employee.objects.get(ID=row["ID"])
        YEAR = row["YEAR"]
        DAY = int(row["DAY"])
        # print(ID, YEAR, DAY)
        DayOff.objects.create(ID=ID, year=YEAR, RestDay=DAY)


def handle_CheckIn(f):
    needs = [
        "ID",
        "DATE",
        "TIME_COME",
        "TIME_LEAVE",
    ]
    reader = handle_csv(f)
    if not all(field in reader.fieldnames for field in needs):
        return
    for row in reader:
        ID = Employee.objects.get(ID=row["ID"])
        DATE = row["DATE"]
        DATE = datetime.strptime(DATE, "%Y/%m/%d").date()
        TIME_COME = row["TIME_COME"]
        TIME_COME = datetime.strptime(TIME_COME, "%I:%M %p").time()
        TIME_LEAVE = row["TIME_LEAVE"]
        TIME_LEAVE = datetime.strptime(TIME_LEAVE, "%I:%M %p").time()
        # print(ID, DATE, TIME_COME, TIME_LEAVE)
        CheckIn.objects.create(ID=ID, date=DATE, checkin=TIME_COME, checkout=TIME_LEAVE)


def handle_Department(f):
    needs = [
        "DEPARTMENT",
        "JOB",
        "MEN_PREDICT",
    ]
    reader = handle_csv(f)
    if not all(field in reader.fieldnames for field in needs):
        return
    for row in reader:
        DEPARTMENT = row["DEPARTMENT"]
        JOB = row["JOB"]
        MEN_PREDICT = int(row["MEN_PREDICT"])
        # print(DEPARTMENT, JOB, MEN_PREDICT)
        Department.objects.create(name=DEPARTMENT, job=JOB, esti_num=MEN_PREDICT)


def handle_Employee(f):
    needs = [
        "ID",
        "NAME",
        "DEPARTMENT",
        "JOB",
        "GENDER",
        "HIRE_DATE",
        "ADDRESS",
        "PHONE",
    ]
    reader = handle_csv(f)
    if not all(field in reader.fieldnames for field in needs):
        return
    for row in reader:
        ID = row["ID"]
        NAME = row["NAME"]
        JOB = Department.objects.get(name=row["DEPARTMENT"], job=row["JOB"])
        DEPARTMENT = JOB
        GENDER = row["GENDER"][0]
        HIRE_DATE = row["HIRE_DATE"]
        HIRE_DATE = datetime.strptime(HIRE_DATE, "%Y/%m/%d").date()
        ADDRESS = row["ADDRESS"]
        PHONE = row["PHONE"]
        # print(ID, NAME, DEPARTMENT, JOB, GENDER, HIRE_DATE, ADDRESS, PHONE)
        Employee.objects.create(
            ID=ID,
            name=NAME,
            department=DEPARTMENT,
            job=JOB,
            gender=GENDER,
            hire_date=HIRE_DATE,
            address=ADDRESS,
            phone_number=PHONE,
        )


def handle_Project(f):
    needs = [
        "PROJ_NAME",
        "ID",
        "DATE",
    ]
    reader = handle_csv(f)
    if not all(field in reader.fieldnames for field in needs):
        return
    for row in reader:
        PROJ_NAME = row["PROJ_NAME"]
        ID = Employee.objects.get(ID=row["ID"])
        DATE = row["DATE"]
        DATE = datetime.strptime(DATE, "%Y/%m/%d").date()
        # print(PROJ_NAME, ID, DATE)
        Project.objects.create(name=PROJ_NAME, principal=ID, deadline=DATE)


def handle_Salary(f):
    needs = [
        "ID",
        "MONTH",
        "SALARY",
        "OVERTIME_PAY",
        "MISECELLANEOUS",
    ]
    reader = handle_csv(f)
    if not all(field in reader.fieldnames for field in needs):
        return
    for row in reader:
        ID = Employee.objects.get(ID=row["ID"])
        MONTH = "2022/" + row["MONTH"]
        MONTH = datetime.strptime(MONTH, "%Y/%m").replace(day=1).date()
        SALARY = int(row["SALARY"])
        OVERTIME_PAY = int(row["OVERTIME_PAY"])
        MISECELLANEOUS = int(row["MISECELLANEOUS"])
        # print(ID, MONTH, SALARY, OVERTIME_PAY, MISECELLANEOUS)
        Salary.objects.create(
            ID=ID,
            month=MONTH,
            basic=SALARY,
            overtime=OVERTIME_PAY,
            miscellaneous=MISECELLANEOUS,
        )


def query_id_valid(q):
    if not q.isdigit():
        return False
    if len(q) > 10:
        return False
    # print("id valid")
    return True


def query_month_valid(q):
    if not q.isdigit():
        return False
    if int(q) < 1 or int(q) > 12:
        return False
    # print("month valid")
    return True


def query_year_valid(q):
    if not q.isdigit():
        return False
    if len(q) > 4:
        return False
    # print("year valid")
    return True


def query_pay_ratio_valid(q):
    if not q.isdigit():
        return False
    return True


def handle_employee_evaluation_worktime(q):
    queryset = (
        CheckIn.objects.filter(ID=q)
        .annotate(time_delta=F("checkout") - F("checkin"))
        .values("date", "time_delta")
    )
    # queryset = queryset.annotate(
    #     month=TruncMonth("date"), time_diff=Sum("time_delta")
    # ).values("month", "time_diff")

    # for entry in queryset:
    #     print(entry["date"], entry["time_delta"])

    return queryset


def handle_employee_evaluation_project(q):
    queryset = Project.objects.filter(principal=q)
    return queryset


def handle_overtime_pay_query(q):
    queryset = handle_employee_evaluation_worktime(q["query_id"])
    queryset = queryset.filter(date__year=q["query_year"], date__month=q["query_month"])
    salary = Salary.objects.get(
        ID__ID=q["query_id"], month__year=q["query_year"], month__month=q["query_month"]
    )
    total_overtime = 0
    for entry in queryset:
        hour = int(entry["time_delta"].total_seconds() / 3600)
        entry["time_diff"] = hour
        if hour > 8:
            total_overtime += hour - 8

    return {"worktime": queryset, "overtime": total_overtime, "salary": salary}

def handle_overtime_pay_basic_salary(q):
    queryset = Salary.objects.filter(ID=q["query_id"]).filter(month__month=q["query_month"])
    return queryset[0].basic

def handle_vacancies():
    queryset = (
        Department.objects.all()
        .annotate(
            job_count=Count("job_title"),
            job_left=ExpressionWrapper(
                F("esti_num") - Count("job_title"), output_field=models.IntegerField()
            ),
        )
        .filter(job_left__gt=0)
    )
    
    return queryset

def handle_basic_salary_range(queryset):
    result = []
    for entry in queryset:
        # find all employees in the department and job title
        employees = Employee.objects.filter(department_id=entry.id)
        # find the max and min basic salary with these employees
        if len(employees) != 0:
            max_basic_salary = Salary.objects.filter(ID__in=employees).aggregate(
                max_basic_salary=Max("basic")
            )["max_basic_salary"]

            min_basic_salary = Salary.objects.filter(ID__in=employees).aggregate(
                min_basic_salary=Min("basic")
            )["min_basic_salary"]
        else:
            # generate random basic salary
            basic_salary = (random.randint(300, 800)*100, random.randint(300, 800)*100)
            max_basic_salary = max(basic_salary)
            min_basic_salary = min(basic_salary)

        result.append({'name':entry.name, 'job':entry.job, 'job_left':entry.job_left , 'salary':f"{min_basic_salary}~{max_basic_salary}"})
    # print(job_salary_range, len(job_salary_range), len(queryset))
    return result
   


def handle_spacial_holiday(q):
    emp = Employee.objects.get(ID=q["query_id"])
    job_tenure = datetime.today().date().year - emp.hire_date.year
    # 員工尚未入職
    if job_tenure < 0:
        return {
            "hired": False,
            "employee": emp,
            "job_tenure": job_tenure,
            "year": q["query_year"],
            "dayoff_total": 0,
            "dayoff_take": 0,
            "dayoff_left": 0,
        }
    

    max_value = DayOffDep.objects.filter(year__lte=job_tenure).aggregate(
        max_value=Max("RestDay")
    )["max_value"]
    
    # 查詢已請假天數
    try:
        restday = DayOff.objects.get(ID=q["query_id"], year=q["query_year"])
        dayoff_take = restday.RestDay
    except DayOff.DoesNotExist:
        # 該年未請假
        dayoff_take = 0
        

    return {
        "hired": True,
        "employee": emp,
        "job_tenure": job_tenure,
        "year": q["query_year"],
        "dayoff_total": max_value,
        "dayoff_take": dayoff_take,
        "dayoff_left": max(max_value - dayoff_take, 0),
    }

    ### original
    # try:
    #     restday = DayOff.objects.get(ID=q["query_id"], year=q["query_year"])
    # except DayOff.DoesNotExist:
    #     emp = Employee.objects.get(ID=q["query_id"])
    #     job_tenure = datetime.today().date().year - emp.hire_date.year
    #     max_value = DayOffDep.objects.filter(year__lte=job_tenure).aggregate(
    #         max_value=Max("RestDay")
    #     )["max_value"]

    #     return {
    #         "employee": emp,
    #         "job_tenure": job_tenure,
    #         "year": q["query_year"],
    #         "dayoff_total": max_value,
    #         "dayoff_take": 0,
    #         "dayoff_left": max_value,
    #     }

    # emp = restday.ID
    # job_tenure = datetime.today().date().year - emp.hire_date.year
    # max_value = DayOffDep.objects.filter(year__lte=job_tenure).aggregate(
    #     max_value=Max("RestDay")
    # )["max_value"]

    # return {
    #     "employee": emp,
    #     "job_tenure": job_tenure,
    #     "year": q["query_year"],
    #     "dayoff_total": max_value,
    #     "dayoff_take": restday.RestDay,
    #     "dayoff_left": max(max_value - restday.RestDay, 0),
    # }


def handle_participation(q):
    deps = Department.objects.filter(name=q)

    resultset = Project.objects.none()
    for dep in deps:
        emps = dep.job_title.all()
        for emp in emps:
            resultset = resultset.union(emp.project_set.all())

    return resultset
