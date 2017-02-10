from django.forms import ModelForm, Textarea

from django.utils.translation import ugettext_lazy as _


from company.models import Company, Job, JobLocation, Attachment 
from consent.models import ConsentDeadline


class CompanyForm(ModelForm):
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
            'infra_req': Textarea(),
        }
        

class JobForm(ModelForm):
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

# Need to be a formset
class JobLocationForm(ModelForm):
    class Meta:
        model = JobLocation
        fields = ['location']

        labels = {
            'location': _('Job Location')
        }



class ConsentDeadlineForm(ModelForm):
    class Meta:
        model = ConsentDeadline
        fields = ['deadline', 'slack_time']

        labels = {
            'deadline': _('Consent Deadline'),
            'slack_time': _('Slack Time'),
        }


class AttachmentForm(ModelForm):
    class Meta:
        model = Attachment
        fields = ['file']