import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core import serializers

from url_api.models import URL

# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
class URLAPI(View):

    http_methods = ['GET', 'POST', 'PATCH', 'DELETE']

    def get(self, request, id=None):
        if id is None:
            return HttpResponse("Specify a url id", status=400)
        id = int(id, base=35)
        url = get_object_or_404(URL, pk=id)
        json_data = url.__dict__
        json_data.pop('_state')

        return JsonResponse(json_data)

    def post(self, request, *args, **kwargs):
        if 'url' not in request.POST:
            return HttpResponse("You must specify a url!", status=400)
        # Links expire a month from creation
        expire_date = datetime.datetime.today() + datetime.timedelta(days=30)
        new_url = URL(redirect=request.POST.get('url'), expired=expire_date, view_count=0)
        new_url.save()
        return HttpResponse(new_url.get_id_as_base(), status=200)

    def patch(self, request, *args, **kwargs):
        return HttpResponse(status=200)

    def delete(self, request, id=None):
        if id is None:
            return HttpResponse("You must specify a url id", status=400)
        id = int(id, base=35)
        url = get_object_or_404(URL, pk=id)
        url.delete()
        url.save()
        return HttpResponse(status=200)
