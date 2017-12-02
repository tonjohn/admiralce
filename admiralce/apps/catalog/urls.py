from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^(?P<slug>[-\w\d]+)/$', views.view_sitter, name='profile'),
    url(r'^courses/$', views.CourseListView.as_view(), name='course-list'),
    url(r'^course/(?P<pk>\d+)$', views.CourseDetailView.as_view(), name='course-detail'),
]
