# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView

from activities.models import Activity
from gardens.models import Garden


class ActivityDetailView(LoginRequiredMixin, DetailView):
    template_name = 'activities/activities.html'
    model = Garden
    context_object_name = 'garden'
    slug_url_kwarg = 'garden_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activities'] = Activity.objects.filter(garden=self.object)
        context['address'] = self.object.address
        return context
