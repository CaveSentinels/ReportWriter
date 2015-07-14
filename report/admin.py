from crispy_forms.bootstrap import UneditableField
from django.contrib import admin
from django.forms import ModelForm
from base.admin import BaseAdmin
from models import CWE, Report
from django.conf.urls import url
from django.http import Http404
from django.template.response import TemplateResponse
from django.utils.text import capfirst
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div
from ReportWriter.rest_api import rest_api

@admin.register(Report)
class ReportAdmin(BaseAdmin):
    # fields = ['name', 'title', 'description', 'cwes', 'misuse_case', 'use_case']
    # readonly_fields = ['name']
    search_fields = ['title']

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['for_review'] = True

        if object_id is not None:
            # Change form
            extra_context['for_review'] = True

        return super(ReportAdmin, self).changeform_view(request, object_id, form_url, extra_context)


    def get_urls(self):
        urls = super(ReportAdmin, self).get_urls()

        additional_urls = [
            url(r'report_report_cwes/$', self.admin_site.admin_view(self.cwe_view)),
            url(r'report_report_misusecases/$', self.admin_site.admin_view(self.misusecases_view)),
            url(r'report_report_usecases/$', self.admin_site.admin_view(self.usecases_view)),
        ]

        return additional_urls + urls

    def cwe_view(self, request):
        if request.method != 'POST':
            raise Http404("Invalid access using GET request!")

        if request.description is None or request.description == '':
            # Raise an exception from here
            pass
        else:
            # Get the suggested CWEs for the description from Enhanced CWE application
            cwes = rest_api.get_cwes_for_description('Authentication Bypass')

        # cwes = [{'id': '1', 'code': '123', 'name': 'Authentication Bypass by Alternate Name'},
        #         {'id': '2', 'code': '456', 'name': 'Authentication Bypass by Spoofing'},
        #         {'id': '3', 'code': '789', 'name': 'Buffer Overflow'},
        #         {'id': '4', 'code': '987', 'name': 'Authentication Bypass by Wrong Name'},
        #         {'id': '5', 'code': '654', 'name': 'Invalid File Traversal'}]

        context = {'cwes': cwes}
        return TemplateResponse(request, "admin/report/report/cwe_suggestion.html", context)

    def misusecases_view(self, request):
        if request.method != 'POST':
            raise Http404("Invalid access using GET request!")

        misuse_cases = rest_api.get_misuse_cases('123,345,567')

        if misuse_cases['success'] is False:
            # There was some error and the REST call was not successful
            # TODO Handle Error
            pass

        # Set the context
        context = {'misuse_cases': misuse_cases['obj']}

        return TemplateResponse(request, "admin/report/report/misusecase.html", context)


    def usecases_view(self, request):
        if request.method != 'POST':
            raise Http404("Invalid access using GET request!")

        selected_misuse_case_id = request.POST['misuse_case_id']

        use_cases = rest_api.get_use_cases(selected_misuse_case_id)

        if use_cases['success'] is False:
            # There was some error and the REST call was not successful
            # TODO Handle Error
            pass

        context = {'use_cases': use_cases['obj']}

        return TemplateResponse(request, "admin/report/report/usecase.html", context)
