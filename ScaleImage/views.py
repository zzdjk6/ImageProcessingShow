from django.shortcuts import render_to_response
from django.http import HttpResponse
from ScaleImage import ScaleImage
from ImageProcessingShow.common_functions import get_attachments,get_codes

def index(request):
    attachments = get_attachments(label='scale_image')
    codes = get_codes('/ScaleImage/ScaleImage.py')
    return render_to_response('ScaleImage/index.html',
                              {'attachments': attachments,
                               'codes': codes})

def get_scaled_image(request):
    method = int(request.GET.get('method'))
    times = float(request.GET.get('times'))
    response = HttpResponse(mimetype='image/jpeg')
    
    if method not in [1,2] or times > 2 or times < 0.1:
        return response
    
    im_new = ScaleImage().scale_image(method=method,times=times)
    im_new.save(response,'jpeg')
    return response