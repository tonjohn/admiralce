"""rover URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import RedirectView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('apps.ce_ledger.urls')),
    url(r'^catalog/', include('apps.catalog.urls')),
    #url(r'^search/', include('apps.search.urls', namespace="search")),
    #url(r'^members/', include('apps.sitters.urls', namespace="sitter")),
    #url(r'^$', RedirectView.as_view(url='/search/')),
]

# Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    url('^auth/', include('django.contrib.auth.urls', namespace="auth")),
]
