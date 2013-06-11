#coding:utf-8
from PIL import Image
from ImageProcessingShow import settings
    
def open_image(im_path, default_path):
    if not im_path:
        im_path = default_path
        im = Image.open(im_path)
    else:
        im = im_path if type(im_path) != type('') else Image.open(im_path)

    return im
    
class ErodeDilateImage:
    
    STUFF_PATH = settings.STATICFILES_DIRS[0] +'/stuff'
    
    def get_eroded_image(self, im_path=None, template=[1,1,1,1,1,1,1,1,1]):
        im = open_image(im_path, self.STUFF_PATH + '/lena.jpg').convert('L')
        im_new = im.copy()
        pix = im.load()
        pix_new = im_new.load()
        width,height = im.size
        
        for x in range(width):
            for y in range(height):
                if pix[x,y] < 127:
                    pix[x,y] = 0
                    pix_new[x,y] = 0
                else:
                    pix[x,y] = 255
                    pix_new[x,y] = 255
                
        
        grid = [0]*9
        for x in range(width):
            for y in range(height):                
                if x in [0,width-1] or y in [0,height-1]:
                    pix_new[x,y] = pix[x,y]
                else:
                    grid[0] = pix[x-1,y-1]
                    grid[1] = pix[x,y-1]
                    grid[2] = pix[x+1,y-1]
                    grid[3] = pix[x-1,y]
                    grid[4] = pix[x,y]
                    grid[5] = pix[x+1,y]
                    grid[6] = pix[x-1,y+1]
                    grid[7] = pix[x,y+1]
                    grid[8] = pix[x+1,y+1]
                    
                    flag = 1
                    for m in range(9):
                        if template[m] == 1:
                            if grid[m] != 255:
                                flag = 0
                                break
                    if flag == 1:
                        pix_new[x,y] = 255
                    else:
                        pix_new[x,y] = 0
        return im_new
    
    def get_dilated_image(self, im_path=None, template=[1,1,1,1,1,1,1,1,1]):
        im = open_image(im_path, self.STUFF_PATH + '/lena.jpg').convert('L')
        im_new = im.copy()
        pix = im.load()
        pix_new = im_new.load()
        width,height = im.size
        
        for x in range(width):
            for y in range(height):
                if pix[x,y] < 127:
                    pix[x,y] = 0
                    pix_new[x,y] = 0
                else:
                    pix[x,y] = 255
                    pix_new[x,y] = 255
        
        grid = [0]*9
        for x in range(width):
            for y in range(height):
                if x in [0,width-1] or y in [0,height-1]:
                    pix_new[x,y] = pix[x,y]
                else:
                    grid[0] = pix[x-1,y-1]
                    grid[1] = pix[x,y-1]
                    grid[2] = pix[x+1,y-1]
                    grid[3] = pix[x-1,y]
                    grid[4] = pix[x,y]
                    grid[5] = pix[x+1,y]
                    grid[6] = pix[x-1,y+1]
                    grid[7] = pix[x,y+1]
                    grid[8] = pix[x+1,y+1]
                    
                    flag = 1
                    for m in range(9):
                        if template[m] == 1:
                            if grid[m] == 255:
                                flag = 0
                                break
                    if flag == 1:
                        pix_new[x,y] = 0
                    else:
                        pix_new[x,y] = 255
        return im_new
    
    def get_opened_image(self, im_path=None, template=[1,1,1,1,1,1,1,1,1]):
        return self.get_dilated_image(self.get_eroded_image(im_path, template), template)
    
    def get_closed_image(self, im_path=None, template=[1,1,1,1,1,1,1,1,1]):
        return self.get_eroded_image(self.get_dilated_image(im_path, template), template)
    
    def get_raw_image(self, im_path=None):
        im = open_image(im_path, self.STUFF_PATH + '/lena.jpg').convert('L')
        pix = im.load()
        width,height = im.size
        
        for x in range(width):
            for y in range(height):
                if pix[x,y] < 127:
                    pix[x,y] = 0
                else:
                    pix[x,y] = 255
        #im.save(self.STUFF_PATH + '/lena_binary_raw.jpg','jpeg')
        return im
    
if __name__ == '__main__':
    pass
    erodeDilateImage = ErodeDilateImage()
    im = erodeDilateImage.get_raw_image()
    im.show()
    im_erode = erodeDilateImage.get_eroded_image()
    im_erode.show()
    im_dilate = erodeDilateImage.get_dilated_image()
    im_dilate.show()
    im_open = erodeDilateImage.get_opened_image()
    im_open.show()
    im_close = erodeDilateImage.get_closed_image()
    im_close.show()