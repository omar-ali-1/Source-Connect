from sourcebasesite.views import home
from django.conf.urls import url

app_name = 'sourcebasesite'
urlpatterns = [
    url(r'^$', home, name='home'),
]