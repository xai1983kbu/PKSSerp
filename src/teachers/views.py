from django.views.generic import FormView, RedirectView
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import HttpResponseRedirect
from .forms import LoginForm, EditTeacherForm, TeacherDeactivateForm, AddTeacherForm
from django.conf import settings
from .models import Teacher
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, reverse
from string import lower

from schools.models import School

#login to site
class LoginView(FormView):
    template_name = 'affiliated_schools.html'
    form_class = LoginForm
    success_url = '/'

    def form_valid(self, form):
        super(LoginView, self).form_valid(form)
        user = authenticate(**form.cleaned_data)
        if user:
            login(self.request, user)
            return HttpResponseRedirect(self.success_url)
        else:
            return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))

#logout from site
class LogoutView(RedirectView):
    url = settings.LOGIN_URL

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)

#success template after changing password
@login_required
def password_updated(request):
    return render(request, "pass_changed_successfully.html", {})


#view list of all teachers 
@login_required
def list_of_teachers(request):
    if request.user.useraccess.access_level == 'super' or request.user.useraccess.access_level == 'manager' or request.user.useraccess.access_level == 'principal' or request.user.useraccess.access_level == 'coordinator':
        # superusers, managers and coordinators can see all teachers
        if request.user.useraccess.access_level == 'super' or request.user.useraccess.access_level == 'manager' or request.user.useraccess.access_level == 'coordinator':
            teach = Teacher.objects.order_by("first_name")  #filter for active later
        # principals can only see profile views of the teachers in their school
        if request.user.useraccess.access_level == 'principal':
            school_ids = School.objects.filter(teacher__id = request.user.teacher.id) #get the list of schools that princ is affiliated with
            teach = Teacher.objects.filter(pkss_school__in = school_ids).order_by("first_name") #filter teacher model for just the teachers associated with the principals school
        num_teachers = len(teach)
        num_active_teachers = len(Teacher.objects.filter(currently_active=True))
        context = {
            "teach": teach,
            "num_teachers": num_teachers,  
            "num_active_teachers": num_active_teachers,  
        }
        return render(request, "list_of_teachers.html", context)



#view profile details for a teacher 
@login_required 
def teacher_profile_details(request, pk=None):
    if request.user.useraccess.access_level == 'super' or request.user.useraccess.access_level == 'manager' or request.user.useraccess.access_level == 'principal' or request.user.useraccess.access_level == 'coordinator':
        #principals should only be able to see this profile detail if the teacher is in their school
        teach = {}
        if request.user.useraccess.access_level == 'principal':
            #create a list of all teachers
            school_ids = School.objects.filter(teacher__id = request.user.teacher.id) #get the list of schools that princ is affiliated with
            teachers = Teacher.objects.filter(pkss_school__in = school_ids) #filter teacher model for just the teachers associated with the principals school
            #if t1 in teachers:
            if teachers.filter(id=pk).exists():
                teach = get_object_or_404(Teacher, pk=pk) #only allow this if present in principals subset 
        else:
            teach = get_object_or_404(Teacher, pk=pk)
        #sch = School.objects.get(id = std.pkss_school_id) #school of object
        context = {
        "teach": teach, 
        }
        return render(request, "teacher_profile.html", context) 


#edit an existing teacher record
@login_required
def edit_teacher_record(request, pk=None):
    if request.user.useraccess.access_level == 'super' or request.user.useraccess.access_level == 'manager' or request.user.useraccess.access_level == 'principal' or request.user.useraccess.access_level == 'coordinator':
        tch = get_object_or_404(Teacher, pk=pk)
        #form = StudentForm(request.POST or None, request.FILES or None, instance=std)
        form = EditTeacherForm(request.POST or None, instance=tch)
        if form.is_valid():
            try:
                instance = form.save(commit=False)
                curr_user = request.user.username
                instance.updated_last_by = curr_user
                instance.save()
                form.save_m2m() # this is essential - it saves the manytomany

                return HttpResponseRedirect( reverse('teacher_profile', kwargs={'pk': instance.pk}) )
            except:
                return HttpResponseRedirect('/teacher_profile/%s' %(pk))
        context = {
            "form": form,
            "tch": tch,
        }
        return render(request, "edit_teacher_profile.html", context)


#Deactivate a teacher
@login_required
def deactivate_teacher(request, pk=None):
    if request.user.useraccess.access_level == 'super' or request.user.useraccess.access_level == 'manager' or request.user.useraccess.access_level == 'principal' or request.user.useraccess.access_level == 'coordinator':
        tch = get_object_or_404(Teacher, pk=pk)
        #form = StudentForm(request.POST or None, request.FILES or None, instance=std)
        form = TeacherDeactivateForm(request.POST or None, request.FILES or None, instance=tch)
        if form.is_valid():
            try:
                instance = form.save(commit=False)
                curr_user = request.user.username
                instance.updated_last_by = curr_user
                instance.save()

                return HttpResponseRedirect( reverse('teacher_profile', kwargs={'pk': instance.pk}))
            except:
                return HttpResponseRedirect('/teacher_profile/%s' %(pk))
        context = {
            "form": form,
            "tch": tch,
        }
        return render(request, "deactivate_teacher.html", context)

#Add a new teacher
@login_required
def add_a_teacher(request):
    if request.user.useraccess.access_level == 'super' or request.user.useraccess.access_level == 'manager' or request.user.useraccess.access_level == 'principal' or request.user.useraccess.access_level == 'coordinator':
        #form = StudentForm(request.POST or None, request.FILES or None, instance=std)
        form = AddTeacherForm(request.POST or None)
        if form.is_valid():
            try:
                instance = form.save(commit=False)
                curr_user = request.user.username
                instance.updated_last_by = curr_user
                instance.save()
                form.save_m2m() # this is essential - it saves the manytomany

                return HttpResponseRedirect( reverse('teacher_profile', kwargs={'pk': instance.pk}) )
            except:
                return HttpResponseRedirect('/')
        context = {
            "form": form,
        }
        return render(request, "add_a_teacher.html", context)

