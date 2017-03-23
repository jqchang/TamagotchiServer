from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^register$', views.firstLogin),
    url(r'^api/berrylist$', views.apiList),
    url(r'^pickup$', views.pickup),
    url(r'^debug$', views.debug)
]
