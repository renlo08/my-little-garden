from django.urls import path

from activities import views
from app import utils

app_name = 'activities'

urlpatterns = [
    path('', views.ActivityDetailView.as_view(), name='index')
]

htmx_urlpatterns = [
]

urlpatterns = utils.arrange_urlpatterns(urlpatterns + htmx_urlpatterns)