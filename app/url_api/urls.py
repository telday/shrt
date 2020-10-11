
from url_api.views import *
from django.urls import path, include
import url_api

urlpatterns = [
    path('', URLAPI.as_view()),
    path('<int:id>', URLAPI.as_view()),
]
