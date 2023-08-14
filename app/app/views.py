from django.shortcuts import render

from gardens.models import Garden


def home_view(request):
    context={}
    garden_qs = Garden.objects.all()
    context = {
        'garden_list': garden_qs
    }
    return render(request, 'index.html', context=context)