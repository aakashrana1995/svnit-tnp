from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from company.models import Company, Job, JobLocation, Attachment, Branch, month_list
from consent.models import PersonalDetail, EducationDetail, CGPA, UserConsent, ConsentDeadline, FieldOrder
from company.views import create_branch_map

from datetime import date
import itertools as it
import csv

branch_map = create_branch_map()

def create_branch_map():
    branch_map = {}
    branch_map['CO'] = 'Computer'
    branch_map['ME'] = 'Mechanical'
    branch_map['CE'] = 'Civil'
    branch_map['EE'] = 'Electrical'
    branch_map['CH'] = 'Chemical'
    branch_map['EC'] = 'Electronics'
    branch_map['PHY'] = 'Physics'
    branch_map['CHEM'] = 'Chemistry'
    branch_map['MATH'] = 'Mathematics'

    return branch_map

def index(request):
	#return render(request, 'base.html')
    return HttpResponse("Aakash says hello world!")

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username').upper()
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/consent/home')
            else:
                return HttpResponse("Your TnP account is disabled.")
        else:
            #print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")
    else:
        if (request.user.is_authenticated):
            return HttpResponseRedirect('/consent/home')
        else:
            return render(request, 'consent/login_user.html', {})


def grouper(n, iterable):
    """
    >>> list(grouper(3, 'ABCDEFG'))
    [['A', 'B', 'C'], ['D', 'E', 'F'], ['G']]
    """
    iterable = iter(iterable)
    return iter(lambda: list(it.islice(iterable, n)), [])


@login_required
def home(request):
    branch = EducationDetail.objects.get(user=request.user).branch
    request.session['branch_name'] = branch.name
    request.session['branch_degree'] = branch.degree

    jobs = Job.objects.filter(eligible_branches=branch).order_by('-updated_at')

    print (jobs)
    companies_list = []
    for job in jobs:
        job_dict = {}
        consent = UserConsent.objects.filter(user=request.user, job=job)
        consent_deadline_objs = ConsentDeadline.objects.filter(job=job)
        if(len(consent_deadline_objs)>0):
            deadline = consent_deadline_objs[0].deadline
        else:
            deadline = ""

        if(consent and consent[0].is_valid == True):
            job_dict['button_type'] = 'cancel'
        else:
            job_dict['button_type'] = 'apply'
        
        job_dict['company'] = job.company.name
        job_dict['designation'] = job.designation
        job_dict['ctc'] = job.ctc
        job_dict['url'] = job.slug
        job_dict['deadline'] = deadline
        if(job.created_at >= request.user.last_login):
            job_dict['badge'] = 'NEW'
        if(job.updated_at >= request.user.last_login):
            job_dict['badge'] = 'UPDATED'
        
        companies_list.append(job_dict)

    companies_list = list(grouper(3,companies_list))
    print (companies_list) 
    return render(request, 'consent/home.html', {
        'companies_list': companies_list,
    })
 

def make_consent_dictionary(personal_detail, education_detail):
    consent_dict = {}
    consent_dict['roll_number'] = education_detail.roll_number
    consent_dict['name'] = personal_detail.user.get_full_name()
    consent_dict['date_of_birth'] = personal_detail.date_of_birth
    consent_dict['caste_category'] = personal_detail.caste_category
    consent_dict['hometown'] = personal_detail.hometown
    consent_dict['ssc'] = education_detail.ssc
    consent_dict['ssc_passing_year'] = education_detail.ssc_passing_year
    consent_dict['hsc'] = education_detail.hsc
    consent_dict['hsc_passing_year'] = education_detail.hsc_passing_year
    consent_dict['entrance_exam'] = education_detail.entrance_exam
    consent_dict['entrance_exam_score'] = education_detail.entrance_exam_score
    
    consent_dict['branch'] = branch_map[education_detail.branch.name]

    consent_dict['current_backlogs'] = education_detail.current_backlogs
    consent_dict['total_backlogs'] = education_detail.total_backlogs
    consent_dict['current_address'] = personal_detail.current_address
    consent_dict['current_residence_city'] = personal_detail.current_residence_city
    consent_dict['current_residence_state'] = personal_detail.current_residence_state
    consent_dict['permanent_address'] = personal_detail.permanent_address
    consent_dict['permanent_residence_city'] = personal_detail.permanent_residence_city
    consent_dict['permanent_residence_state'] = personal_detail.permanent_residence_state
    consent_dict['email'] = personal_detail.user.email
    consent_dict['phone_number'] = personal_detail.phone_number

    return consent_dict



@login_required
def export_consent(request):
    job_slug = request.GET['job']
    branch_name = request.GET['branch_name']
    branch_degree = request.GET['branch_degree']

    job = Job.objects.get(slug=job_slug)
    branch = Branch.objects.get(name=branch_name, degree=branch_degree)    

    field_order = FieldOrder.objects.filter(job=job).order_by('position')
    cgpa_field = field_order.get(optional__gte=0)
    cgpa_type = cgpa_field.field.slug
    optional = cgpa_field.optional

    cgpa_header = []
    if(cgpa_type == 'cgpa_upto_semester'):
        cgpa_header = [('Sem '+ str(i)) for i in range(1, optional+1)]
    elif(cgpa_type == 'cgpa_of_semester'):
        cgpa_header = 'Sem ' + str(optional)

    header = []
    for field in field_order:
        if (field.field.slug==cgpa_type):
            header.extend(cgpa_header)
        else:
            header.append(field.field.name)

    if(branch_degree=='BTECH'):
        degree = 'BTech'
    elif(branch_degree=='MTECH'):
        degree = 'MTech'
    else:
        degree = 'MSc'

    filename = job.company.name + '-' + job.designation + '-' + degree + ' ' + branch_map[branch_name] + '.csv'

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="' + filename + '"'

    writer = csv.writer(response)
    writer.writerow(header)

    consents = UserConsent.objects.filter(job=job, is_valid=True)

    for consent in consents:
        education_detail = EducationDetail.objects.get(user=consent.user)
        if(education_detail.branch!=branch):
            continue

        personal_detail = PersonalDetail.objects.get(user=consent.user)
        consent_dict = make_consent_dictionary(personal_detail, education_detail)

        cgpa_list = []
        if(cgpa_type=='cgpa_upto_semester'):
            cgpa_list = [str(obj.cgpa) for obj in education_detail.cgpa.order_by('semester')][:optional]
        else:
            cgpa_list = education_detail.cgpa.filter(semester=optional)

        row = []
        for field in field_order:
            if (field.field.slug==cgpa_type):
                row.extend(cgpa_list)
            else:
                row.append(consent_dict[field.field.slug])

        writer.writerow(row)

    return response


@login_required
def apply(request):
    job_slug = request.GET['job']
    job = Job.objects.get(slug=job_slug)
    obj, created = UserConsent.objects.update_or_create(user=request.user, job=job, defaults={'is_valid':True})
    return HttpResponse('{ "message": "success" }')


@login_required
def cancel(request):
    job_slug = request.GET['job']
    job = Job.objects.get(slug=job_slug)
    UserConsent.objects.filter(user=request.user, job=job).update(is_valid=False)
    return HttpResponse('{ "message": "success" }')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')