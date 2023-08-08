from django.http import HttpResponse
from django.shortcuts import render, redirect

from tasks.models import Garden


# Create your views here.


def index(request):
    context = {}
    context['gardens'] = Garden.objects.order_by("name")
    return render(request, "tasks/index.html", context=context)


def add_garden(request):
    collection_name = request.POST.get("garden-name")
    Garden.objects.create(name=collection_name)
    return redirect('home')
