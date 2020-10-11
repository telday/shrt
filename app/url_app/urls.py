
from url_app.views import *
from django.urls import path, include

urlpatterns = [
    path('', index),
    path('url/<str:id>', redirect_to_url),
]
