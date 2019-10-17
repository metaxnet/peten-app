from django.conf.urls import include, url
from django.urls import path

from django.contrib import admin
admin.autodiscover()

import hello.views

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^/?$',       hello.views.peten, name='peten'),
    url(r'^/?peten/?$', hello.views.peten, name='peten'),
    url(r'^/?real/?$', hello.views.peten_real, name='peten'),
    url(r'^/?peten/real/?$', hello.views.peten_real, name='peten'),
    url(r'^/?reactor/?$', hello.views.reactor, name='reactor'),
]
