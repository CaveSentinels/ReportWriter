from django.http import HttpResponseForbidden, Http404
from django.db.models import Q
import operator
from django.template.response import TemplateResponse
from report.models import Report


def report_list(request):
    """
    This view is called by reports search using ajax to get the list of reports for a given search query
    """
    if not request.is_ajax():
        return HttpResponseForbidden()

    term = request.POST.get('term')
    query = []

    if term:
        if term.isdigit():
            query.append(Q(pk__exact=term))
            query.append(Q(cwes__code__exact=term))

        query.append(Q(name__icontains=term))
        query.append(Q(title__icontains=term))
        query.append(Q(description__icontains=term))
        query.append(Q(cwes__name__icontains=term))

        reports = Report.objects.filter(status='approved').filter(reduce(operator.or_, query)).distinct()
    else:
        reports = Report.objects.filter(status='approved')

    context = {'reports': reports}

    return TemplateResponse(request, "report/report_list.html", context)


def report_details(request, pk):
    report = Report.objects.get(pk=pk, status='approved')
    if not report:
        return Http404()

    context = {'report': report}
    return TemplateResponse(request, "report/report_details.html", context)
