from django.urls import path

from gardens import views, utils

app_name = 'gardens'

urlpatterns = [
    path("", views.GardenListView.as_view(), name='list'),
    path('create/', views.GardenFormView.as_view(), name='create'),
    path('<str:slug>/', views.GardenDetailView.as_view(), name='detail'),
    path('<str:slug>/edit/', views.GardenUpdateView.as_view(), name='edit'),
]

htmx_urlpatterns = [
    path('char_count/', views.char_count, name='char-count'),
    path('<str:slug>/delete/', views.garden_delete_view, name='delete'),
    path('search/', views.search_garden_view, name='search'),
    # path('activities/')
]

urlpatterns = utils.arrange_urlpatterns(urlpatterns + htmx_urlpatterns)
