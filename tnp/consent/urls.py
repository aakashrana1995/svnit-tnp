from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login', views.login_user, name='login_user'),
    url(r'^create', views.create_account, name='create'),
    url(r'^home', views.home, name='home'),
    url(r'^apply', views.apply, name='apply'),
    url(r'^cancel', views.cancel, name='cancel'),
    url(r'^export_resumes', views.export_resumes, name='export_resumes'),
    url(r'^export', views.export_consent, name='export'),
    url(r'^merit-list', views.merit_list, name='merit_list'),
    url(r'^logout/$', views.user_logout, name='logout'),
    # my work from here @abhishek981996
    url(r'^profile/view$', views.view_profile, name='profile'),
    url(r'^profile/edit$', views.edit_profile, name='edit_profile'),
    url(r'^profile/change-password$',
        views.change_password, name='change_password'),
]
