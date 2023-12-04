from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from gardens.forms import GardenForm
from gardens.models import Garden


@login_required
def garden_list_view(request):
    qs = Garden.objects.filter(user=request.user)
    context = {
        'object_list': qs
    }
    return render(request, 'gardens/list.html', context=context)


@login_required
def garden_detail_view(request, id=None):
    obj = get_object_or_404(Garden, id=id, user=request.user)
    context = {
        "object": obj
    }
    return render(request, 'gardens/detail.html', context=context)


@login_required
def garden_create_view(request):
    form = GardenForm(request.POST or None)
    context = {
        'form': form
    }
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        return redirect(obj.get_absolute_url())
    return render(request, 'gardens/create-update.html', context=context)


@login_required
def garden_update_view(request, id=None):
    obj = get_object_or_404(Garden, id=id, user=request.user)
    form = GardenForm(request.POST or None, instance=obj)
    context = {
        "form": form,
        "object": obj,
    }
    if form.is_valid():
        form.save()
        context['message'] = 'Data saved.'
    return render(request, "gardens/create-update.html", context)


@login_required
def garden_delete_view(request, id=None):
    try:
        obj = Garden.objects.get(id=id, user=request.user)
    except:
        obj = None
    if obj is None:
        raise Http404
    if request.method == "POST":
        obj.delete()
        success_url = reverse('gardens:list')
        return redirect(success_url)
    context = {
        "object": obj
    }
    return render(request, "gardens/delete.html", context)
