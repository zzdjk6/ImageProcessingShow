from django.http import HttpResponse
from django.shortcuts import render_to_response
from ImageProcessingShow.common_functions import get_attachments,get_codes
from TriangleImage import TriangleImage

def index(request):
    attachments = get_attachments('triangle_image')
    codes = get_codes('/TriangleImage/TriangleImage.py')
    return render_to_response('TriangleImage/index.html',
                              {'attachments': attachments,
                               'codes': codes})

def get_triangled_image(request):
    response = HttpResponse(mimetype='image/jpeg')
    im_copy = TriangleImage().triangle_image()
    im_copy.save(response,'jpeg')
    return response