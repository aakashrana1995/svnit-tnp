from django.contrib import admin

from consent.models import PersonalDetail, EducationDetail, CGPA, \
UserConsent, UserDataFields, ConsentDeadline

admin.site.register(PersonalDetail)
admin.site.register(EducationDetail)
admin.site.register(CGPA)
admin.site.register(UserConsent)
admin.site.register(UserDataFields)
admin.site.register(ConsentDeadline)
