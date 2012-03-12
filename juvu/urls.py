from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'splash.views.splash', name='splash'),
    url(r'^uh$', 'splash.views.record_email', name='record_email'),

    # Static media (should be served directly by the web server in production.)
    (
        r'^static/(?P<path>.*)$',
        'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT},
        ),

)