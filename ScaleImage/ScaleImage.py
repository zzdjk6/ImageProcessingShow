import Image
from ImageProcessingShow import settings

class ScaleImage():
    STUFF_PATH = settings.STATICFILES_DIRS[0] +'/stuff'
    
    def scale_image(self, im_path=None, method=1, times=1):
        if not im_path:
            im_path = self.STUFF_PATH + '/lena.jpg'
            
        im = Image.open(im_path)
        pix = im.load()
        
        times = float(times)
        width,height = im.size
        width = int(width * times)
        height = int(height * times)
        im_new = Image.new('RGB', (width,height))
        pix_new = im_new.load()
        
        if method == 1:
            for x in range(width):
                for y in range(height):
                    m = int(x/times)
                    n = int(y/times)
                    pix_new[x,y] = pix[m,n]
        elif method == 2:
            for x in range(width-1):
                for y in range(height-1):
                    #f(i+u,j+v) = (1-u)(1-v)f(i,j) + 
                    #             (1-u)vf(i,j+1) + 
                    #             u(1-v)f(i+1,j) + 
                    #             uvf(i+1,j+1)
                    m = x/times
                    n = y/times
                    i = int(m)
                    j = int(n)
                    u = m - i
                    v = n - j
                    A = pix[i,j]
                    B = pix[i,j+1]
                    C = pix[i+1,j]
                    D = pix[i+1,j+1]
                
                    new_point = [0,0,0]
                    for k in range(3):
                        new_point[k]= (1-u) * (1-v) * A[k] + \
                                            (1-u) * v * B[k] + \
                                            u * (1-v) * C[k] + \
                                            u * v * D[k]
                        new_point[k] = int(new_point[k])
                    pix_new[x,y] = tuple(new_point)
        
        return im_new

if __name__ == '__main__':
    im_new = ScaleImage().scale_image(method=2, times=1.5)
    im_new.show()
    im_new2 = ScaleImage().scale_image(method=1, times=1.5)
    im_new2.show()