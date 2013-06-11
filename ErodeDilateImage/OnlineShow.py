#coding:utf-8
from PIL import Image
from ImageProcessingShow import settings
from os.path import dirname
import sqlite3

ROOT_PATH = dirname(dirname(__file__))
    
def open_image(im_path=None, default_path=ROOT_PATH+'/static/stuff/lena_copy.ppm'):
    if not im_path:
        im = Image.open(default_path).convert('L')
    else:
        im = im_path if type(im_path) != type('') else Image.open(im_path).convert('L')

    pix = im.load()
    width,height = im.size
    
    #二值化一把
    for x in range(width):
        for y in range(height):
            if pix[x,y] < 127:
                pix[x,y] = 0
            else:
                pix[x,y] = 255
    return im
    
class ErodeDilateImage:
    
    STUFF_PATH = settings.STATICFILES_DIRS[0] +'/stuff'
    
    def __init__(self):
        DB_PATH = ROOT_PATH + '/database/onlineshow_1.db3'
        self.dbn = sqlite3.connect(DB_PATH)
        
    
    def get_eroded_image(self, im_path=None, template=[1,1,1,1,1,1,1,1,1]):
        im = open_image()
        pix = im.load()
        width,height = im.size
        
        im_new = im.copy()
        pix_new = im_new.load() 
        
        query_string_base = "INSERT INTO operation_log \
                                    values('%s','%s','%s','%s','%s','%s','%s','%s')"
        query_string = ''
        grid = [0]*9
        step_id = 0
        for x in range(width):
            for y in range(height):                
                if x in [0,width-1] or y in [0,height-1]:
                    #边界点
                    query_string = query_string_base % (step_id,x,y,pix_new[x,y],pix_new[x,y],1,'erode','')
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
                        #符合模板条件，保留点
                        query_string = query_string_base % (step_id,x,y,pix_new[x,y],255,3,
                                                            'erode',','.join([str(i) for i in grid]))
                        pix_new[x,y] = 255
                    else:
                        #不符合模板条件，腐蚀点
                        query_string = query_string_base % (step_id,x,y,pix_new[x,y],0,2,
                                                            'erode',','.join([str(i) for i in grid]))
                        pix_new[x,y] = 0
                    
                self.dbn.cursor().execute(query_string)
                step_id += 1
        self.dbn.commit()
        return im_new
    
    def get_dilated_image(self, im_path=None, template=[1,1,1,1,1,1,1,1,1]):
        im = open_image()
        im_new = im.copy()
        pix = im.load()
        pix_new = im_new.load()
        width,height = im.size
        
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
    
    def get_state_of_step(self, step_id):
        dbcursor = self.dbn.cursor()
        dbcursor.execute("select * from operation_log where step_id=?",(step_id,))
        row = dbcursor.next()
        _,x,y,old_value,new_value,remark_id,operation_type,grid = tuple(row)
        dbcursor.execute("select remark from remark where remark_id=?",(remark_id,))
        remark = dbcursor.next()[0]
        state = {'x':x, 'y':y, 'old_value':old_value, 'new_value':new_value,
                 'remark':remark, 'operation_type':operation_type,'grid':grid}
        return state
    
    def render_to_step(self, step_id, im_path=None):
        im = open_image()
        pix = im.load()
        width,height = im.size
        
        for i in range(step_id):
            state = self.get_state_of_step(i)
            x = state['x']
            y = state['y']
            pix[x,y] = state['new_value']
 
        return im
    
    def render_a_step(self, image, step_id):
        pix = image.load()
        state = self.get_state_of_step(step_id)
        x,y,new_value = state['x'],state['y'],state['new_value']
        pix[x,y] = new_value
        return image
    
if __name__ == '__main__':
    pass
    erodeDilateImage = ErodeDilateImage()
    
#    im = erodeDilateImage.get_raw_image()
#    im.show()
#    im_erode = erodeDilateImage.get_eroded_image()
#    im_erode.show()
    im_dilate = erodeDilateImage.get_dilated_image()
    im_dilate.show()
#    im_open = erodeDilateImage.get_opened_image()
#    im_open.show()
#    im_close = erodeDilateImage.get_closed_image()
#    im_close.show()