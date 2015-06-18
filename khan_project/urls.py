from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'khan_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'khan_project.views.home', name='home'),
    #url(r'^suggest_exercises/$', 'exercises.views.suggest_exercises', name='suggest_exercises'),
    url(r'^exercises/',include('exercises.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}), )
