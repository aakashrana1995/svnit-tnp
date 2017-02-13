from django.contrib import admin

from consent.models import PersonalDetail, EducationDetail, CGPA, \
UserConsent, UserDataFields, ConsentDeadline, FieldOrder

admin.site.register(PersonalDetail)
admin.site.register(EducationDetail)
admin.site.register(CGPA)
admin.site.register(UserConsent)
admin.site.register(UserDataFields)
admin.site.register(ConsentDeadline)
admin.site.register(FieldOrder)