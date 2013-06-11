from django.conf.urls import patterns, include, url

urlpatterns = patterns('InvertColor.views',
    url(r'^$', 'index'),
    url(r'^ajax_invert$', 'get_inverted_image'),
)
