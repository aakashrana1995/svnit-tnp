from django.contrib import admin

from consent.models import PersonalDetail, EducationDetail, CGPA

admin.site.register(PersonalDetail)
admin.site.register(EducationDetail)
admin.site.register(CGPA)
