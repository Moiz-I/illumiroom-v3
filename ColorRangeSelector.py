import tkinter as tk
from PIL import Image, ImageDraw, ImageTk
import colorsys

class ColorRangeSelector:
    def __init__(self, root, x, y, w=255 , h=255 , bg='white', lineColor='black' , textColor = 'gray' , initial = [0,255] ):
        self.root=root
        self.x = x
        self.y = y
        self.w = w
        h=min(h, 255)
        self.h = h

        self.clicked_id = -1
        self.padding = 16
        self.canvas = tk.Canvas(self.root, width=w + 2 * self.padding, height=h + 2 * self.padding, bg=bg)
        self.result = initial.copy()

        image = Image.new("RGB", (w, h))
        draw = ImageDraw.Draw(image)

        w_adim= w/255
        for i in range(255):
            for j in range(255-h, 255):
                rgb = tuple(round(c * 255) for c in colorsys.hsv_to_rgb(i / 255, 1, j / 255))
                color= '#%02x%02x%02x' % rgb
                draw.rectangle( [i * w_adim , (j + h - 255) ,(i + 1) * w_adim , (j + h - 255) + 1 ], outline=None,fill=color)

        ph = ImageTk.PhotoImage(image)
        self.canvas.create_image(self.padding, self.padding, anchor='nw', image = ph)
        self.canvas.image = ph

        start_line = self.canvas.create_rectangle(initial[0]+ self.padding, self.padding,initial[0]+  self.padding+1, h+self.padding, width=0, fill=lineColor)
        start_select = self.canvas.create_rectangle(initial[0]+ self.padding/2, self.padding/2, initial[0]+ self.padding*3/2, self.padding, width=0, fill='black')
        start_text = self.canvas.create_text(initial[0]+ self.padding/2+7 ,self.padding/2+4,text='S',fill="white", font=('Helvetica 6 bold'))

        end_line = self.canvas.create_rectangle(initial[1]*w_adim-1+ self.padding, self.padding,initial[1]*w_adim+ self.padding, h+self.padding, width=0, fill=lineColor)
        end_select = self.canvas.create_rectangle(initial[1]*w_adim + self.padding/2, h+self.padding, initial[1]*w_adim+self.padding*3/2, h +self.padding*3/2, width=0,
                                                  fill='black')

        end_text = self.canvas.create_text(initial[1]*w_adim + self.padding/2+8, h+ self.padding+4, text='E', fill="white", font=('Helvetica 6 bold'))

        self.text = self.canvas.create_text(self.w/2 + self.padding, self.padding/2, text='[{:.2f},{:.2f}]'.format(self.result[0],self.result[1]), fill=textColor, font=('Helvetica 7 bold'))

        self.selectors = [start_select,start_line,start_text,end_select,end_line,end_text]

        self.canvas.bind( '<B1-Motion>', self.motion)
        self.canvas.bind('<ButtonRelease-1>', self.mouseReleased)
        self.canvas.place(x=x,y=y)

    def motion(self,event):
        if self.clicked_id and self.clicked_id < 0:
            self.clicked_id= self.getRectangle(event.x, event.y)
        if self.clicked_id:
            index = self.selectors.index(self.clicked_id)
            rect_y = self.padding/2
            if index>2:
                rect_y=self.h+self.padding

            line_id= self.selectors[index+1]
            text_id = self.selectors[index + 2]

            cur_x = event.x
            if event.x > self.w+self.padding:
                cur_x = self.w +self.padding
            if event.x < self.padding:
                cur_x = self.padding

            self.canvas.coords(line_id, cur_x, self.padding, cur_x + 1,self.h + self.padding)
            self.canvas.coords(self.clicked_id, cur_x-self.padding/2, rect_y, cur_x+self.padding/2, rect_y+self.padding/2)

            self.canvas.coords(text_id, cur_x, rect_y+4)

            self.result[int(index/3)] = (cur_x-self.padding)/self.w*255
            self.canvas.itemconfigure(self.text,text='[{:.2f},{:.2f}]'.format(self.result[0],self.result[1]))    

    def mouseReleased(self,event):
        self.clicked_id = -1

    def getRectangle(self,x, y):
        for i in range(2):
            sel = self.selectors[i*3]
            curr_xs, curr_ys, curr_xe, curr_ye = self.canvas.coords(sel)
            if (curr_xs <= x <= curr_xe) and (curr_ys <= y <= curr_ye):
                return sel