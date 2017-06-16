import os

from django.db import models

from django.template.defaultfilters import slugify
from django.utils.timezone import now
from tnp.settings import MEDIA_ROOT, CURRENT_FINAL_YEAR_BATCH


JOB_DOMAINS = (
        ('C', 'Core'),
        ('N', 'Non-Core'),
)


BRANCHES = (
    ('CO', 'Computer Engineering'),
    ('ME', 'Mechanical Engineering'),
    ('CE', 'Civil Engineering'),
    ('EE', 'Electrical Engineering'),
    ('CH', 'Chemical Engineering'),
    ('EC', 'Electronics Engineering'),
    ('PHY', 'Physics'),
    ('CHEM', 'Chemistry'),
    ('MATH', 'Mathematics'),
    ('ALL', 'All Branches'),
)


DEGREES = (
    ('BTECH', 'BTech'),
    ('MTECH', 'MTech'),
    ('MSC', 'MSc'),
)


CTC_UNIT = (
    ('LPA', 'lpa'),
    ('PM', 'pm'),
    ('PA', 'pa'),
)


HIRING_FOR = (
    ('FT', 'Full Time'),
    ('IN', 'Internship'),
)


month_list = [
    'January',
    'February',
    'March',
    'April',
    'May',
    'June',
    'July',
    'August',
    'September',
    'October',
    'November',
    'December',
]


class Branch(models.Model):
    name = models.CharField(max_length=4, choices=BRANCHES)
    degree = models.CharField(max_length=5, choices=DEGREES, default='BTECH')

    class Meta:
        unique_together = ('name', 'degree')
        ordering = ['degree']

    def __str__(self):
        return "{}, {}".format(self.get_degree_display(), self.get_name_display())


class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    website = models.URLField(max_length=255, blank=True, null=True)
    about = models.TextField(max_length=5000, blank=True, null=True)
    infra_req =  models.TextField(max_length=5000, blank=True, null=True)
    other = models.TextField(max_length=5000, blank=True, null=True)
    crpdate = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField('date created', auto_now_add=True)
    updated_at = models.DateTimeField('date updated', auto_now=True)

    def __str__(self):
        return self.name


class PlacementCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    ctc_range = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return "{}, {}".format(self.name, self.ctc_range)


class JobType(models.Model):
    job_domain = models.CharField(max_length=1, choices=JOB_DOMAINS)
    job_type = models.CharField(max_length=255)

    class Meta:
        unique_together = ('job_domain', 'job_type')

    def __str__(self):
        return "{}, {}".format(self.get_job_domain_display(), self.job_type)


def company_file_path(instance, filename):
    dir_path = '/'.join(['uploads', 'jobs', instance.job.slug])
    path = '/'.join([MEDIA_ROOT, dir_path])
    
    if not os.path.exists(path):
        os.makedirs(path)
    
    file_path = os.path.join(dir_path, filename)
    return file_path

class Attachment(models.Model):
    job = models.ForeignKey('Job', related_name='attachment')
    file = models.FileField(upload_to=company_file_path)
    created_at = models.DateTimeField('date created', auto_now_add=True)
    updated_at = models.DateTimeField('date updated', auto_now=True)

    def get_file_name(self):
        arr = self.file.name.split('/')
        file_name = arr[-1]
        return file_name

    def __str__(self):
        arr = self.file.name.split('/')
        file_name = arr[-1]
        return "{}, {}".format(self.job.company, file_name)


class JobLocation(models.Model):
    job = models.ForeignKey('Job', related_name='job_location')
    location = models.CharField(max_length=255)

    class Meta:
        unique_together = ('job', 'location')

    def __str__(self):
        return "{}, {}, {}".format(self.job.company, self.job.designation, self.location)


class SelectionProcedure(models.Model):
    procedure = models.CharField(max_length=255)

    def __str__(self):
        return self.procedure


class Job(models.Model):
    company = models.ForeignKey('Company', related_name='job')
    slug = models.SlugField(max_length=255, null=True, blank=True)
    designation = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(max_length=5000, blank=True, null=True)
    requirements = models.TextField(max_length=5000, blank=True, null=True)
    perks = models.TextField(max_length=5000, blank=True, null=True)
    category = models.ForeignKey('PlacementCategory', related_name='job', blank=True, null=True) #Super Dream, A,B C
    job_type = models.ForeignKey('JobType', related_name='job', blank=True, null=True) #Core (Dev, PSU, Automobile), Non-Core (BA, Sales, Operations)
    eligible_branches = models.ManyToManyField('Branch')
    eligibility_criteria = models.TextField(max_length=5000, blank=True, null=True)
    ctc = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    ctc_unit = models.CharField(max_length=3, choices=CTC_UNIT, default='LPA')
    ctc_details = models.TextField(max_length=5000, blank=True, null=True)
    hiring_for = models.CharField(max_length=2, choices=HIRING_FOR, default='FT')
    for_batch = models.CharField(max_length=4, default=CURRENT_FINAL_YEAR_BATCH)
    bond_details = models.CharField(max_length=255, blank=True, null=True)
    selection_procedure = models.ManyToManyField('SelectionProcedure', blank=True)
    number_of_selections = models.IntegerField(blank=True, null=True)
    other = models.TextField(max_length=5000, blank=True, null=True)
    resumes_required = models.BooleanField(default=False)
    created_at = models.DateTimeField('date created', auto_now_add=True)
    updated_at = models.DateTimeField('date updated', auto_now=True)

    
    def save(self, *args, **kwargs):
        # uncomment if you don't want the slug to change every time the name changes
        if self.id is None:
            slug_str = self.company.name + ' ' + self.designation
            self.slug = slugify(slug_str)
        super(Job, self).save(*args, **kwargs)

    def __str__(self):
        return "{}, {}, {} {}".format(self.company, self.designation, self.ctc, self.get_ctc_unit_display())
