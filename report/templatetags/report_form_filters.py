#in templatetags/user_list_tags.py
from django import template
from crispy_forms.templatetags.crispy_forms_filters import as_crispy_field
register = template.Library()

@register.filter(name='as_report_field')
def as_report_field(field):
    return  as_crispy_field(field)

#
# @register.filter(name='as_crispy_field')
# def as_crispy_field(field, template_pack=TEMPLATE_PACK):
#     """
#     Renders a form field like a django-crispy-forms field::
#
#         {% load crispy_forms_tags %}
#         {{ form.field|as_crispy_field }}
#
#     or::
#
#         {{ form.field|as_crispy_field:"bootstrap" }}
#     """
#     if not isinstance(field, forms.BoundField) and DEBUG:
#         raise CrispyError('|as_crispy_field got passed an invalid or inexistent field')
#
#     template = get_template('%s/field.html' % template_pack)
#     c = Context({'field': field, 'form_show_errors': True, 'form_show_labels': True})
#     return template.render(c)