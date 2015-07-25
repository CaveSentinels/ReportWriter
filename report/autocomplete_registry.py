from .models import *
import autocomplete_light

class IssueReportAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields = ['id', 'name']
    attrs = {'placeholder': 'Report...'}
    model = Report
    widget_attrs = {
        'class': 'modern-style',
    }

autocomplete_light.register(IssueReportAutocomplete)


