from django.contrib import admin
from base.admin import BaseAdmin
from models import CWE, Report
from django.conf.urls import url
from django.http import Http404
from django.template.response import TemplateResponse
from ReportWriter import RESTAPI

@admin.register(Report)
class ReportAdmin(BaseAdmin):
    fields = ['name', 'title', 'description', 'cwes', 'misuse_case', 'use_case']
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

        cwes = [{'id': '1', 'code': '123', 'name': 'Authentication Bypass by Alternate Name'},
                {'id': '2', 'code': '456', 'name': 'Authentication Bypass by Spoofing'},
                {'id': '3', 'code': '789', 'name': 'Buffer Overflow'},
                {'id': '4', 'code': '987', 'name': 'Authentication Bypass by Wrong Name'},
                {'id': '5', 'code': '654', 'name': 'Invalid File Traversal'}]

        context = {'cwes': cwes}
        return TemplateResponse(request, "admin/report/report/cwe_suggestion.html", context)

    def misusecases_view(self, request):
        if request.method != 'POST':
            raise Http404("Invalid access using GET request!")

        RESTAPI.get_cwes_for_description('Authentication Bypass')

        misuse_cases = [{'id': '1', 'name': 'MU/00001', 'created_at': '07/01/2015', 'description': 'This is Misuse Case 1'},
                        {'id': '2', 'name': 'MU/00002', 'created_at': '07/02/2015', 'description': 'This is Misuse Case 2'},
                        {'id': '3', 'name': 'MU/00003', 'created_at': '07/03/2015', 'description': 'This is Misuse Case 3'},
                        {'id': '4', 'name': 'MU/00004', 'created_at': '07/04/2015', 'description': 'This is Misuse Case 4'},
                        {'id': '5', 'name': 'MU/00005', 'created_at': '07/05/2015', 'description': 'This is Misuse Case 5'},
                        {'id': '6', 'name': 'MU/00006', 'created_at': '07/06/2015', 'description': 'This is Misuse Case 6'}]
        context = {'misuse_cases': misuse_cases}

        return TemplateResponse(request, "admin/report/report/misusecase.html", context)


    def usecases_view(self, request):
        if request.method != 'POST':
            raise Http404("Invalid access using GET request!")

        #  Create a context with all the corresponding use cases
        use_cases = [{'id': '1', 'name': 'UC/00001', 'created_at': '07/01/2015', 'description': 'This is Use Cas 1', 'osr': 'This is OSR 1'},
                     {'id': '2', 'name': 'UC/00002', 'created_at': '07/02/2015', 'description': 'This is Use Cas 2', 'osr': 'This is OSR 2'},
                     {'id': '3', 'name': 'UC/00003', 'created_at': '07/03/2015', 'description': 'This is Use Cas 3', 'osr': 'This is OSR 3'},
                     {'id': '4', 'name': 'UC/00004', 'created_at': '07/04/2015', 'description': 'This is Use Cas 4', 'osr': 'This is OSR 4'},
                     {'id': '5', 'name': 'UC/00005', 'created_at': '07/05/2015', 'description': 'This is Use Cas 5', 'osr': 'This is OSR 5'}]
        context = {'use_cases': use_cases}

        return TemplateResponse(request, "admin/report/report/usecase.html", context)
