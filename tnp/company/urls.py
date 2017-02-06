from django.conf.urls import url

from . import views
from consent import views as consent_views

urlpatterns = [
	url(r'^$', consent_views.home, name='home'),
	url(r'^(?P<job_slug>[\w\-]+)/$', views.job, name='job'),
]



