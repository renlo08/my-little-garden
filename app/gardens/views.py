from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView

from gardens.forms import GardenForm, FertilizationForm
from gardens.models import Garden, FertilizationInline


class GardenFormView(CreateView):
    template_name = 'gardens/create-update.html'
    form_class = GardenForm
    success_url = reverse_lazy('gardens:list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


@login_required
def garden_create_view(request):
    form = GardenForm(request.POST or None)
    context = {
        'form': form
    }
    if form.is_valid():
        obj = form.save(commit=False)
        obj.created_by = request.user
        obj.save()
        return redirect(obj.get_absolute_url())
    return render(request, 'gardens/create-update.html', context=context)


@login_required
def garden_update_view(request, id=None):
    obj = get_object_or_404(Garden, id=id, created_by=request.user)
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
def amendment_update_view(request, garden_slug:str = None, id: int=None):
    if not request.htmx:
        raise Http404("HTMX requesst not found.")

    try:
        garden = Garden.objects.get(slug__exact=garden_slug, created_by=request.user)
    except Garden.DoesNotExist:
        raise Http404("Garden not found.")

    try:
        instance = FertilizationInline.objects.get(garden=garden, id=id)
    except FertilizationInline.DoesNotExist:
        return HttpResponse(status=404, content_type="text/plain", content="No Fertilization Information")

    if request.method == "PUT":
        form = FertilizationForm(request.PUT, instance=instance)


class GardenListView(LoginRequiredMixin, ListView):
    template_name = 'gardens/gardens.html'
    model = Garden
    context_object_name = 'gardens'

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return user.gardens.all()
        else:
            return Garden.objects.none()


class GardenDetailView(LoginRequiredMixin, DetailView):
    template_name = 'gardens/details.html'
    model = Garden
    context_object_name = 'garden'


@login_required
def garden_delete_view(request, slug: str):
    if not request.htmx:
        raise Http404('Delete Garden is not HTMX requested. Invalid request')
    garden = get_object_or_404(Garden, slug=slug, created_by=request.user)
    if request.method == 'POST':
        garden.delete()
        # Get all gardens after delete
        gardens = Garden.objects.filter(created_by=request.user)
        context = {'gardens': gardens}
        return render(request, "gardens/partials/cards.html", context)
    return render(request, "gardens/delete.html", {"garden": garden})


class GardenUpdateView(LoginRequiredMixin, UpdateView):
    model = Garden
    fields = ['name', 'description']
    template_name = 'gardens/create-update.html'
    success_url = reverse_lazy('gardens:list')


def char_count(request):
    text = request.POST.get('name', '')
    count = len(text)
    return HttpResponse(f"{count} / {Garden._meta.get_field('name').max_length} caractères.")


@login_required
def search_garden_view(request):
    card_search = request.GET.get('garden-search', None)
    if card_search:  # Search functionality
        context = {'is_search': True}
        gardens = Garden.objects.search(card_search)
    else:  # Clear functionality
        context = {'is_search': False}
        gardens = Garden.objects.all()
    context['gardens'] = gardens
    return render(request, "gardens/partials/cards.html", context=context)
