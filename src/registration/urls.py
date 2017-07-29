from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^register', views.register, name="ntpc.register"),
    url(r'^login', views.login, name="ntpc.login"),
    url(r'^signin', views.signin),
    url(r'^members', views.members),
    url(r'^logout', views.logUserOut),
    url(r'^', views.home)
]