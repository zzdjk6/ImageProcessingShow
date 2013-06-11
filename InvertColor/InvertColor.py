import Image
from ImageProcessingShow import settings

class InvertColor():
    "This class will invert the color of an image"
    STUFF_PATH = settings.STATICFILES_DIRS[0] +'/stuff'
    
    def invert_color(self, im_path=None, need_extra=False):
        if not im_path:
            im_path = self.STUFF_PATH + '/lena.jpg'
            
        im = Image.open(im_path)
        im_copy = im.copy()
        pix = im_copy.load()
        width,height = im_copy.size
        for x in range(width):
            for y in range(height):
                pix[x,y] = tuple(255-k for k in pix[x,y])
        
        result = (im,im_copy) if need_extra==True else im_copy
        return result
    
    def get_raw_image(self, im_path=None):
        if not im_path:
            im_path = self.STUFF_PATH + '/lena.jpg'
        return Image.open(im_path)

if __name__ == '__main__':
#    im, im_copy = InvertColor().invert_color(need_extra=True)
#    
#    im.show()
#    im_copy.show()

    im_copy = InvertColor().invert_color()
    im_copy.show()
    pass