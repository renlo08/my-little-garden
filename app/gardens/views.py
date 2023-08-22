from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from gardens.forms import GardenForm
from gardens.models import Garden


# Create your views here.
@login_required
def create_garden_view(request):
    """ Create a garden """
    form = GardenForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        garden_object = form.save()
        context['form'] = GardenForm()
    return render(request, "gardens/create.html", context=context)

def garden_overview_view(request):
    context = {}
    garden_qs = Garden.objects.all()
    context = {
        'gardens': garden_qs
    }
    return render(request, "gardens/garden_overview.html", context=context)
def search_garden_view(request):
    """ Search a garden """
    query_dict = request.GET
    try:
        query = int(query_dict.get('q'))
    except:
        query = None
    garden_obj = Garden.objects.get(id=query) if query is not None else None
    context = {"object": garden_obj}
    return render(request, "gardens/search.html", context=context)

def garden_details_view(request, _id: int =None):
    """
    Show the details of a garden
    :param request: the GET request
    :param _id: the ID of the garden to detail.
    """
    garden_obj = Garden.objects.get(id=_id) if _id is not None else None
    context = {'object': garden_obj}
    return render(request, "gardens/details.html", context=context)
