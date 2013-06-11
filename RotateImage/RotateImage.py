#coding:utf-8
#opencv和一般的图像处理库不一样，它的x是纵轴，但实际上ｘ轴应该是横轴
import Image
import math
from ImageProcessingShow import settings
import ImageFilter

class RotateImage():
    STUFF_PATH = settings.STATICFILES_DIRS[0] +'/stuff'
    image = None
    
    def rotate_image(self, im_path=None, angle=30):
        if not im_path:
            im_path = self.STUFF_PATH + '/lena.jpg'
            
        angle = self._get_right_angle(angle)
        
        im = Image.open(im_path)
        self.image = im
        width,height = im.size
        pix = im.load()
 
        im_new = self._buildNewImage(angle)
        pix_new = im_new.load()
        move_distance = self._getMoveDistance(angle)
        for x in range(width):
            for y in range(height):
                i,j = self._rotatePointMoving((x,y), angle, move_distance)
                try:
                    pix_new[i,j] = pix[x,y]
                except:
                    pass
        
        return im_new
        #return im_new.filter(ImageFilter.MedianFilter)
    
    def _get_right_angle(self,angle):
        while angle < 0:
            angle += 360
        while angle > 360:
            angle -= 360
        return angle
    
    def _rotatePointNormal(self,point,angle):
        anglePi = angle * math.pi/180.0 #角度变弧度
        x0,y0 = point
        x1 = int(math.cos(anglePi) * x0 + math.sin(anglePi) * y0)
        y1 = int(-math.sin(anglePi) * x0 + math.cos(anglePi) * y0)
        return (x1,y1)
    
    def _rotatePointMoving(self,point,angle,move_distance):
        point = self._rotatePointNormal(point, angle)
        point = (point[0] + move_distance[0], point[1] + move_distance[1])
        return point
    
    def _getMoveDistance(self,angle):
        width,height = self.image.size
        A = (0,0)
        B = (width,0)
        C = (width,height)
        D = (0,height)
        
        A_ = (0,0)
        B_ = self._rotatePointNormal(B, angle)
        C_ = self._rotatePointNormal(C, angle)
        D_ = self._rotatePointNormal(D, angle)
        
        #condition: 0 < angle <= 90
        if 0<=angle<=90:
            x_move = 0
            y_move = abs(B_[1] - 0)
        elif 90<angle<=180:
            x_move = abs(B_[0] - 0)
            y_move = abs(C_[1] - 0)
        elif 180<angle<=270:
            x_move = abs(C_[0] - 0)
            y_move = abs(D_[1] - 0)
        elif 270<angle<=360:
            x_move = abs(D_[0] - 0)
            y_move = 0
        else:
            raise Exception("Wrong angle!")
        return (x_move,y_move)
    
    def _buildNewImage(self, angle):
        width,height = self.image.size
        A = (0,0)
        B = (width,0)
        C = (width,height)
        D = (0,height)
        
        A_ = (0,0)
        B_ = self._rotatePointNormal(B, angle)
        C_ = self._rotatePointNormal(C, angle)
        D_ = self._rotatePointNormal(D, angle)
        
        if 0<=angle<=90:
            new_width = abs(C_[0])
            new_height = abs(B_[1] - D_[1])
        elif 90<angle<=180:
            new_width = abs(B_[0] - D_[0])
            new_height = abs(C_[1])
        elif 180<angle<=270:
            new_width = abs(C_[0])
            new_height = abs(B_[1] - D_[1])
        elif 270<angle<=360:
            new_width = abs(B_[0]-D_[0])
            new_height = abs(C_[1])
        else:
            raise Exception("Wrong angle!")
            
        new_size = (new_width,new_height)
        return Image.new('RGB', new_size)

if __name__ == '__main__':
    im_new = RotateImage().rotate_image(angle=30)
    im_new.show()
    