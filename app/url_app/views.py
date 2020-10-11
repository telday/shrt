
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from url_api.models import URL

# Create your views here.
def index(request):
    return render(request, 'index.html', dict())

def redirect_to_url(request, id):
    id_int = int(id, base=35)
    url = get_object_or_404(URL, pk=id_int)
    url.view_count += 1
    url.save()

    return redirect(url, permanent=True)
