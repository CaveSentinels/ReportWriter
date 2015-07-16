from ReportWriter.rest_api import rest_api
from django.core.exceptions import ValidationError
from django.contrib import admin
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.admin.templatetags.admin_urls import add_preserved_filters
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.template.response import TemplateResponse
from django.conf.urls import url
import autocomplete_light
from models import *
from django.utils.safestring import mark_safe
from django.http import HttpResponseRedirect
from base.admin import BaseAdmin



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


@admin.register(IssueReport)
class IssueReportAdmin(BaseAdmin):
    form = autocomplete_light.modelform_factory(IssueReport, fields="__all__")
    fields = [('name', 'status'), 'type', 'report', 'report_duplicate', 'description',
              ('created_by', 'created_at'), ('reviewed_by', 'reviewed_at'), 'resolve_reason']
    readonly_fields = ['name', 'status', 'created_by', 'created_at', 'reviewed_by', 'reviewed_at', 'resolve_reason']
    list_display = ['name', 'type', 'created_by', 'created_at', 'status',]
    search_fields = ['name', 'created_by__name']
    list_filter = ['type', 'status']
    date_hierarchy = 'created_at'


    def get_fields(self, request, obj=None):
        """ Override to hide the 'usecase_duplicate' if type is not 'duplicate' """
        fields = super(IssueReportAdmin, self).get_fields(request, obj)

        if obj and obj.type != 'duplicate' and 'report_duplicate' in fields:
            fields.remove('report_duplicate')

        return fields


    def get_urls(self):
        urls = super(IssueReportAdmin, self).get_urls()
        info = self.model._meta.app_label, self.model._meta.model_name

        my_urls = [

            url(r'new_report/$', self.admin_site.admin_view(self.new_report_view), name='%s_%s_new_report' % info),
            url(r'add_report/$', self.admin_site.admin_view(self.render_add_report), name='%s_%s_add_report' % info),
        ]
        return my_urls + urls


    def new_report_view(self, request):
        """
        This view is called by muo search using ajax to display the report issue popup
        """
        if request.method == "POST":
            # read the usecase_id that triggered this action
            report_id = request.POST.get('report_id')
            report = get_object_or_404(Report, pk=report_id)

            # Render issue report form and default initial values, if any
            ModelForm = self.get_form(request)
            initial = self.get_changeform_initial_data(request)
            initial['report'] = report
            form = ModelForm(initial=initial)

            context = dict(
                # Include common variables for rendering the admin template.
                self.admin_site.each_context(request),
                form=form,
                report=report,
            )
            return TemplateResponse(request, "admin/report/issuereport/new_report.html", context)
        else:
            raise Http404("Invalid access using GET request!")


    def render_add_report(self, request):
        """
        Handle adding new report created using muo search popup
        """

        if request.method == 'POST':

            ModelForm = self.get_form(request)
            form = ModelForm(request.POST, request.FILES)
            if form.is_valid():
                new_object = form.save()
                self.message_user(request, "Report %s has been created will be reviewed by our reviewers" % new_object.name , messages.SUCCESS)
            else:
                # submitted form is invalid
                errors = ["%s: %s" % (form.fields[field].label, error[0]) for field, error in form.errors.iteritems()]
                errors = '<br/>'.join(errors)
                self.message_user(request, mark_safe("Invalid report content!<br/>%s" % errors) , messages.ERROR)

            # Go back to misuse case view
            opts = self.model._meta
            post_url = reverse('admin:%s_%s_changelist' %
                               (opts.app_label, 'issuereport'),
                               current_app=self.admin_site.name)
            preserved_filters = self.get_preserved_filters(request)
            post_url = add_preserved_filters({'preserved_filters': preserved_filters, 'opts': opts}, post_url)

            return HttpResponseRedirect(post_url)

        else:
            raise Http404("Invalid access using GET request!")


    def response_change(self, request, obj, *args, **kwargs):
        '''
        Override response_change method of admin/options.py to handle the click of
        newly added buttons
        '''

        # Get the metadata about self (it tells you app and current model)
        opts = self.model._meta

        # Get the primary key of the model object i.e. Issue Report
        pk_value = obj._get_pk_val()

        preserved_filters = self.get_preserved_filters(request)

        redirect_url = reverse('admin:%s_%s_change' %
                                   (opts.app_label, opts.model_name),
                                   args=(pk_value,))
        redirect_url = add_preserved_filters({'preserved_filters': preserved_filters, 'opts': opts}, redirect_url)

        # Check which button is clicked, handle accordingly.
        try:
            if "_investigate" in request.POST:
                obj.action_investigate(request.user)
                msg = "The issue is now being investigated."

            elif "_resolve" in request.POST:
                resolve_reason = request.POST.get('resolve_reason_text', '')
                obj.action_resolve(resolve_reason,request.user)
                msg = "The issue is now resolved because  " + resolve_reason

            elif "_reopen" in request.POST:
                obj.action_reopen(request.user)
                msg = "The issue has been re-opened."

            elif "_open" in request.POST:
                obj.action_open(request.user)
                msg = "The issue is now opened."

        except ValueError as e:
            # In case the state of the object is not suitable for the corresponding action,
            # model will raise the value exception with the appropriate message. Catch the
            # exception and show the error message to the user
            msg = e.message
            self.message_user(request, msg, messages.ERROR)

        self.message_user(request, msg, messages.SUCCESS)
        return HttpResponseRedirect(redirect_url)
