from django.http import HttpResponse
from django.db.models import Q

import json

from emergency.models import Emergency_Group, Emergency
from emergency.models import Condition, Variety, Presenting_Complaint


mimetype = 'application/json'


def get_conditions_by_name(request):
    query = request.GET.get('term', '').capitalize()
    search_qs = Condition.objects.filter(name__startswith=query)
    results = []
    for r in search_qs:
        results.append(r.name)
    data = json.dumps(results)
    return HttpResponse(data, mimetype)
