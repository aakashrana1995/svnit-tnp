from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.utils import timezone
from django.contrib import messages

from company.models import Company, Job, JobLocation, Attachment, Branch
from consent.models import UserConsent, UserDataFields, ConsentDeadline, FieldOrder
from company.forms import CompanyForm, JobForm, AttachmentForm, ConsentDeadlineForm 

import json
from datetime import datetime, timedelta


def add(request):
    if (request.method == 'POST'):
        company_form = CompanyForm(prefix="company_form", data=request.POST)
        job_form = JobForm(prefix="job_form", data=request.POST)
        attachment_form = AttachmentForm(prefix='attachment_form', files=request.FILES)
        consent_deadline_form = ConsentDeadlineForm(prefix='consent_deadline_form', data=request.POST)
        
        print (company_form.errors.as_data())
        print (job_form.errors.as_data())
        print (attachment_form.errors.as_data())
        print (consent_deadline_form.errors.as_data())


        if company_form.is_valid() and job_form.is_valid() and attachment_form.is_valid() and consent_deadline_form.is_valid():
            company = company_form.save()
            job = job_form.save(commit=False)
            job.company = company
            job.added_by = request.user
            job.save()
            job_form.save_m2m()
            
            eb = job.eligible_branches.filter(name='ALL')
            for all_type_branch in eb:
                all_branches = Branch.objects.filter(degree=all_type_branch.degree).exclude(name='ALL')
                for branch in all_branches:
                    job.eligible_branches.add(branch)
                job.eligible_branches.remove(all_type_branch)

            locations = request.POST.getlist('location');
            for loc in locations:
                if(len(loc)>0):
                    JobLocation.objects.create(job=job, location=loc)
            
            files = request.FILES.getlist('attachment_form-file')
            for f in files:
                instance = Attachment(file=f)
                instance.job = job
                instance.save()
            
            deadline_date = consent_deadline_form.cleaned_data['deadline_date']
            deadline_time = consent_deadline_form.cleaned_data['deadline_time']
            slack_time = consent_deadline_form.cleaned_data['slack_time']
            
            deadline = datetime.combine(deadline_date, deadline_time)
            ConsentDeadline.objects.create(job=job, deadline=deadline, slack_time=slack_time)
            
            consent_format = request.POST.getlist('A');
            cgpa_type = 'cgpa_upto_semester'
            
            position = 1
            for slug in consent_format:
                if (slug in ['cgpa_of_semester', 'cgpa_upto_semester']):
                    cgpa_type = slug
                else:
                    if (len(slug)<=2):
                        field = UserDataFields.objects.get(slug=cgpa_type)
                        FieldOrder.objects.create(job=job, field=field, optional=int(slug), position=position)
                    else:
                        field = UserDataFields.objects.get(slug=slug)
                        FieldOrder.objects.create(job=job, field=field, position=position)
                    position += 1

        messages.success(request, 'The company was successfully added!')
        return HttpResponseRedirect('/consent/home')
    else:
        if request.user.groups.filter(name='Coordinator').exists():
            company_form = CompanyForm(prefix='company_form', label_suffix='')
            job_form = JobForm(prefix='job_form', label_suffix='')
            attachment_form = AttachmentForm(prefix='attachment_form', label_suffix='')
            consent_deadline_form = ConsentDeadlineForm(prefix='consent_deadline_form', label_suffix='')

            default_fields = UserDataFields.objects.filter(default_position__gte=1).order_by(
                'default_position').values_list('slug', 'name')
            optional_fields = UserDataFields.objects.filter(default_position=0).values_list('slug', 'name')
            half = int(len(optional_fields)/2)
            optional_fields_1 = optional_fields[:half]
            optional_fields_2 = optional_fields[half:]

            return render(request, 'company/add.html', {
                    'company_form': company_form,
                    'job_form': job_form,
                    'attachment_form': attachment_form,
                    'consent_deadline_form': consent_deadline_form,
                    'default_fields': default_fields,
                    'optional_fields_1': optional_fields_1,
                    'optional_fields_2': optional_fields_2,
                })
        else:
            return HttpResponseRedirect('/consent/home')


def create_branch_map():
    branch_map = {}
    branch_map['CO'] = 'Computer Engineering'
    branch_map['ME'] = 'Mechanical Engineering'
    branch_map['CE'] = 'Civil Engineering'
    branch_map['EE'] = 'Electrical Engineering'
    branch_map['CH'] = 'Chemical Engineering'
    branch_map['EC'] = 'Electronics Engineering'
    branch_map['PHY'] = 'Physics'
    branch_map['CHEM'] = 'Chemistry'
    branch_map['MATH'] = 'Mathematics'

    return branch_map


def job(request, job_slug):
    job_dict = {}
    branch_map = create_branch_map()

    try:
        job = Job.objects.get(slug=job_slug)
    except Job.DoesNotExist:
        raise Http404("This company page doesn't exist!")

    job_dict['title'] = job.company.name + ', ' + job.designation
    job_dict['company'] = job.company.name
    job_dict['company_slug'] = job_slug
    job_dict['designation'] = job.designation
        
    job_dict['about_company'] = job.company.about
    job_dict['job_description'] = job.description
    job_dict['job_requirements'] = job.requirements
    job_dict['ctc'] = ('%f' % job.ctc).rstrip('0').rstrip('.')
    job_dict['ctc_unit'] = job.get_ctc_unit_display()
    job_dict['ctc_details'] = job.ctc_details
    job_dict['eligibility_criteria'] = job.eligibility_criteria
    job_dict['salary_type'] = 'CTC'
    if (job.hiring_for == 'IN'):
        job_dict['salary_type'] = 'Stipend'

    job_tags = []
    if(job.hiring_for):
        job_tags.append(job.get_hiring_for_display())
    if (job.job_type):
        job_tags.append(job.job_type.get_job_domain_display() + ' | ' + job.job_type.job_type)
    if (job.resumes_required):
        job_tags.append('Resumes required')
    job_dict['job_tags'] = job_tags 

    if(job.category):
        job_dict['job_category'] = job.category.name + ' Category'
    
    notifications = []
    if (job.resumes_required):
        notifications.append('This company has asked for resumes. Please add/update your resumes before applying!')
    if (job.other):
        notifications.append(job.other)
    job_dict['notifications'] = notifications


    eligible_branches = []
    eb = job.eligible_branches.values_list('name', 'degree')
    for branch in eb:
        if(branch[1] == 'BTECH'):
            eligible_branches.append('BTech, ' + branch_map[branch[0]])
        elif(branch[1] == 'MTECH'):
            eligible_branches.append('MTech, ' + branch_map[branch[0]])
        elif(branch[1] == 'MSC'):
            eligible_branches.append('MSc, ' + branch_map[branch[0]])
    eligible_branches.sort()
    job_dict['eligible_branches'] = eligible_branches

    locations = list(job.job_location.values_list('location', flat=True))
    
    if(len(locations)>0):
        job_dict['locations'] = locations
    
    if(job.number_of_selections):
        job_dict['number_of_selections'] = str(job.number_of_selections)

    selection_procedure = list(job.selection_procedure.values_list('procedure', flat=True))
    if(len(selection_procedure)>0):
        job_dict['selection_procedure'] = selection_procedure
        
    atch_list = Attachment.objects.filter(job=job)
    attachments = []

    for atch in atch_list:
        file_location = '/media/' + str(atch.file)
        arr = file_location.split('/')
        file_name = arr[-1]
        attachment = (file_name, file_location)
        attachments.append(attachment)

    if(len(attachments)>0):
        job_dict['attachments'] = attachments

    consent_deadline_obj = ConsentDeadline.objects.filter(job=job)
    curr_time = timezone.now()
    consent = UserConsent.objects.filter(user=request.user, job=job)

    if(len(consent_deadline_obj)>0):
        display_deadline = consent_deadline_obj[0].deadline
        real_deadline = display_deadline + timedelta(hours=consent_deadline_obj[0].slack_time)

        if (curr_time <= real_deadline):
            if(consent and consent[0].is_valid == True):
                job_dict['button_id'] = 'cancel'
            else:
                job_dict['button_id'] = 'apply'
        
        else:
            if(consent and consent[0].is_valid == True):
                job_dict['button_id'] = 'disabled_applied'
            else:
                job_dict['button_id'] = 'disabled_not_applied'
            
    else:
        display_deadline = ''
        if(consent and consent[0].is_valid == True):
            job_dict['button_id'] = 'disabled_applied'
        else:
            job_dict['button_id'] = 'disabled_not_applied'
    
    job_dict['display_deadline'] = display_deadline
    
    return render(request, 'company/job.html', job_dict)

