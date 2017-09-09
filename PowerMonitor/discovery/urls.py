from django.conf.urls import url

from . import views

app_name = 'discovery'
urlpatterns = [
    url(r'^$', views.index, name='discovery-index'),
    url(r'^meters$', views.meters, name='discovery-meters'),
]