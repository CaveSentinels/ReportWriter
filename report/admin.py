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
from django.contrib import admin
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.admin.templatetags.admin_urls import add_preserved_filters
from models import *
from django.http import HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

@admin.register(Report)
class ReportAdmin(BaseAdmin):
    exclude = ['created_at', 'created_by', 'modified_by']
    search_fields = ['title']
    list_display = ['name', 'status']

    def is_readonly(self, obj, user):
        '''
        returns a boolean value indicating whether change form should be readonly or not. Change form is always readonly
        except when it is in draft state and the current user is the author of the report or the user has the
        'can_edit_all' permission
        '''
        return obj.status == 'draft' and (user == obj.created_by or user.has_perm('report.can_edit_all'))

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        # Override changeform_view to decide if the if the form should be read only or not. Also pass the read only
        # variable in the context

        extra_context = extra_context or {}

        if object_id is not None:
            # Change form. Check if the change form should be editable or readonly

            # Get the current model instance
            current_model_instance = Report.objects.get(pk=object_id)

            # Get the current User
            current_user = request.user

            extra_context['read_only'] = self.is_readonly(current_model_instance, current_user)

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


    def response_change(self, request, obj, *args, **kwargs):
        '''
        Override response_change method of admin/options.py to handle the click of
        newly added buttons
        '''

        # Get the metadata about self (it tells you app and current model)
        opts = self.model._meta

        # Get the primary key of the model object i.e. MUO Container
        pk_value = obj._get_pk_val()

        preserved_filters = self.get_preserved_filters(request)

        redirect_url = reverse('admin:%s_%s_change' %
                                   (opts.app_label, opts.model_name),
                                   args=(pk_value,))
        redirect_url = add_preserved_filters({'preserved_filters': preserved_filters, 'opts': opts}, redirect_url)

        # Check which button is clicked, handle accordingly.
        try:
            if "_approve" in request.POST:
                obj.action_approve(request.user)
                msg = "You have approved the submission"

            elif "_reject" in request.POST:
                reject_reason = request.POST.get('reject_reason_text', '')
                obj.action_reject(reject_reason, request.user)
                msg = "The submission has been sent back to the author for review"

            elif "_submit_for_review" in request.POST:
                obj.action_submit()
                msg = "Your review request has been successfully submitted"

            elif "_edit" in request.POST:
                obj.action_save_in_draft()
                msg = "You can now edit the Report"

            else:
                # Let super class 'ModelAdmin' handle rest of the button clicks i.e. 'save' 'save and continue' etc.
                return super(ReportAdmin, self).response_change(request, obj, *args, **kwargs)
        except ValueError as e:
            # In case the state of the object is not suitable for the corresponding action,
            # model will raise the value exception with the appropriate message. Catch the
            # exception and show the error message to the user
            msg = e.message
            self.message_user(request, msg, messages.ERROR)
            return HttpResponseRedirect(redirect_url)
        except ValidationError as e:
            # If incomplete MUO Container is attempted to be approved or submitted for review, a validation error will
            # be raised with an appropriate message
            msg = e.message
            self.message_user(request, msg, messages.ERROR)
            return HttpResponseRedirect(redirect_url)

        self.message_user(request, msg, messages.SUCCESS)
        return HttpResponseRedirect(redirect_url)
