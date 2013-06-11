"These are common usage functions for this site"
from ImageProcessingShow.models import Operation
from ImageProcessingShow import settings
ROOT_DIR = settings.ROOT_DIR

def get_attachments(label):
    return Operation.objects.get(label=label)

def get_codes(codes_path):
    codes = open(ROOT_DIR + codes_path).readlines()
    codes = '<br/>'.join(codes)
    codes = codes.replace(' ', '&nbsp;')
    return codes