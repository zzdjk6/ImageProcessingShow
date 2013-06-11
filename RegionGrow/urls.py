from django.conf.urls import patterns, url

urlpatterns = patterns('RegionGrow.views',
    url(r'^$', 'index'),
    url(r'^get_dealed_image/', 'get_dealed_image'),
)
