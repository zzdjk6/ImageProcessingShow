from django.shortcuts import render_to_response
from django.http import HttpResponse
from RotateImage import RotateImage
from ImageProcessingShow.common_functions import get_attachments,get_codes

def index(request):
    attachments = get_attachments(label='rotate_image')
    codes = get_codes('/RotateImage/RotateImage.py')
    return render_to_response('RotateImage/index.html',
                              {'attachments': attachments,
                               'codes': codes})

def get_rotated_image(request):
    angle = int(request.GET.get('angle'))
    response = HttpResponse(mimetype='image/jpeg')    
    im_new = RotateImage().rotate_image(angle=angle)
    im_new.save(response,'jpeg')
    return response