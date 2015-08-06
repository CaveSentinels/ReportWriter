from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/$', views.report_details, name='report_details'),
    url(r'^report_list/$', views.report_list, name='report_list'),
    url(r'^create_issue_report/$', views.create_issue_report, name='create_issue_report'),
    url(r'^process_issue_report/$', views.process_issue_report, name='process_issue_report'),

]