from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^registration_process$', views.registration),
    url(r'^login_process$', views.login),
    url(r'^dashboard$', views.dashboard),
    url(r'^logout$', views.logout),
    url(r'^create_trip$', views.create_trip),
    url(r'^create_trip_cancel$', views.create_trip_cancel),
    url(r'^create_trip_process$', views.create_trip_process),
    url(r'^edit_trip/(?P<trip_id>\d+)$', views.edit_trip),
    url(r'^update_trip_process/(?P<trip_id>\d+)$', views.update_trip_process),
    url(r'^remove_trip/(?P<trip_id>\d+)$', views.remove_trip),
    url(r'^join_trip/(?P<trip_id>\d+)$', views.join_trip),
    url(r'^cancel_trip/(?P<trip_id>\d+)$', views.cancel_trip),
    url(r'^trip_info/(?P<trip_id>\d+)$', views.trip_info),
]
