from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'ImageProcessingShow.views.index'),
    url(r'^invert_color/', include('InvertColor.urls')),
    url(r'^scale/', include('ScaleImage.urls')),
    url(r'^rotate/', include('RotateImage.urls')),
    url(r'^erode_dilate/', include('ErodeDilateImage.urls')),
    url(r'^triangle/', include('TriangleImage.urls')),
#    url(r'^histogram/', include('HistogramImage.urls')),
    url(r'^filters/', include('Filters.urls')),
#    url(r'^binary/', include('BinaryImage.urls')),
    url(r'^region_grow/', include('RegionGrow.urls')),
    url(r'^get_operation_list$', 'ImageProcessingShow.views.get_operations'),
    # Examples:
    # url(r'^$', 'ImageProcessingShow.views.home', name='home'),
    # url(r'^', include('ImageProcessingShow.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
