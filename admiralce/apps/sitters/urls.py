from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<slug>[-\w\d]+)/$', views.view_sitter, name='profile')
]
