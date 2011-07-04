from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'items.views.index'),
    (r'^todos\/?(?P<item_id>\d*)$', 'items.views.restful'),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/django/todos/items/static/'}),
    (r'^admin/', include(admin.site.urls)),
)

