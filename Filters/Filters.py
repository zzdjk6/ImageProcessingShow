#coding:utf-8
from PIL import Image
from ImageProcessingShow import settings

STUFF_PATH = settings.STATICFILES_DIRS[0] +'/stuff'

#这个Filters类里面的函数都是独立的，想看面向对象封装的同学
#请往下拉到FilterBase类(面向对象封装后，每个滤波器只要写自己特别的那一部分就可以了)
class Filters:
    
    def add_noise(self):
        from random import randint
        im = Image.open(STUFF_PATH+'/lena.jpg')
        pix = im.load()
        width,height = im.size
        
        for x in range(width):
            for y in range(height):
                r = randint(0,100)
                if r > 97:
                    pix[x,y] = (255,255,255)
                elif r < 3:
                    pix[x,y] = (0,0,0)
        #im.save(STUFF_PATH+'/lena_noise.jpg')
        return im
    
    
    def median_filter(self):
        im = Image.open(STUFF_PATH+'/lena_noise.jpg')
        pix = im.load()
        im_new = im.copy()
        pix_new = im_new.load()
        width,height = im.size
        
        for x in range(width):
            for y in range(height):
                try:
                    grid = []
                    for i in [x-1,x,x+1]:
                        for j in [y-1,y,y+1]:
                            grid.append(pix[i,j])
                    grid.sort()
                    pix_new[x,y] = grid[4]
                except IndexError:
                    pix_new[x,y] = (0,0,0)
        
        return im_new
    
    def box_filter(self):
        im = Image.open(STUFF_PATH+'/lena_noise.jpg')
        pix = im.load()
        im_new = im.copy()
        pix_new = im_new.load()
        width,height = im.size
        
        for x in range(width):
            for y in range(height):
                try:
                    grid = []
                    for i in [x-1,x,x+1]:
                        for j in [y-1,y,y+1]:
                            grid.append(pix[i,j])
                    sumv = [0,0,0]
                    for pix_value in grid:
                        sumv[0] += pix_value[0]
                        sumv[1] += pix_value[1]
                        sumv[2] += pix_value[2]
                    pix_new[x,y] = tuple([value/9 for value in sumv])
                except IndexError:
                    pix_new[x,y] = (0,0,0)
        
        return im_new
    
    #注意sobel和roberts都是交叉算子
    def sobel(self):
        im = Image.open(STUFF_PATH+'/lena_grey.jpg')
        pix = im.load()
        im_new = im.copy()
        pix_new = im_new.load()
        width,height = im.size
        
        template1 = [-1,-2,-1,0,0,0,1,2,1]
        template2 = [-1,0,1,-2,0,2,-1,0,1]
        for x in range(width):
            for y in range(height):
                try:
                    gx = 0
                    gy = 0
                    grid = []
                    for j in [y-1,y,y+1]:
                        for i in [x-1,x,x+1]:
                            grid.append(pix[i,j])
                    for i,v in enumerate(grid):
                        gx += template1[i] * v
                        gy += template2[i] * v
                    pix_new[x,y] = abs(gx) + abs(gy)
                except:
                    pix_new[x,y] = 0
        return im_new
    
    def roberts(self):
        im = Image.open(STUFF_PATH+'/lena_grey.jpg')
        pix = im.load()
        im_new = im.copy()
        pix_new = im_new.load()
        width,height = im.size
        
        template1 = [-1,0,0,1]
        template2 = [0,-1,1,0]
        for x in range(width):
            for y in range(height):
                try:
                    gx = 0
                    gy = 0
                    grid = []
                    for j in [y,y+1]:
                        for i in [x,x+1]:
                            grid.append(pix[i,j])
                    for i,v in enumerate(grid):
                        gx += template1[i] * v
                        gy += template2[i] * v
                    pix_new[x,y] = abs(gx) + abs(gy)
                except:
                    pix_new[x,y] = 0
        return im_new
    
    def laplacian(self,template=[0,1,0,1,-4,1,0,1,0]):
        im = Image.open(STUFF_PATH+'/lena_grey.jpg')
        pix = im.load()
        im_new = im.copy()
        pix_new = im_new.load()
        width,height = im.size
        for x in range(width):
            for y in range(height):
                try:
                    grid = []
                    for j in [y-1,y,y+1]:
                        for i in [x-1,x,x+1]:
                            grid.append(pix[i,j])
                    new_value = 0
                    for i,v in enumerate(grid):
                        new_value += template[i] * v
                    pix_new[x,y] = new_value
                except:
                    pix_new[x,y] = 0
        return im_new

#下面是面向对象封装的滤波器函数
#这个FilterBase是基类，继承之后覆盖deal_every_loop函数就可以
#后面给了一个NoiseFilter的例子和MedianFilter的例子
class FilterBase:
    
    def deal_every_loop(self,x=None,y=None,pix=None,pix_new=None):
        return None
    
    def loop_over_image(self,path):
        im,pix,im_new,pix_new,width,height = self.get_stuff(path)
        for x in range(width):
            for y in range(height):
                res = self.deal_every_loop(x=x,y=y,pix=pix,pix_new=pix_new)
                if res:
                    pix_new[x,y] = res
        return im_new
    
    def get_stuff(self,path):
        im = Image.open(path)
        pix = im.load()
        im_new = im.copy()
        pix_new = im_new.load()
        width,height = im.size
        return im,pix,im_new,pix_new,width,height

class NoiseFilter(FilterBase):
    
    def deal_every_loop(self,x=None,y=None,pix=None,pix_new=None):
        from random import randint
        r = randint(0,100)
        if r > 97:
            res = (255,255,255)
        elif r < 3:
            res = (0,0,0)
        else:
            res = None
        return res

class MedianFilter(FilterBase):
    
    def deal_every_loop(self, x=None, y=None, pix=None, pix_new=None):
        try:
            grid = []
            for i in [x-1,x,x+1]:
                for j in [y-1,y,y+1]:
                    grid.append(pix[i,j])
            grid.sort()
            return grid[4]
        except IndexError:
            return (0,0,0)

    
if __name__ == '__main__': 
    pass   
#    filters = Filters()
#    filters.add_noise().show()
#    filters.median_filter().show()
#    filters.box_filter().show()
#    Image.open(STUFF_PATH+'/lena.jpg').convert('L').show()
#    filters.sobel().show()
#    filters.roberts().show()
#    filters.laplacian().show()
#    filters.laplacian(template=[1,1,1,1,-8,1,1,1,1]).show()
#    filters.laplacian(template=[0,-1,0,-1,4,-1,0,-1,0]).show()
#    filters.laplacian(template=[-1,-1,-1,-1,8,-1,-1,-1,-1]).show()

#    NoiseFilter().loop_over_image(path=STUFF_PATH+'/lena.jpg').show()
#    MedianFilter().loop_over_image(path=STUFF_PATH+'/lena_noise.jpg').show()