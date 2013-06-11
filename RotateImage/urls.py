from django.conf.urls import patterns, include, url

urlpatterns = patterns('RotateImage.views',
    url(r'^$', 'index'),
    url(r'^get_rotated_image/', 'get_rotated_image'),
)
