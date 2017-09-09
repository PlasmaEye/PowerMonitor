from django.conf.urls import url

from . import views

app_name = 'monitor'
urlpatterns = [
    url(r'^(?P<meter_id>[0-9]+)$', views.index, name='monitor-index'),
    url(r'^(?P<meter_id>[0-9]+)/readings$', views.readings, name='monitor-readings')
]