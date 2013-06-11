from django.shortcuts import render_to_response
from django.http import HttpResponse
from ImageProcessingShow.common_functions import get_attachments,get_codes
from RegionGrow import RegionGrow

def index(request):
    attachments = get_attachments(label='region_grow')
    codes = get_codes('/RegionGrow/RegionGrow.py')
    return render_to_response('RegionGrow/index.html',
                              {'attachments': attachments,
                               'codes': codes})

def get_dealed_image(request):
    length = int(request.GET.get('length',None))
    threshold = int(request.GET.get('threshold',50))
    seeds = []
    for i in range(length):
        x = int(request.GET.get('x%s'%i,None))
        y = int(request.GET.get('y%s'%i,None))
        seeds.append((x,y))
    
    response = HttpResponse(mimetype='image/jpeg')
#    im_new = RegionGrow().region_grow(seeds=seeds)
    im_new = RegionGrow().region_grow(seeds=seeds,threshold=threshold)
    im_new.save(response,'jpeg')
    return response