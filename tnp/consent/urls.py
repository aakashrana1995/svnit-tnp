from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login', views.login_user, name='login_user'),
    url(r'^home', views.home, name='home'),
    url(r'^logout/$', views.user_logout, name='logout'),
]
