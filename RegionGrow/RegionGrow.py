#coding:utf-8
from PIL import Image
from ImageProcessingShow import settings

class RegionGrow:
    
    STUFF_PATH = settings.STATICFILES_DIRS[0] +'/stuff'
    
    def __init__(self):
        #注意seeds_history在这里应该声明为实例属性，而不是类属性
        self.seeds_history = list()
    
    def region_grow(self,seeds=None,threshold=50):
        if not seeds:
            raise Exception
        
        im_raw = Image.open(self.STUFF_PATH+'/Regiongrowing_figure_Original.jpg').convert('L')
        im = im_raw.copy()
        pix = im.load()
        width,height = im.size
        
        for i in seeds:
            x,y = i
            pix[x,y] = 255
        
        while len(seeds) != 0:
            seed = seeds.pop()
            if seed not in self.seeds_history:
                self.seeds_history.append(seed)
            x,y = seed
            pending = ((x+1,y),(x-1,y),(x,y+1),(x,y-1))
            for cor in pending:
                if self._validate(cor,pix,threshold):
                    seeds.append(cor)
                    pix[cor] = 255
        
        print len(self.seeds_history)

#        这个循环效率太低,用下面那个代替(吼吼，算法优化真开心，耗时从7秒降至1秒不到～)
#        for i in range(width):
#            for j in range(height):
#                if (i,j) not in self.seeds_history:
#                    pix[i,j] = 0

        self.seeds_history.sort()
        k = 0
        length_of_history = len(self.seeds_history)
        for i in range(width):
            for j in range(height):
                if k < length_of_history and (i,j) == self.seeds_history[k]:
                    k += 1
                else:
                    pix[i,j] = 0
        return im
    
    def _validate(self,cor,pix,threshold):
        x,y = cor
        if cor not in self.seeds_history and 255 - pix[x,y] < threshold:
            return True
        else:
            return False

if __name__ == "__main__":
    pass
    #regionGrow = RegionGrow()
    im = RegionGrow().region_grow([(216,194),(206,63)],50)
    im.show()
    im_new = RegionGrow().region_grow([(206,63)],100)
    im_new.show()
    