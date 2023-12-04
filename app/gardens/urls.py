from django.urls import path

from gardens.views import (
    garden_list_view,
    garden_detail_view,
    garden_create_view,
    garden_update_view,
    garden_delete_view
)

app_name = 'gardens'

urlpatterns = [
    path("", garden_list_view, name='list'),
    path("create/", garden_create_view, name='create'),
    path("<int:id>/delete/", garden_delete_view, name='delete'),
    path("<int:id>/edit/", garden_update_view, name='update'),
    path("<int:id>/", garden_detail_view, name='detail')
]
