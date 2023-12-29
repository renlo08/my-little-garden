from django.urls import path

from gardens import views

app_name = 'gardens'

urlpatterns = [
    # path("", garden_list_view, name='list'),
    path("", views.GardenListView.as_view(), name='list'),
    # path("create/", views.garden_create_view, name='create'),
    # path("<int:id>/delete/", garden_delete_view, name='delete'),
    # path("<int:id>/edit/", garden_update_view, name='update'),
    # path("<int:id>/", garden_detail_view, name='detail'),
]

htmx_urlpatterns = [
    path('detail/<int:pk>/', views.detail, name='detail'),
    path('create/', views.GardenFormView.as_view(), name='create'),
]

urlpatterns += htmx_urlpatterns
