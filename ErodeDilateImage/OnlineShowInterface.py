#coding:utf-8
from Tkinter import *

def callback(event):
    print event.x,event.y

root = Tk()
frame1 = Frame(root)
frame2 = Frame(root)
frame3 = Frame(root)

#frame1
imgobj = PhotoImage(file='/home/csh/Projects/ImageProcessingShow/static/stuff/lena_copy.ppm')
canvas = Canvas(frame1,height=imgobj.height(),width=imgobj.width())
canvas.create_image(0, 0, anchor=NW, image=imgobj)
canvas.pack()
canvas.bind('<Button-1>', callback)

#frame2
template_vars = [StringVar() for i in range(9)]
entries = [Entry(frame2,width=2,textvariable=template_vars[i]) for i in range(9)]
for i,entry in enumerate(entries):
    template_vars[i].set('1')
    entry.grid(row=i/3,column=i%3)

buttons = [Button(frame3,text='开始',width=5),
           Button(frame3,text='上一步',width=5),
           Button(frame3,text='下一步',width=5)]
for i,button in enumerate(buttons):
    button.grid(row=i,column=0,sticky=NW)

frame1.grid(row=0,column=0,rowspan=2,sticky=NW)
frame2.grid(row=0,column=1,sticky=NW,padx=10,pady=5)
frame3.grid(row=1,column=1,sticky=NW,padx=10,pady=5)
root.mainloop()