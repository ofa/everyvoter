"""kennedy URL Configuration"""
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic import TemplateView, RedirectView
from django.urls import reverse_lazy


admin.autodiscover()
admin.site.login = RedirectView.as_view(
    url=reverse_lazy('manage:manage_login'), query_string=True)
admin.site.logout = RedirectView.as_view(
    url=reverse_lazy('manage:manage_logout'), query_string=True)


# pylint: disable=invalid-name
urlpatterns = [
    url(
        r'^favicon.ico$',
        RedirectView.as_view(
            url=staticfiles_storage.url('img/favicons/favicon.ico'),
            permanent=False),
        name="favicon"
    ),

    # By default disable bots
    url(r'^robots\.txt$', TemplateView.as_view(
        template_name="robots.txt", content_type='text/plain')),

    url(r'^user/', include('accounts.urls', namespace='accounts')),
    url(r'^unsubscribe/',
        include('mailer.unsubscribe_urls', namespace='unsubscribe')),

    url(r'^api/', include('api.urls', namespace='api')),

    url(r'^aws_feedback/', include('feedback.urls', namespace='aws_feedback')),
    url(r'^hirefire/', include('hirefire.urls', namespace='hirefire')),

    url(r'^manage/admin/', admin.site.urls),
    url(r'^manage/', include('manage.urls', namespace='manage')),

    # Configuring 404 page in DEBUG mode is easier if it's available at `/404/`
    url(r'^404/$', TemplateView.as_view(template_name='404.html')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
