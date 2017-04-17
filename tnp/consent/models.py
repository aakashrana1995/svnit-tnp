import os

from django.db import models
from django.contrib.auth.models import User


CASTE_CATEGORIES = (
    ('OBC', 'OBC'),
    ('GEN', 'General/Open'),
    ('SC', 'SC'),
    ('ST', 'ST'),
    ('OBC-PH', 'OBC Physically Handicapped'),
    ('General-PH', 'General Physically Handicapped'),
    ('SC-PH', 'SC Physically Handicapped'),
    ('ST-PH', 'ST Physically Handicapped'),
)

RESULT_TYPES = (
    ('CGPA', 'CGPA'),
    ('PERCENTAGE', '%'),
)

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
)

ENTRANCE_EXAM_TYPES = (
    ('JEE_MAIN', 'JEE Mains'),
    ('SAT', 'SAT'),
)

SEMESTERS = (
    ('1', 'First'),
    ('2', 'Second'),
    ('3', 'Third'),
    ('4', 'Fourth'),
    ('5', 'Fifth'),
    ('6', 'Sixth'),
    ('7', 'Seventh'),
    ('8', 'Eighth'),
    ('9', 'Ninth'),
    ('10', 'Tenth'),
)


class PersonalDetail(models.Model):
    user = models.OneToOneField(User, related_name='personal_detail')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    caste_category = models.CharField(max_length=3, choices=CASTE_CATEGORIES, default='GEN')
    phone_number = models.CharField(max_length=10, unique=True)
    current_address = models.TextField(max_length=5000, blank=True, null=True)
    hometown = models.CharField(max_length=255, blank=True, null=True)
    current_residence_city = models.CharField(max_length=255, blank=True, null=True)
    current_pincode = models.CharField(max_length=6, blank=True, null=True, default='395007')
    current_residence_state = models.CharField(max_length=255, blank=True, null=True)
    permanent_address = models.TextField(max_length=5000, blank=True, null=True)
    permanent_residence_city = models.CharField(max_length=255, blank=True, null=True)
    permanent_pincode = models.CharField(max_length=6, blank=True, null=True)
    permanent_residence_state = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField('date created', auto_now_add=True)
    updated_at = models.DateTimeField('date updated', auto_now=True)

    def __str__(self):
        return "{}, {}, {}".format(
            self.user.get_full_name(), self.user.email, self.phone_number)

class CGPA(models.Model):
    person = models.ForeignKey('EducationDetail', related_name='cgpa')
    semester = models.CharField(max_length=1, choices=SEMESTERS)
    cgpa = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return "{}, {}, {}".format(
            self.person.user.get_full_name(),
            self.semester,
            self.cgpa,
            )


def resume_file_path(instance, filename):
    dir_path = os.path.join('uploads', 'resumes', instance.college_passout_year, instance.branch.degree + '_' + instance.branch.name)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    extension = filename.split('.')[-1]    
    filename = '_'.join([instance.user.first_name, instance.user.last_name, 'NITSurat', 'Resume']) + '.' + extension
    file_path = os.path.join(dir_path, filename)
    return file_path


class EducationDetail(models.Model):
    user = models.OneToOneField(User, related_name='education_detail')
    roll_number = models.CharField(max_length=31, unique=True)

    ssc = models.DecimalField(max_digits=4, decimal_places=2)
    ssc_board_name = models.CharField(max_length=255, blank=True, null=True)
    ssc_result_type = models.CharField(max_length=10, choices=RESULT_TYPES, default='PERCENTAGE')
    ssc_passing_year = models.CharField(max_length=4, blank=True, null=True)

    hsc = models.DecimalField(max_digits=4, decimal_places=2)
    hsc_board_name = models.CharField(max_length=255, blank=True, null=True)
    hsc_result_type = models.CharField(max_length=10, choices=RESULT_TYPES, default='PERCENTAGE')
    hsc_passing_year = models.CharField(max_length=4, blank=True, null=True)

    entrance_exam_score = models.IntegerField(blank=True, null=True)
    entrance_exam = models.CharField(max_length=8, choices=ENTRANCE_EXAM_TYPES, default='JEE_MAIN')
    
    branch = models.ForeignKey('company.Branch')
    college_passout_year = models.CharField(max_length=4)
    resume = models.FileField(upload_to=resume_file_path, blank=True, null=True)

    current_backlogs = models.IntegerField(default=0)
    total_backlogs = models.IntegerField(default=0)
 
    created_at = models.DateTimeField('date created', auto_now_add=True)
    updated_at = models.DateTimeField('date updated', auto_now=True)

    def __str__(self):
        cgpa_obj = self.cgpa.all().order_by('-semester')
        if(cgpa_obj):
            cgpa_str = str(cgpa_obj[0].cgpa) + ', Sem ' + cgpa_obj[0].semester 
        else:
            cgpa_str = ''
        
        return "{}, {}, {}".format(
            self.user.get_full_name(), 
            self.roll_number,
            cgpa_str,
        )


class UserConsent(models.Model):
    user = models.ForeignKey(User, related_name='user_consent')
    job = models.ForeignKey('company.Job', related_name='user_consent')
    is_valid = models.BooleanField(default=True)
    created_at = models.DateTimeField('date created', auto_now_add=True)
    updated_at = models.DateTimeField('date updated', auto_now=True)
    
    class Meta:
        unique_together = ('user', 'job')

    def __str__(self):
        return "{}, {}, {}, {}".format(self.user.get_full_name(), self.job.company.name, self.job.designation, self.is_valid)


class UserDataFields(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.CharField(max_length=255, unique=True)
    default_position = models.IntegerField(default=0);

    def __str__(self):
        return "{}, {}".format(self.name, self.slug)


class FieldOrder(models.Model):
    job = models.ForeignKey('company.Job', related_name='field_order')
    field = models.ForeignKey('UserDataFields', related_name='field_order')
    optional = models.IntegerField(blank=True, null=True)
    position = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return "{}, {}, {}, {}".format(self.job.company.name, self.job.designation, self.field, self.position)

class ConsentDeadline(models.Model):
    job = models.OneToOneField('company.Job', related_name='consent_deadline')
    deadline = models.DateTimeField()
    strict = models.BooleanField(default=True) #If strict, consent will be automatically sent to TnP Office after deadline
    slack_time = models.IntegerField(default=0) #After this no of hours, the consent data will be automatically sent
    
    def __str__(self):
        return "{}, {}, {}, {}, {} hours".format(
            self.job.company.name,
            self.job.designation,
            self.deadline,
            self.strict,
            self.slack_time,
        )
