from django.conf.urls import patterns, include, url

urlpatterns = patterns('ErodeDilateImage.views',
    url(r'^$', 'index'),
    url(r'^get_dealed_image/', 'get_dealed_image'),
    #url(r'^online_dealing/$', 'online_dealing'),
)
