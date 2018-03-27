"""kennedy URL Configuration"""
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView


# pylint: disable=invalid-name
urlpatterns = [
    # By default disable bots
    url(r'^robots\.txt$', TemplateView.as_view(
        template_name="robots.txt", content_type='text/plain')),

    url(r'^user/', include('accounts.urls', namespace='accounts')),

    url(r'^admin/', admin.site.urls),

    # Configuring 404 page in DEBUG mode is easier if it's available at `/404/`
    url(r'^404/$', TemplateView.as_view(template_name='404.html')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
