from django.contrib import admin

from .models import Attachment, Branch, Company, \
	Job, JobLocation, JobType, PlacementCategory, SelectionProcedure

# Register your models here.

admin.site.register(Attachment)
admin.site.register(Branch)
admin.site.register(Company)
admin.site.register(Job)
admin.site.register(JobLocation)
admin.site.register(JobType)
admin.site.register(PlacementCategory)
admin.site.register(SelectionProcedure)
