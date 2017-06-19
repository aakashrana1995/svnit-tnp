from datetime import date, datetime
import itertools as it
import csv
import os
import zipfile
from io import BytesIO

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils import http

from company.models import Company, Job, JobLocation, Attachment, Branch, month_list
from consent.models import PersonalDetail, EducationDetail, CGPA, UserConsent, ConsentDeadline, FieldOrder
from company.views import create_branch_map, job as job_view
from tnp.settings import MEDIA_ROOT

from consent.forms import UserForm, PersonalDetailForm, EducationDetailForm
# my import @abhishek981996
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm


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


def create_degree_map():
    degree_map = {}
    degree_map['BTECH'] = 'BTech'
    degree_map['MTECH'] = 'MTech'
    degree_map['MSC'] = 'MSc'
    return degree_map


branch_map = create_branch_map()
degree_map = create_degree_map()


def index(request):
    return HttpResponseRedirect('/consent/home')


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username').upper()
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                next_url = request.POST.get('next')
                next_url = (next_url 
                    if http.is_safe_url(next_url, request.get_host()) 
                    else '/consent/home'
                )
                return HttpResponseRedirect(next_url)
            else:
                message = "Your TnP account is disabled!"
        else:
            message = "Invalid login details supplied!"

        return render(request, 'consent/login_user.html', {'message': message})

    else:
        if (request.user.is_authenticated):
            return HttpResponseRedirect('/consent/home')
        else:
            return render(request, 'consent/login_user.html', {})


def create_account(request):
    if (request.method == 'POST'):
        user_form = UserForm(prefix="user_form", data=request.POST)
        user_creation_form = UserCreationForm(
            prefix="user_creation_form", data=request.POST)
        personal_detail_form = PersonalDetailForm(
            prefix='personal_detail_form', data=request.POST)
        education_detail_form = EducationDetailForm(
            prefix='education_detail_form', data=request.POST, files=request.FILES)

        #print (user_form.errors.as_data())
        #print (user_creation_form.errors.as_data())
        #print (personal_detail_form.errors.as_data())
        #print (education_detail_form.errors.as_data())

        if (user_form.is_valid() and user_creation_form.is_valid() and personal_detail_form.is_valid() and education_detail_form.is_valid()):
            user = user_creation_form.save()
            user_form_obj = user_form.save(commit=False)
            user.email = user_form_obj.email
            user.first_name = user_form_obj.first_name.title()
            user.last_name = user_form_obj.last_name.title()
            user.username = user.username.upper()
            user.save()

            personal_detail = personal_detail_form.save(commit=False)
            personal_detail.user = user
            personal_detail.save()

            education_detail = education_detail_form.save(commit=False)
            education_detail.user = user
            education_detail.roll_number = user.username
            education_detail.save()

            cgpas = request.POST.getlist('cgpa')
            sem = 1
            for cgpa in cgpas:
                if(cgpa):
                    CGPA.objects.create(
                        person=education_detail, semester=sem, cgpa=cgpa)
                    sem += 1
                else:
                    break

        else:
            error_list = []
            print (user_form.errors.as_data())
            errors_dict = user_form.errors.as_data()
            for key, value in errors_dict.items():
                print (key, value)
                error_list.append(value)

            errors_dict = user_creation_form.errors.as_data()
            print (user_creation_form.errors.as_data())
            for key, value in errors_dict.items():
                for item in value:
                    print (item)
                    error_list.extend(item)

            errors_dict = personal_detail_form.errors.as_data()
            print (personal_detail_form.errors.as_data())
            for key, value in errors_dict.items():
                for item in value:
                    print (item)
                    error_list.extend(item)

            errors_dict = education_detail_form.errors.as_data()
            print (education_detail_form.errors.as_data())
            for key, value in errors_dict.items():
                for item in value:
                    print (item)
                    error_list.extend(item)

            print ('\n')
            print (error_list)
            return render(request, 'consent/create_account.html', {
                'user_form': user_form,
                'user_creation_form': user_creation_form,
                'personal_detail_form': personal_detail_form,
                'education_detail_form': education_detail_form,
                'error_list': error_list,
            })

        return HttpResponseRedirect('/consent/home')
        # return HttpResponse('Form successfully submitted.')

    else:
        user_form = UserForm(prefix='user_form', label_suffix='')
        user_creation_form = UserCreationForm(
            prefix='user_creation_form', label_suffix='')
        personal_detail_form = PersonalDetailForm(
            prefix='personal_detail_form', label_suffix='')
        education_detail_form = EducationDetailForm(
            prefix='education_detail_form', label_suffix='')

        return render(request, 'consent/create_account.html', {
            'user_form': user_form,
            'user_creation_form': user_creation_form,
            'personal_detail_form': personal_detail_form,
            'education_detail_form': education_detail_form,
        })


def grouper(n, iterable):
    """
    >>> list(grouper(3, 'ABCDEFG'))
    [['A', 'B', 'C'], ['D', 'E', 'F'], ['G']]
    """
    iterable = iter(iterable)
    return iter(lambda: list(it.islice(iterable, n)), [])


@login_required
def home(request):
    ed = EducationDetail.objects.get(user=request.user)
    branch = ed.branch
    batch = ed.college_passout_year
    request.session['branch_name'] = branch.name
    request.session['branch_degree'] = branch.degree

    jobs = Job.objects.filter(eligible_branches=branch, for_batch=batch).order_by('-updated_at')

    print (jobs)
    companies_list = []
    for job in jobs:
        job_dict = {}
        consent = UserConsent.objects.filter(user=request.user, job=job)
        consent_deadline_objs = ConsentDeadline.objects.filter(job=job)
        if(len(consent_deadline_objs) > 0):
            deadline = consent_deadline_objs[0].deadline
        else:
            deadline = ""

        if(consent and consent[0].is_valid == True):
            job_dict['button_type'] = 'cancel'
        else:
            job_dict['button_type'] = 'apply'

        job_dict['company'] = job.company.name
        job_dict['designation'] = job.designation
        job_dict['ctc'] = ('%f' % job.ctc).rstrip('0').rstrip('.')
        job_dict['url'] = job.slug
        job_dict['deadline'] = deadline
        job_dict['ctc_unit'] = job.get_ctc_unit_display()
        job_dict['salary_type'] = 'CTC'
        if (job.hiring_for == 'IN'):
            job_dict['salary_type'] = 'Stipend'

        if(job.created_at >= request.user.last_login):
            job_dict['badge'] = 'NEW'
        if(job.updated_at >= request.user.last_login):
            job_dict['badge'] = 'UPDATED'

        companies_list.append(job_dict)

    companies_list = list(grouper(3, companies_list))
    print (companies_list)
    return render(request, 'consent/home.html', {
        'companies_list': companies_list,
    })


def make_consent_dictionary(personal_detail, education_detail):
    consent_dict = {}
    consent_dict['roll_number'] = education_detail.roll_number
    consent_dict['name'] = personal_detail.user.get_full_name()
    dob = personal_detail.date_of_birth
    consent_dict['date_of_birth'] = '/'.join(
        [str(dob.day).zfill(2), str(dob.month).zfill(2), str(dob.year)])
    consent_dict['caste_category'] = personal_detail.get_caste_category_display()
    consent_dict['hometown'] = personal_detail.hometown
    consent_dict['ssc'] = str(education_detail.ssc)
    consent_dict['ssc_passing_year'] = education_detail.ssc_passing_year
    consent_dict['hsc'] = str(education_detail.hsc)
    consent_dict['hsc_passing_year'] = education_detail.hsc_passing_year
    consent_dict['entrance_exam'] = education_detail.get_entrance_exam_display()
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
    consent_dict['current_pincode'] = personal_detail.current_pincode
    consent_dict['permanent_pincode'] = personal_detail.permanent_pincode
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
    cgpa_field = field_order.filter(optional__lt=0)

    index = {}
    cgpa_header = []
    cgpa_type = ''

    if cgpa_field:
        cgpa_field = cgpa_field[0]
        cgpa_type = cgpa_field.field.slug
        optional = cgpa_field.optional

        if (branch_degree == 'BTECH'):
            optional += 9
        elif (branch_degree == 'MTECH'):
            optional += 5
        elif (branch_degree == 'MSC'):
            optional += 11

        if(cgpa_type == 'cgpa_upto_semester'):
            cgpa_header = [('Sem ' + str(i)) for i in range(1, optional + 1)]
        elif(cgpa_type == 'cgpa_of_semester'):
            cgpa_header = ['Sem ' + str(optional)]

    header = ['Sr No']

    i = 0
    for field in field_order:
        if (field.field.slug == cgpa_type):
            header.extend(cgpa_header)
            i += len(cgpa_header)
            index['cgpa'] = i - 1
        else:
            header.append(field.field.name)
            i += 1
            if (field.field.slug == 'name'):
                index['name'] = i - 1
            elif (field.field.slug == 'roll_number'):
                index['roll_number'] = i - 1

    degree = degree_map[branch_degree]
    filename = job.company.name + ' - ' + job.designation + \
        ' - ' + degree + ' ' + branch_map[branch_name] + '.csv'

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="' + filename + '"'

    writer = csv.writer(response)
    writer.writerow(header)

    branch_students = EducationDetail.objects.filter(
        branch=branch).values_list('user', flat=True)
    consents = UserConsent.objects.filter(
        job=job, user__in=branch_students, is_valid=True)

    consent_sheet = []

    for consent in consents:
        education_detail = EducationDetail.objects.get(
            user=consent.user, branch=branch)
        personal_detail = PersonalDetail.objects.get(user=consent.user)
        consent_dict = make_consent_dictionary(
            personal_detail, education_detail)

        cgpa_list = []
        if (cgpa_type == 'cgpa_upto_semester'):
            cgpa_list = [str(obj.cgpa) for obj in education_detail.cgpa.order_by(
                'pk')][:optional]
        elif (cgpa_type == 'cgpa_of_semester'):
            cgpa_list = [
                str(education_detail.cgpa.filter(semester=optional)[0].cgpa)]

        row = []
        for field in field_order:
            if (field.field.slug == cgpa_type):
                row.extend(cgpa_list)

            elif (field.field.slug == 'ssc'):
                value = str(consent_dict[field.field.slug])
                if (education_detail.ssc_result_type == 'PERCENTAGE'):
                    value += ' %'
                elif (education_detail.ssc_result_type == 'CGPA'):
                    value += ' CGPA'
                row.append(value)

            elif (field.field.slug == 'hsc'):
                value = str(consent_dict[field.field.slug])
                if (education_detail.hsc_result_type == 'PERCENTAGE'):
                    value += ' %'
                elif (education_detail.hsc_result_type == 'CGPA'):
                    value += ' CGPA'
                row.append(value)

            else:
                row.append(consent_dict[field.field.slug])

        consent_sheet.append(row)
        # writer.writerow(row)

    # Sorting the consent sheet: Priority order (highest first) -> cgpa, name,
    # roll_number
    sort_index = 0
    reverse_flag = False

    if ('cgpa' in index):
        sort_index = index['cgpa']
        reverse_flag = True
    elif ('name' in index):
        sort_index = index['name']
    elif ('roll_number' in index):
        sort_index = index['roll_number']

    consent_sheet.sort(
        key=lambda x: x[sort_index].lower(), reverse=reverse_flag)

    for sr_no, row in enumerate(consent_sheet):
        row.insert(0, str(sr_no + 1))
        writer.writerow(row)

    return response


def export_resumes(request):
    job_slug = request.GET['job']
    branch_name = request.GET['branch_name']
    branch_degree = request.GET['branch_degree']

    job = Job.objects.get(slug=job_slug)
    branch = Branch.objects.get(name=branch_name, degree=branch_degree)

    branch_students = EducationDetail.objects.filter(
        branch=branch).values_list('user', flat=True)
    consents = UserConsent.objects.filter(
        job=job, user__in=branch_students, is_valid=True)

    degree = degree_map[branch_degree]
    zip_subdir = job.company.name + ' - ' + job.designation + \
        ' - ' + degree + ' ' + branch_map[branch_name]
    zipname = zip_subdir + '.zip'

    resume_dir_path = os.path.join(MEDIA_ROOT, 'uploads', 'resumes')

    filepaths = []
    for consent in consents:
        education_detail = EducationDetail.objects.get(
            user=consent.user, branch=branch)
        resume_fp = os.path.join(MEDIA_ROOT, education_detail.resume.name)
        if (os.path.isfile(resume_fp)):
            filepaths.append(resume_fp)

    s = BytesIO()
    zf = zipfile.ZipFile(s, "w")

    for fpath in filepaths:
        fdir, fname = os.path.split(fpath)
        zip_path = os.path.join(zip_subdir, fname)
        zf.write(fpath, zip_path)

    zf.close()

    response = HttpResponse(
        s.getvalue(), content_type="application/x-zip-compressed")
    response['Content-Disposition'] = 'attachment; filename=' + zipname
    return response


@login_required
def apply(request):
    job_slug = request.GET['job']
    job = Job.objects.get(slug=job_slug)
    obj, created = UserConsent.objects.update_or_create(
        user=request.user, job=job, defaults={'is_valid': True})
    return HttpResponse('{ "message": "success" }')


@login_required
def cancel(request):
    job_slug = request.GET['job']
    job = Job.objects.get(slug=job_slug)
    UserConsent.objects.filter(
        user=request.user, job=job).update(is_valid=False)
    return HttpResponse('{ "message": "success" }')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


# my work @abhishek981996

@login_required
def view_profile(request):
    usercreation = User.objects.get(username=request.user)
    personal_detail = PersonalDetail.objects.get(user=request.user)
    education_detail = EducationDetail.objects.get(user=request.user)
    cgpa = CGPA.objects.filter(person=education_detail)

    semester_var = {}
    for semesters in cgpa:
        semester_var[semesters.semester] = semesters.cgpa

    return render(request, 'consent/profile.html', {
        'usercreation': usercreation,
        'personaldetail': personal_detail,
        'education_detail': education_detail,
        'semester_var': semester_var,
    })


@login_required
def edit_profile(request):
    personal_detail = PersonalDetail.objects.get(user=request.user)
    education_detail = EducationDetail.objects.get(user=request.user)
    cgpa = CGPA.objects.filter(person=education_detail)

    if (request.method == 'POST'):
        personal_detail_form = PersonalDetailForm(
            prefix='personal_detail_form',
            data=request.POST,
            instance=personal_detail,
        )
        education_detail_form = EducationDetailForm(
            prefix='education_detail_form',
            data=request.POST,
            files=request.FILES,
            instance=education_detail,
        )

        user_form = UserForm(
            prefix='user_form',
            data=request.POST,
            instance=request.user,
        )

        print (user_form.errors.as_data())
        print (personal_detail_form.errors.as_data())
        print (education_detail_form.errors.as_data())

        if (user_form.is_valid() and personal_detail_form.is_valid() and education_detail_form.is_valid()):
            user_obj = user_form.save()
            personal_detail = personal_detail_form.save()
            education_detail = education_detail_form.save()

            cgpas = request.POST.getlist('cgpa')

            sem = 1
            for cgpa in cgpas:
                new_cgpa = None
                if (cgpa):
                    new_cgpa = cgpa

                cgpa_qs = CGPA.objects.update_or_create(
                    person=education_detail,
                    semester=sem, 
                    defaults={'cgpa': new_cgpa},
                )
                sem += 1

            messages.success(request, 'Your profile was successfully updated!')
            return HttpResponseRedirect('/consent/profile/view')

        else:
            error_list = []

            errors_dict = personal_detail_form.errors.as_data()
            print (personal_detail_form.errors.as_data())
            for key, value in errors_dict.items():
                for item in value:
                    print (item)
                    error_list.extend(item)

            errors_dict = education_detail_form.errors.as_data()
            print (education_detail_form.errors.as_data())
            for key, value in errors_dict.items():
                for item in value:
                    print (item)
                    error_list.extend(item)

            print ('\n')
            print (error_list)
            semester_var = {}
            for semesters in cgpa:
                semester_var[semesters.semester] = semesters.cgpa

            return render(request, 'consent/edit_profile.html', {
                'user_form': user_form,
                'personal_detail_form': personal_detail_form,
                'education_detail_form': education_detail_form,
                'error_list': error_list,
                'semester_var': semester_var,

            })

        return HttpResponseRedirect('/consent/home')

    else:
        user_form = UserForm(prefix='user_form', instance=request.user)
        
        personal_detail_form = PersonalDetailForm(
            prefix='personal_detail_form',
            instance=personal_detail
        )
        
        education_detail_form = EducationDetailForm(
            prefix='education_detail_form',
            instance=education_detail
        )
        
        semester_var = {}

        for semesters in cgpa:
            semester_var[semesters.semester] = semesters.cgpa

        return render(request, 'consent/edit_profile.html', {
            'user_form': user_form,
            'personal_detail_form': personal_detail_form,
            'education_detail_form': education_detail_form,
            'cgpa': cgpa,
            'semester_var': semester_var,
        })


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect('/consent/home')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'consent/change_password.html', {
        'form': form
    })


@login_required
def merit_list(request):
    if request.user.groups.filter(name='Coordinator').exists():
        branch = request.user.education_detail.branch
        batch = request.user.education_detail.college_passout_year

        education_details = EducationDetail.objects.filter(
            branch=branch,
            college_passout_year=batch
        ).order_by('roll_number')

        merit_list = []
        sem_cnt = 6

        for sr_no, ed in enumerate(education_details):
            pd = PersonalDetail.objects.get(user=ed.user)
            
            cgpa_list = [str(obj.cgpa) for obj in 
                ed.cgpa.exclude(cgpa=None).order_by('pk')[:sem_cnt]]
            
            rem = max(sem_cnt - len(cgpa_list), 0)
            none_list = [None for i in range(rem)]
            cgpa_list.extend(none_list)

            data = make_consent_dictionary(pd, ed)
            student_detail = []
            student_detail.append(str(sr_no+1))
            student_detail.append(data['roll_number'])
            student_detail.append(data['name'])
            student_detail.append(data['date_of_birth'])
            student_detail.append(data['caste_category'])
            student_detail.append(data['hometown'])
            
            if (ed.ssc_result_type == 'PERCENTAGE'):
                data['ssc'] += ' %'
            elif (ed.ssc_result_type == 'CGPA'):
                data['ssc'] += ' CGPA'
            
            student_detail.append(data['ssc'])
            
            if (ed.hsc_result_type == 'PERCENTAGE'):
                data['hsc'] += ' %'
            elif (ed.ssc_result_type == 'CGPA'):
                data['hsc'] += ' CGPA'
            
            student_detail.append(data['hsc'])

            student_detail.extend(cgpa_list)
            student_detail.append(data['email'])
            student_detail.append(data['phone_number'])

            merit_list.append(student_detail)

        semesters = [i for i in range(1,sem_cnt+1)]
        
        return render(request, 'consent/merit_list.html', {
            'merit_list': merit_list,
            'semesters': semesters,
            'branch': branch,
            'batch': batch,
        })

    else:
        return HttpResponseRedirect('/consent/home')