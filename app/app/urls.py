"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from app import views as app_views
from accounts import views as account_views

urlpatterns = [
    path("", app_views.home_view, name='home'),
    path('gardens/', include('gardens.urls')),
    # path('gardens/', garden_views.garden_search_view, name='search-garden'),
    # path('gardens/create/', garden_views.garden_create_view, name='create-garden'),
    # path('gardens/<slug:slug>/', garden_views.garden_details_view, name='details-garden'),
    path('admin/', admin.site.urls),
    path('login/',account_views.login_view),
    path('logout/', account_views.logout_view),
    path('register/', account_views.register_view)
]
