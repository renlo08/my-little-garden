from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, CreateView

from gardens.forms import GardenForm, FertilizationForm
from gardens.models import Garden, FertilizationInline


class GardenFormView(CreateView):
    template_name = 'gardens/partials/create.html'
    form_class = GardenForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


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


@login_required
def amendment_update_view(request, garden_slug:str = None, id: int=None):
    if not request.htmx:
        raise Http404("HTMX requesst not found.")

    try:
        garden = Garden.objects.get(slug__exact=garden_slug, user=request.user)
    except Garden.DoesNotExist:
        raise Http404("Garden not found.")

    try:
        instance = FertilizationInline.objects.get(garden=garden, id=id)
    except FertilizationInline.DoesNotExist:
        return HttpResponse(status=404, content_type="text/plain", content="No Fertilization Information")

    if request.method == "PUT":
        form = FertilizationForm(request.PUT, instance=instance)

@login_required
def garden_amendment_update_hx_view(request, parent_id=None, id=None):
    if not request.htmx:
        raise Http404("HTMX request not found")

    # Retrieve the Garden instance
    try:
        parent_obj = Garden.objects.get(id=parent_id, user=request.user)
    except Garden.DoesNotExist:
        raise Http404("Garden not found")

    # Retrieve the FertilizationInline instance
    try:
        instance = FertilizationInline.objects.get(id=id, garden=parent_obj)
    except FertilizationInline.DoesNotExist:
        return HttpResponse(status=404, content_type="text/plain", content="No Fertilization Information")

    # Handle the form submission
    if request.method == "POST":
        form = FertilizationForm(request.POST, instance=instance)
        if not form.is_valid():
            return HttpResponseBadRequest("Invalid form data")
    else:
        form = FertilizationForm(instance=instance)

    return render(request, 'gardens/partials/fertilization-form.html', context={'form': form})


class GardenListView(ListView):
    template_name = 'gardens/gardens.html'
    model = Garden
    context_object_name = 'gardens'

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return user.gardens.all()
        else:
            return Garden.objects.none()


@login_required
def detail(request, pk: int):
    garden = get_object_or_404(Garden, pk=pk, user=request.user)
    return render(request, 'gardens/partials/detail.html', {'garden': garden})