from django.shortcuts import render_to_response
from models import Operation
from ImageProcessingShow.common_functions import get_attachments,get_codes

def index(request):
    attachments = get_attachments('index')
    codes = get_codes('/ShowImage/ShowImage.py')
    return render_to_response('index.html',
                              {'attachments': attachments,
                               'codes': codes})

def get_operations(request):
    operation_list = Operation.objects.all()
    return render_to_response('operations.html',{'operation_list':operation_list})