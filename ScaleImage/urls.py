from django.conf.urls import patterns, include, url

urlpatterns = patterns('ScaleImage.views',
    url(r'^$', 'index'),
    url(r'^get_scaled_image/', 'get_scaled_image'),
)
