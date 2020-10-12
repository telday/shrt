import datetime
import re

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, Http404
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core import serializers

from url_api.models import URL

url_re = re.compile("http://*\.*")

# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
class URLAPI(View):

    http_methods = ['GET', 'POST', 'PATCH', 'DELETE']
    id = None
    redirect_url = None

    def get_expire_date(self):
        """Gets the expire date based off todays date. Links expire in 30 days"""
        expire_date = datetime.datetime.today() + datetime.timedelta(days=30)
        return expire_date

    def get_id_as_int(self, id):
        """Attempts to turn the base 35 id into an int

        Args:
            id: The base 35 url id to convert
        Returns:
            int the if it could be converted, HttpResponse if it failed
        """
        try:
            int_id = int(id, base=35)
        except ValueError as e:
            return HttpResponse("Invalid url id", status=400)
        return int_id

    def validate_redirect_url(self, url):
        """Makes sure the url is correctly formatted (has a http:// at the front and a .* at the end

        Args:
            url: The url to valdate
        Returns:
            None if url is valid, HttpResponse if it is invalid
        """
        match = url_re.match(url)
        if match is None:
            return HttpResponse("Invalid url", status=400)

    def get(self, request, id=None):
        """GETS the URL object given the base 35 int identifying it. We use the
        base 35 int in place of the actual primary key because it is user facing. We dont
        want the user to have to do conversions in javascript/other language before getting"""
        if id is None:
            return HttpResponse("Specify a url id", status=400)
        # We have to convert the id to an integer for django to find it in the database
        id = self.get_id_as_int(id)
        if id is HttpResponse:
            return id

        # this will either get the object or automatically return a 404 to user
        url = get_object_or_404(URL, pk=id)
        json_data = url.__dict__
        json_data.pop('_state')

        return JsonResponse(json_data)

    def post(self, request, *args, **kwargs):
        """Add a new URL to the database with the given redirect as a post form element"""
        if 'url' not in request.POST:
            return HttpResponse("You must specify a url!", status=400)
        # Links expire a month from creation
        expire_date = self.get_expire_date()
        redirect = request.POST.get('url')
        validated  = self.validate_redirect_url(redirect)
        if validated is not None:
            return validated
        new_url = URL(redirect=redirect, expired=expire_date, view_count=0)
        new_url.save()
        return HttpResponse(new_url.get_id_as_base(), status=200)

    def patch(self, request, id=None):
        """We only allow the user to update the redirect value of a URL. Then we update the
        expiry date to a month ahead"""
        if id is None or 'url' not in request.GET:
            return HttpResponse("You must specify a url id and new url", status=400)
        id = self.get_id_as_int(id)
        if id is HttpResponse:
            return id

        url = get_object_or_404(URL, pk=id)

        # make sure the url is actually valid
        new_redirect = request.GET.get('url')
        validated = self.validate_redirect_url(new_redirect)
        if validated is not None:
            return validated

        new_expire_date = self.get_expire_date()
        url.expire_date = new_expire_date
        url.view_count = 0
        url.redirect = new_redirect
        url.save()

        return HttpResponse(status=200)

    def delete(self, request, id=None):
        """Deletes a url given by the base 35 integer that identifies it. Again use the base 35 int
        here because it is user facing"""
        if id is None:
            return HttpResponse("You must specify a url id", status=400)
        id = self.get_id_as_int(id)
        if id is HttpResponse:
            return id

        url = get_object_or_404(URL, pk=id)
        url.delete()
        url.save()
        return HttpResponse(status=200)
