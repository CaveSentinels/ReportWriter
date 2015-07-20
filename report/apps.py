from django.apps import AppConfig

class IssueReportConfig(AppConfig):
    name = 'report'
    verbose_name = "Report"

    def ready(self):
        # Importing autocomplete_registry only after models are ready and app is fully loaded
        import autocomplete_registry