from django.contrib import admin
from base.admin import BaseAdmin
from django import forms
from models import CWE, Report
from django.contrib import admin
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.admin.templatetags.admin_urls import add_preserved_filters
from models import *
from django.http import HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist




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
    search_fields = ['title','status']
    list_display = ['title', 'status']
    readonly_fields = ['name', 'status']


    # form = ReportForm

    # def get_fields(self, request, obj=None):
    #     if obj is None:
    #         return ['title', 'description']
    #     else:
    #         return super(ReportAdmin, self).get_fields(request, obj)

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

