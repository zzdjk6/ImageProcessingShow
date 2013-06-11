from django.http import HttpResponse
from django.shortcuts import render_to_response
from ImageProcessingShow.common_functions import get_attachments,get_codes
import InvertColor

def index(request):
    attachments = get_attachments('invert_color')
    codes = get_codes('/InvertColor/InvertColor.py')
    return render_to_response('InvertColor/index.html',
                              {'attachments': attachments,
                               'codes': codes})

def get_inverted_image(request):
    response = HttpResponse(mimetype='image/jpeg')
    im_copy = InvertColor.InvertColor().invert_color()
    im_copy.save(response,'jpeg')
    return response