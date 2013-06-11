from django.shortcuts import render_to_response
from django.http import HttpResponse
from ImageProcessingShow.common_functions import get_attachments,get_codes
from Filters import Filters

def index(request):
    attachments = get_attachments(label='filters')
    codes = get_codes('/Filters/Filters.py')
    return render_to_response('Filters/index.html',
                              {'attachments': attachments,
                               'codes': codes})

def get_dealed_image(request):
    method = int(request.GET.get('method'))
    response = HttpResponse(mimetype='image/jpeg')
    dealer = Filters()

    #pass function with dict!! it replaces switch-case perfectly!
    map_dict = {1: dealer.box_filter,
                2: dealer.median_filter,
                3: dealer.roberts,
                4: dealer.sobel,
                5: dealer.laplacian}
    
    if method == 5:
        template = request.GET.get('template')
        template = [int(i) for i in template.split(',')]
        im_new = map_dict[method](template=template)
    else:
        im_new = map_dict[method]()
        
    im_new.save(response,'jpeg')
    return response