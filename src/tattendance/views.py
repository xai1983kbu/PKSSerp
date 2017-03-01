from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta
from django.forms import modelformset_factory
from .models import TeacherAttendance
from .forms import TeacherAttendanceForm
from students.models import Student
from schools.models import School
from classes.models import Class
from teachers.models import Teacher
from django.contrib import messages
from django.db import connection #for custom sql
from django.db.models import *
import datetime
from collections import OrderedDict
from django.utils import timezone
from dateutil.relativedelta import relativedelta
import json


def tattendance_affiliated_schools(request):
	#schools = School.objects.all()
    schools = {}  #by default, the dict of schools for tattendance should be empty
    #logic: if a superuser or manager is loggin on, they should see all schools. Otherwise, only if a user is a principal, they should see the schools they are affiliated with
    if request.user.useraccess.access_level == 'super' or request.user.useraccess.access_level == 'manager':
        schools = School.objects.all()
    elif request.user.teacher.level == 'principal':
        schools = School.objects.filter(teacher__id = request.user.teacher.id)
    #test = request.user.teacher.pkss_school.all().values_list('id', flat=True) 
    test = 0
    context = {
        'affiliated_schools': schools, 
        'test': test, 
        } 
    return render(request, 'tattendance_affiliated schools.html', context)

# this helper function below is a custom func to convert the cursor object return to a dict
def dictfetchall(cursor):
	#Return all rows from a cursor as a dict
	columns = [col[0] for col in cursor.description]
	return [
		dict(zip(columns, row))
		for row in cursor.fetchall()
	]

def get_dates_range(start, end, delta):
    curr = start
    while curr < end:
        yield curr
        curr += delta

@login_required()
def tattendance_dates(request, school_id):    
    five_days_back = date.today() - timedelta(2)
    next_day = date.today() + timedelta(1)
    dates_range = list(get_dates_range(five_days_back, next_day, timedelta(days=1)))
	# cursor = connection.cursor()

	# cursor.execute(
	# '''SELECT i,
	# COUNT (*) AS num_att,
	# %s AS school_id
	# FROM
	# (select i::date from generate_series(Date(Now() -  Interval '2 day'), 
	# Date(Now()), '1 day'::interval) i) AS A
	# LEFT JOIN (SELECT X.*, Y.pkss_school_id
	# FROM attendance_attendance AS X
	# INNER JOIN students_student AS Y ON X.student_id = Y.id
	# INNER JOIN classes_class AS Z ON Y.pkss_class_id = Z.id
	# WHERE pkss_school_id= %s) AS B ON A.i = B.attendance_date
	# GROUP BY i 
	# ORDER BY i DESC;''', [school_id, school_id])

	# l1 = dictfetchall(cursor) #raw sql query list of dates

    #logic: only submit the request if superuser or a principal with access to a specific school
    if request.user.useraccess.access_level == 'super' or request.user.useraccess.access_level == 'manager':
        sch = School.objects.get(pk=school_id)
    #elif request.user.teacher.level == 'principal' and school_id in test:
    elif request.user.teacher.level == 'principal' and request.user.teacher.pkss_school.filter(id=school_id).exists(): 
        sch = School.objects.get(pk=school_id)
    else:
        sch = {}
        school_id = {}

    #sch = School.objects.get(pk=school_id) #use this if no controls required
    context = {
		'dates_range': dates_range, 
		'school_id': school_id, 
		'sch': sch,
    } 
    return render(request, 'tattendance_dates.html', context)


@login_required()
def add_tattendance(request, school_id, date, readonly=False):
        school = School.objects.get(pk=school_id)

        #teacher_list = Teacher.objects.all()  # < filter this for just teachers in the school
        teacher_list = Teacher.objects.filter(pkss_school = school_id) #filter teachers for just those associated with the school
        teacher_list_initial = [{
                                'teacher': teacher,
                                'attendance_date': date,
                                'school': school
                                }
                                for teacher in teacher_list]

        tattendance_formset = modelformset_factory(TeacherAttendance, form=TeacherAttendanceForm,
                                                   extra=len(teacher_list),
                                                   max_num=len(teacher_list)
                                                   )

        formsets = tattendance_formset(initial=teacher_list_initial,
                                       queryset=TeacherAttendance.objects.filter(school=school, attendance_date=date, teacher__in=teacher_list)
                                       )

        date = datetime.datetime.strptime(date, "%Y-%m-%d").date()

        if request.method == 'POST':
            teacher_list = Teacher.objects.filter(pkss_school = school_id) #filter teachers for just those associated with the school
            tattendance_formset = modelformset_factory(TeacherAttendance, form=TeacherAttendanceForm,
                                                       extra=len(teacher_list),
                                                       max_num=len(teacher_list))

            formsets = tattendance_formset(request.POST)
            if formsets.is_valid():
                formsets.save()

                msg = 'Attendance submitted successfully for %s on %s' % (school.school_name, date.strftime("%b %d, %Y"))
                messages.success(request, msg)
                return redirect(reverse('tattendance_dates', kwargs={'school_id': school.pk}))
            else:
                print json.dumps(formsets.errors, indent=4)


        context = {
        'formset': formsets,
        'date': date,
        'school': school,
        'teacher_list': teacher_list
        }

        return render(request, 'teacher_attendance_formset.html', context)

