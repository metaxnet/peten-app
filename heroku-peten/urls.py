from django.urls import include, re_path
from django.urls import path

from django.contrib import admin
admin.autodiscover()

import hello.views

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    re_path(r'^$',       hello.views.peten, name='peten'),
    re_path(r'^peten/?$', hello.views.peten, name='peten'),
    re_path(r'^real/?$', hello.views.peten_real, name='peten'),
    re_path(r'^peten/real/?$', hello.views.peten_real, name='peten'),
    re_path(r'^reactor/?$', hello.views.reactor, name='reactor'),
]
