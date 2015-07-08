from django.contrib import admin
from base.admin import BaseAdmin
from django import forms
from models import CWE, Report


# class ReportForm(forms.ModelForm):
#     name = forms.CharField(label='Name', required=True)
#     title = forms.CharField(label='Title', required=True)
#     description = forms.CharField(label='Description', required=True)
#
#     class Meta:
#         model = Report
#         fields = ['name', 'title', 'description']

@admin.register(Report)
class ReportAdmin(BaseAdmin):
    fields = ['name', 'title', 'description']
    search_fields = ['title']

    # form = ReportForm

    # def get_fields(self, request, obj=None):
    #     if obj is None:
    #         return ['title', 'description']
    #     else:
    #         return super(ReportAdmin, self).get_fields(request, obj)