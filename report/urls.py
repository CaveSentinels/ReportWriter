from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^report_list/$', views.report_list, name='report_list'),
    url(r'^(?P<pk>[0-9]+)/$', views.report_details, name='report_details'),
]