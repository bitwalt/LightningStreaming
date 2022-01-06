"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache

# These paths are for the Vue app - remove if you are not using the vue frontend, and create your custom views.
urlpatterns = [
    # http://localhost:8000/
    path('', never_cache(TemplateView.as_view(
        template_name='index.html')), name='index'),
    path('app.js', never_cache(TemplateView.as_view(
        template_name='app.js')), name='appjs'),
]
###

# These paths are for the api endpoints and admin interface.
urlpatterns += [
    # http://localhost:8000/api/<router-viewsets>
    path('api/v1.0/', include('backend.api.urls')),

    # http://localhost:8000/admin/
    path('admin/', admin.site.urls),
]
###


# Matches everything else, probably a Vue route?
# urlpatterns += [
#     re_path(r'(?P<url>)$', index_view, name='index-for-SPA'),
# ]
