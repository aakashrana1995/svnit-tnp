from django import forms

from django.utils.translation import ugettext_lazy as _

from tnp.settings import DATE_INPUT_FORMATS

from django.contrib.auth.models import User
from consent.models import PersonalDetail, EducationDetail, CGPA
from company.models import Branch


class UserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        #exclude = ['username', 'password', 'date_joined']


class PersonalDetailForm(forms.ModelForm):
    date_of_birth = forms.DateField(input_formats=DATE_INPUT_FORMATS)

    def __init__(self, *args, **kwargs):
        super(PersonalDetailForm, self).__init__(*args, **kwargs)
        self.fields['gender'].required = False
        self.fields['date_of_birth'].required = True
        self.fields['hometown'].required = True
        self.fields['permanent_residence_state'].required = True

    class Meta:
        model = PersonalDetail
        exclude = ['user', 'created_at', 'updated_at']

        labels = {
            'date_of_birth': _('Date of Birth'),
            'caste_category': _('Caste Category'),
            'phone_number': _('Mobile Number'),
            'current_address': _('Current Address'),
            'current_residence_city': _('Current City'),
            'current_pincode': _('Pincode'),
            'current_residence_state': _('Current State'),
            'permanent_address': _('Permanent Address'),
            'permanent_residence_city': _('Permanent City'),
            'permanent_pincode': _('Pincode'),
            'permanent_residence_state': _('Permanent State'),
        }


class EducationDetailForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(EducationDetailForm, self).__init__(*args, **kwargs)
        self.fields['branch'].required = False
        self.fields['college_passout_year'].required = True
        self.fields['branch'].queryset = Branch.objects.exclude(name='ALL')

    class Meta:
        model = EducationDetail
        exclude = ['user', 'roll_number', 'created_at', 'updated_at']

        labels = {
            'ssc': _('10th Std Score'),
            'ssc_board_name': _('10th Board Name'),
            'ssc_result_type': _('Type'),
            'ssc_passing_year': _('Pass Year'),

            'hsc': _('12th Std Score'),
            'hsc_board_name': _('12th Board Name'),
            'hsc_result_type': _('Type'),
            'hsc_passing_year': _('Pass Year'),

            'entrance_exam_score': _('Entrance Exam Score'),
            'entrance_exam': _('Entrance Exam'),
            'current_backlogs': _('Current Backlogs'),
            'total_backlogs': _('Total Backlogs'),
            'college_passout_year': _('College Passout Year'),
        }

#shall be used as Model Formset mostly
"""
class CGPAForm(forms.ModelForm):
    class Meta:
        model = CGPA
        exclude = ['person']
"""