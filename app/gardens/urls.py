from django.urls import path

from gardens import views

app_name = 'gardens'

urlpatterns = [
    path("", views.GardenListView.as_view(), name='list'),
    path('create/', views.GardenFormView.as_view(), name='create'),
    path('<str:slug>/edit/', views.GardenUpdateView.as_view(), name='edit'),
]

htmx_urlpatterns = [
    path('char_count/', views.char_count, name='char-count'),
    path('<str:slug>/delete/', views.garden_delete_view, name='delete'),
    path('<str:slug>detail/', views.detail, name='detail'),
    path('search/', views.search_garden_view, name='search')
]

urlpatterns += htmx_urlpatterns
