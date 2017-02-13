from django.shortcuts import render
from django.http import HttpResponse
from django.forms import formset_factory

from company.models import Company, Job, JobLocation, Attachment
from consent.models import UserConsent, UserDataFields, ConsentDeadline, FieldOrder
from company.forms import CompanyForm, JobForm, AttachmentForm, ConsentDeadlineForm 

import json
from datetime import datetime


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
            #print ('valid')
            company = company_form.save()
            #company = Company.objects.latest('id')
            job = job_form.save(commit=False)
            job.company = company
            job.save()
            job_form.save_m2m()
            
            locations = request.POST.getlist('location');
            for loc in locations:
                print (loc)
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
                print (slug)
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

        return HttpResponse("Aakash says hello world!")
    else:
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
    job = Job.objects.get(slug=job_slug)

    consent = UserConsent.objects.filter(user=request.user, job=job)
    
    if(consent and consent[0].is_valid == True):
        job_dict['button_id'] = 'cancel'
    else:
        job_dict['button_id'] = 'apply'
    
    print (job)
    job_dict['title'] = job.company.name + ', ' + job.designation
    job_dict['company'] = job.company.name
    job_dict['designation'] = job.designation
    if(job.company.website):
        job_dict['website'] = job.company.website
    
    if(job.category):
        job_dict['job_category'] = job.category.name + ' Category'
    #job_dict["consent_deadline"]
    if(job.company.about):
        job_dict['about_company'] = job.company.about
    if(job.description):
        job_dict['job_description'] = job.description
    if(job.requirements):
        job_dict['job_requirements'] = job.requirements
    if(job.ctc):
        job_dict['ctc'] = str(job.ctc)
    if(job.ctc_details):
        job_dict['ctc_details'] = job.ctc_details
    
    if(job.eligibility_criteria):
        job_dict['eligibility_criteria'] = job.eligibility_criteria
        #all_details.append((len(eligibility_criteria), eligibility_criteria))
 
    #all_details = []

    eligible_branches = []
    eb = job.eligible_branches.values_list('name', 'degree')
    #eb_cnt = 0
    for branch in eb:
        if(branch[1] == 'BTECH'):
            eligible_branches.append('BTech, ' + branch_map[branch[0]])
            #eb_cnt += 1
        elif(branch[1] == 'MTECH'):
            eligible_branches.append('MTech, ' + branch_map[branch[0]])
            #eb_cnt += 1
        elif(branch[1] == 'MSC'):
            eligible_branches.append('MSc, ' + branch_map[branch[0]])
            #eb_cnt += 1
    eligible_branches.sort()
    job_dict['eligible_branches'] = eligible_branches

    #eb_dict = {}
    #eb_dict['arr'] = eligible_branches
    #eb_dict['name'] = 'Eligible Branches'
    #all_details.append((int(eb_cnt), eb_dict))

    locations = list(job.job_location.values_list('location', flat=True))
    
    if(len(locations)>0):
        job_dict['locations'] = locations
        #locs_dict = {}
        #locs_dict['arr'] = locs
        #locs_dict['name'] = 'Job Location(s)'
        #all_details.append((len(locs), locs_dict))
    
    if(job.number_of_selections):
        job_dict['number_of_selections'] = str(job.number_of_selections)
        #tmp['arr'] = str(job.number_of_selections)
        #tmp['name'] = 'Expected Number of Selections'
        #all_details.append((int(1), tmp))

    selection_procedure = list(job.selection_procedure.values_list('procedure', flat=True))
    if(len(selection_procedure)>0):
        job_dict['selection_procedure'] = selection_procedure
        #sel_dict = {}
        #sel_dict['arr'] = selection_procedure
        #sel_dict['name'] = 'Selection Procedure'
        #all_details.append((len(selection_procedure), sel_dict))
    
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
        #atch_dict = {}
        #atch_dict['arr'] = attachments
        #atch_dict['name'] = 'Attachments'
        #all_details.append((len(attachments), atch_dict))

    #all_details.sort(key=lambda x: x[0])
    #all_details.reverse()
    
    #job_dict['all_details'] = all_details
    print (job_dict)
    #return HttpResponse(json.dumps(job_dict))
    return render(request, 'company/job.html', job_dict)

