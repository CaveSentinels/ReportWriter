'''
+This file will contain all the custom template tags for the
+Invitation app.
+'''

from django.contrib.admin.templatetags.admin_modify import *
from base.templatetags.admin_modify import submit_row as original_submit_row
from django import template

register = template.Library()


@register.inclusion_tag('admin/invitation/invitation_submit_line.html', takes_context=True)
def invitation_submit_row(context):
    ctx = original_submit_row(context)

    model_object = ctx.get('original')
    ctx.update({
        'show_invite': context['add'],
        'show_re_invite': context['change'] and model_object and model_object.status == 'pending',
    })

    return ctx
