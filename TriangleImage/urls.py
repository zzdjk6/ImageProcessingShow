from django.conf.urls import patterns, include, url

urlpatterns = patterns('TriangleImage.views',
    url(r'^$', 'index'),
    url(r'^get_triangled_image', 'get_triangled_image'),
)
