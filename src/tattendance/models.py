from __future__ import unicode_literals

from django.db import models 


# Create your models here.
class TeacherAttendance(models.Model):
	teacher = models.ForeignKey('teachers.Teacher')
	attendance_date = models.DateField(auto_now=False, auto_now_add=False)
	school = models.ForeignKey('schools.School')
	# SHIFT_CHOICES = (
	# 	('morning', 'morning'),
	# 	('evening', 'evening'),
	# )
	# shift = models.CharField(max_length=7, choices=SHIFT_CHOICES)
	datestamp = models.DateField(auto_now=False, auto_now_add=True) 
	STATUS_CHOICES = (
		('present', 'present'),
		('absent', 'absent'),
	)
	status =  models.CharField(max_length=7, choices=STATUS_CHOICES, default='absent')
	notes = models.CharField(max_length=150, null=True, blank=True)
	att_taker = models.CharField(max_length=120, null=True, blank=True)

	class Meta: 
		unique_together = ("teacher", "attendance_date", "school")

	@property
	def attendance_instance(self):
		return ''.join([self.teacher.full_name, '_',  self.status])

	def __unicode__(self):
		return self.attendance_instance

	def __string__(self):
		return self.attendance_instance