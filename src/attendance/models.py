from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Attendance(models.Model):
	student = models.ForeignKey('students.Student')
	attendance_date = models.DateField(auto_now=False, auto_now_add=False)
	datestamp = models.DateField(auto_now=False, auto_now_add=True) 
	datestamp_change = models.DateTimeField(auto_now=True, auto_now_add=False) 
	STATUS_CHOICES = (
		('present', 'present'),
		('absent', 'absent'),
	)

	status =  models.CharField(max_length=7, choices=STATUS_CHOICES, default='absent')
	notes = models.CharField(max_length=100, null=True, blank=True)

	class Meta: 
		unique_together = ("student", "attendance_date")

	@property
	def attendance_instance(self):
		return ''.join([self.student.full_name, '_',  self.status])

	def __unicode__(self):
		return self.attendance_instance

	def __string__(self):
		return self.attendance_instance 


class AttendanceCalendar(models.Model):
	school = models.ForeignKey('schools.School')
	first_day_of_month = models.DateField(auto_now=False, auto_now_add=False)
	workdays_in_month =  models.IntegerField(null=False, blank=False)
	non_weekend_workdays_off = models.IntegerField(null=True, blank=True)

	class Meta:
		unique_together = ("school", "first_day_of_month")

	def __unicode__(self):
		return self.school

	def __string__(self):
		return self.school

	def goto_att_cal(self):
		return reverse('attend_calendar')

class NonScheduledHolidays(models.Model):
	school = models.ForeignKey('schools.School')
	holiday_date = models.DateField(auto_now=False, auto_now_add=False)
	reason_for_holiday = models.CharField(max_length=500, null=False, blank=False) 

	class Meta:
		unique_together = ("school", "holiday_date")