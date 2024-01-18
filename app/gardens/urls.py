from django.urls import path, include

from app import utils
from gardens import views

app_name = 'gardens'

urlpatterns = [
    path("", views.GardenListView.as_view(), name='list'),
    path('create/', views.GardenFormView.as_view(), name='create'),
    path('<str:slug>/', views.GardenDetailView.as_view(), name='detail'),
    path('<str:slug>/edit/', views.GardenUpdateView.as_view(), name='edit'),
    path('<str:garden_slug>/activities/', include('activities.urls'), name='activities')
]

htmx_urlpatterns = [
    path('name_length/', views.garden_name_length_view, name='length-name'),
    path('search/', views.search_garden_view, name='search'),
    path('<str:slug>/delete/', views.garden_delete_view, name='delete'),
]

urlpatterns = utils.arrange_urlpatterns(urlpatterns + htmx_urlpatterns)
