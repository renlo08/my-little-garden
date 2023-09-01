from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect

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

def garden_details_view(request, slug=None):
    """
    Show the details of a garden
    :param request: the GET request
    :param slug: the slug of the garden to detail.
    """
    garden_obj = None
    if slug is not None:
        try:
            garden_obj = Garden.objects.get(slug=slug)
        except Garden.DoesNotExist:
            raise Http404
        except Garden.MultipleObjectsReturned:
            garden_obj = Garden.objects.filter(slug=slug).first()
        except:
            raise Http404
    context = {
        "object": garden_obj
    }
    return render(request, "gardens/details.html", context=context)

def remove_garden(request, slug=None):
    garden_obj = None
    if slug is not None:
        try:
            garden_obj = Garden.objects.get(slug=slug)
        except Garden.DoesNotExist:
            raise Http404
        except Garden.MultipleObjectsReturned:
            garden_obj = Garden.objects.filter(slug=slug).first()
        except:
            raise Http404
        garden_obj.delete()
    return redirect('/gardens')
