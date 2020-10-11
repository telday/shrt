
from url_app.views import index
from django.urls import path, include

urlpatterns = [
    path('', index),
]
