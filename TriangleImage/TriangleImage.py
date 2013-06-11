#coding:utf-8
from __future__ import division
import Image
from ImageProcessingShow import settings

def open_image(im_path, default_path):
    if not im_path:
        im_path = default_path
        im = Image.open(im_path)
    else:
        im = im_path if type(im_path) != type('') else Image.open(im_path)

    return im

class TriangleImage():
    STUFF_PATH = settings.STATICFILES_DIRS[0] +'/stuff'
    
    def triangle_image(self, im_path=None):
        im = open_image(im_path, self.STUFF_PATH + '/lena.jpg')
        pix = im.load()
        width,height = im.size
        im_new = Image.new('RGB', (width,height))
        pix_new = im_new.load()
        
        for x in range(width):
            for y in range(height):
                times = (x+1)/width
                m = x
                n = int(y/times)
                try:
                    pix_new[x,y] = pix[m,n]
                except:
                    pass
        
        return im_new

if __name__ == '__main__':
    im_new = TriangleImage().triangle_image()
    im_new.show()