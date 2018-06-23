from django.conf.urls import url

from . import views
from consent import views as consent_views

urlpatterns = [
	url(r'^$', consent_views.home, name='home'),
	url(r'^add', views.add, name='add'),
	url(r'^companies', views.companies_list, name='companies'),
	url(r'^profiles', views.profiles_list, name='profiles'),
	url(r'^(?P<job_slug>[\w\-]+)/$', views.job, name='job'),
]



