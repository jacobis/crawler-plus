from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='base.html')),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('google_plus',
    url(r'^google_plus/activities/$', 'views.activities'),
    url(r'^google_plus/fetch_json/$', 'views.fetch_json'),
    url(r'^google_plus/parse_object/$', 'views.parse_object'),
    url(r'^google_plus/activities/csv/$', 'views.activities_csv'),
)

# Uncomment the next line to serve media files in dev.
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
                            url(r'^__debug__/', include(debug_toolbar.urls)),
                            )
