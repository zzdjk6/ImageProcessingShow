from django.shortcuts import render_to_response
from django.http import HttpResponse
from ImageProcessingShow.common_functions import get_attachments,get_codes
from ErodeDilateImage import ErodeDilateImage

def index(request):
    attachments = get_attachments(label='erode_dilate')
    codes = get_codes('/ErodeDilateImage/ErodeDilateImage.py')
    return render_to_response('ErodeDilateImage/index.html',
                              {'attachments': attachments,
                               'codes': codes})

def get_dealed_image(request):
    method = int(request.GET.get('method'))
    template = request.GET.get('template')
    response = HttpResponse(mimetype='image/jpeg')
    dealer = ErodeDilateImage()
    
    template = [int(i) for i in template.split(',')]
    
    #pass function with dict!! it replaces switch-case perfectly!
    map_dict = {1: dealer.get_eroded_image,
                2: dealer.get_dilated_image,
                3: dealer.get_opened_image,
                4: dealer.get_closed_image}
    
    im_new = map_dict[method](template=template)
    im_new.save(response,'jpeg')
    return response

def online_dealing(request):
    return render_to_response('ErodeDilateImage/online_dealing.html')