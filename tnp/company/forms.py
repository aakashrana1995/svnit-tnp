from django import forms

from django.utils.translation import ugettext_lazy as _

from tnp.settings import TIME_INPUT_FORMATS, DATE_INPUT_FORMATS

from company.models import Company, Job, JobLocation, Attachment 
from consent.models import ConsentDeadline


class CompanyForm(forms.ModelForm):
    crpdate = forms.DateField(input_formats=DATE_INPUT_FORMATS, required=False)
    class Meta:
        model = Company
        exclude = ['created_at', 'updated_at']
        labels = {
            'name': _('Company Name'),
            'website': _('Website (start with "http://")'),
            'about': _('About Company'),
            'infra_req': _('Infrastructure Requirements'),
            'other': _('Other Details'),
            'crpdate': _('Campus Recruitment Date'),
        }
        widgets = {
            'infra_req': forms.Textarea(),
        }
        

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        exclude = ['company', 'slug', 'created_at', 'updated_at']

        labels = {
            'designation': _('Job Profile'),
            'description': _('Job Description'),
            'requirements': _('Job Requirements / Skills'),
            'perks': _('Job Perks'),
            'category': _('Job Category'),
            'job_type': _('Job Type'),
            'eligible_branches': _('Eligible Branches'),
            'eligibility_criteria': _('Eligibility Criteria'),
            'ctc': _('CTC (in lpa)'),
            'ctc_details': _('CTC Details / Breakup'),
            'bond_details': _('Bond Details (if any)'),
            'selection_procedure': _('Selection Procedure'),
            'number_of_selections': _('Expected Number of Selections'),
            'other': _('Other details (if any)'),
        }


class AttachmentForm(forms.Form):
    file = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'multiple': True}))


class ConsentDeadlineForm(forms.Form):
    deadline_date = forms.DateField(input_formats=DATE_INPUT_FORMATS)
    deadline_time = forms.TimeField(input_formats=TIME_INPUT_FORMATS)
    slack_time = forms.IntegerField(initial='0')

    labels = {
        'deadline_date': _('Consent Deadline'),
        'deadline_time': _('Time'),
        'slack_time': _('Slack Time (in hours)'),
    }


"""
# Need to be a formset
class JobLocationForm(forms.ModelForm):
    class Meta:
        model = JobLocation
        fields = ['location']

        labels = {
            'location': _('Job Location')
        }


class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ['file']

"""