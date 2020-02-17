from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('wiki_bot', csrf_exempt(views.WikiBotView.as_view())),
]
