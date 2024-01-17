from app import utils

app_name = 'activities'

urlpatterns = [
]

htmx_urlpatterns = [
]

urlpatterns = utils.arrange_urlpatterns(urlpatterns + htmx_urlpatterns)