from django.contrib import admin
from base.admin import BaseAdmin
from models import Category, CWE, MisuseCase, UseCase, Report


@admin.register(Category)
class CategoryAdmin(BaseAdmin):
    fields = ['name']
    search_fields = ['name']


@admin.register(Report)
class ReportAdmin(BaseAdmin):
    fields = ['name', 'title', 'description']
    search_fields = ['title', 'reliability']

    def get_fields(self, request, obj=None):
        if obj is None:
            return ['title', 'description']
        else:
            return super(ReportAdmin, self).get_fields(request, obj)