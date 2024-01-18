from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView

from gardens.forms import GardenForm
from gardens.models import Garden


class GardenFormView(CreateView):
    template_name = 'gardens/create-update.html'
    form_class = GardenForm
    success_url = reverse_lazy('gardens:list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['address'] = self.object.address
        return context


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
    form_class = GardenForm
    template_name = 'gardens/create-update.html'
    success_url = reverse_lazy('gardens:list')


def garden_name_length_view(request):
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

