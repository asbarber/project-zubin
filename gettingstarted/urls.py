from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

import src.views

urlpatterns = [
    url(r'^$', src.views.index, name='index')
]
