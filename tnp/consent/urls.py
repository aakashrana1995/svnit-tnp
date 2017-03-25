from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login', views.login_user, name='login_user'),
    url(r'^create', views.create_account, name='create'),
    url(r'^home', views.home, name='home'),
    url(r'^apply', views.apply, name='apply'),
    url(r'^cancel', views.cancel, name='cancel'),
    url(r'^export', views.export_consent, name='export'),
    url(r'^logout/$', views.user_logout, name='logout'),
]
