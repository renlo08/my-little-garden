from django.shortcuts import render

from gardens.models import Garden


# Create your views here.
def create_garden(request):
    """ Create a garden """
    context = {}
    if request.method == "POST":
        garden_name = request.POST.get("garden-name")
        garden_description = request.POST.get("garden-desc")
        garden_object = Garden.objects.create(name=garden_name, description=garden_description)
        context['object'] = garden_object
        context['created'] = True
    return render(request, 'gardens/create.html', context=context)

def garden_details(request, id: int = None):
    """
    Show the details of a garden
    :param id: the ID of the garden to detail.
    """
    garden_obj = Garden.objects.get(id=id) if id is not None else None
    context = {'object': garden_obj}
    return render(request, "gardens/details.html", context=context)
