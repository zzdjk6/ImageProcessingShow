import Image
from ImageProcessingShow import settings

class ShowImage():
    "This class will load an Image and show it"
    STUFF_PATH = settings.STATICFILES_DIRS[0] +'/stuff'
    
    def show_image(self, im_path=None):
        if not im_path:
            im_path = self.STUFF_PATH + '/lena.jpg'
        
        im = Image.open(im_path)
        return im
    
if __name__ == "__main__":
    im = ShowImage().show_image()
    im.show()