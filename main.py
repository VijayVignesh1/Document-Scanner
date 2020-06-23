import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.filters import threshold_local
import imutils
from PIL import Image,ImageTk
from PIL import ImageTk as itk
from scan import *

import tkinter as tk     # python 3
from tkinter import ttk
# import Tkinter as tk   # python 2

class Example(tk.Frame):
    """Illustrate how to drag items on a Tkinter canvas"""

    def __init__(self, parent,image_name):
        tk.Frame.__init__(self, parent)

        self.img = cv2.imread(image_name)
        # create a canvas
        self.canvas = tk.Canvas(width=self.img.shape[1]+100, height=self.img.shape[0])
        # self.canvas.pack(fill="both", expand=True)
        # self.canvas.pack( expand=False)
        self.canvas.pack()


        # self.img = cv2.imread(image_name)
        # self.img=cv2.resize(self.img,(400,400))
    
        self.img_tk = Image.fromarray(self.img)
        self.image = itk.PhotoImage(image=self.img_tk)

        # self.image=itk.PhotoImage(file="pages.jpg")
        # self.img = cv2.imread('pages.jpg')
        # print(self.img.shape)

        self.canvas.create_image(0, 0, image=self.image, anchor=tk.NW)

        
        # this data is used to keep track of an
        # item being dragged
        self._drag_data = {"x": 0, "y": 0, "item": None}

        # create a couple of movable objects
        self.id_topleft=self.create_token(100, 100, "red")
        self.id_topright=self.create_token(200, 100, "red")
        self.id_bottomleft=self.create_token(100, 200, "red")
        self.id_bottomright=self.create_token(200, 200, "red")

        self.x_topleft=self.canvas.coords(self.id_topleft)[0]+5
        self.y_topleft=self.canvas.coords(self.id_topleft)[1]+5

        self.x_topright=self.canvas.coords(self.id_topright)[0]+5
        self.y_topright=self.canvas.coords(self.id_topright)[1]+5

        self.x_bottomright=self.canvas.coords(self.id_bottomright)[0]+5
        self.y_bottomright=self.canvas.coords(self.id_bottomright)[1]+5

        self.x_bottomleft=self.canvas.coords(self.id_bottomleft)[0]+5
        self.y_bottomleft=self.canvas.coords(self.id_bottomleft)[1]+5


        self.line_top=self.canvas.create_line(self.x_topleft,self.y_topleft,self.x_topright,self.y_topright,width=3,fill='red')
        self.line_rightvert=self.canvas.create_line(self.x_topright,self.y_topright,self.x_bottomright,self.y_bottomright,width=3,fill='red')
        self.line_bottom=self.canvas.create_line(self.x_bottomleft,self.y_bottomleft,self.x_bottomright,self.y_bottomright,width=3,fill='red')
        self.line_leftvert=self.canvas.create_line(self.x_topleft,self.y_topleft,self.x_bottomleft,self.y_bottomleft,width=3,fill='red')
        # lines=[self.id1,self.id2]
        # canvas.create_line()
        # print(self.id1,self.id2)
        # print(self.canvas.coords(self.id1))
        # B = Tkinter.Button(self.canvas, text ="Hello", command = helloCallBack)
        self.canvas.pack()
        style = ttk.Style()
        style.configure('TButton', font = 
               ('calibri', 12, 'bold'), 
                    borderwidth = '4')
        style.map('TButton', foreground = [('active', 'green')], 
                     background = [('active', 'black')]) 
        B=ttk.Button(self.canvas,text="Scan!!",command=self.ScanImage)
        B.grid(row = 1, column = 3, pady = 10, padx = 10)
        # self.image = tk.PhotoImage(Image.open("pages.jpg"))
        # B.pack(anchor=tk.NE)
        self.canvas.create_window(self.img.shape[1],self.img.shape[0]/2,anchor=tk.SW,window=B)
        # add bindings for clicking, dragging and releasing over
        # any object with the "token" tag
        self.canvas.tag_bind("token", "<ButtonPress-1>", self.drag_start)
        self.canvas.tag_bind("token", "<ButtonRelease-1>", self.drag_stop)
        self.canvas.tag_bind("token", "<B1-Motion>", self.drag)

    def ScanImage(self):
        def nothing(x):
            pass
        # tkMessageBox.showinfo( "Hello Python", "Hello World")
        print("Scanning...")
        pts1=np.float32([[self.x_topleft,self.y_topleft],
                        [self.x_topright,self.y_topright],
                        [self.x_bottomleft,self.y_bottomleft],
                        [self.x_bottomright,self.y_bottomright]])
        width=int(max(abs(self.x_topleft-self.x_topright),abs(self.x_bottomleft-self.x_bottomright)))
        height=int(max(abs(self.y_topleft-self.y_bottomleft),abs(self.y_topright-self.y_bottomright)))
        # print(width,height)
        width+=50
        height+=50
        pts2 = np.float32([[0,0],[width,0],[0,height],[width,height]])
        # print(pts1)
        M = cv2.getPerspectiveTransform(pts1,pts2)
        # print(pts1)
        dst = cv2.warpPerspective(self.img,M,(width,height))
        # print(dst.shape)
        # plt.imshow(dst)
        # plt.show()
        # dst=cv2.cvtColor(dst,cv2.COLOR_BGR2GRAY)
        # _=scan_adaptive(dst,11)
        # exit(0)
        # exit(0)
        im = Image.fromarray(dst)
        self.imgtk = itk.PhotoImage(image=im)
        self.canvas.delete("all")
        # self.canvas.itemconfig(self.image, image = imgtk)
        self.canvas.create_image(0, 0, image=self.imgtk, anchor=tk.NW)
        self.canvas.pack()

        kernel = np.array([[-1,-1,-1], 
                   [-1, 9.1,-1],
                   [-1,-1,-1]])




        # dst = cv2.filter2D(dst, -1, kernel)
        # kernel = np.ones((3,3), np.uint8)
        # dst = cv2.erode(dst, kernel, iterations=1) 
        # dst = cv2.dilate(dst, kernel, iterations=1) 
        # dst=cv2.GaussianBlur(dst,(7,7),0)

        # cv2.namedWindow('image')
        # cv2.createTrackbar('Threshold','image',1,20,nothing)
        
        dst=cv2.cvtColor(dst,cv2.COLOR_BGR2GRAY)
        # dst = cv2.equalizeHist(dst)
        # dst = cv2.filter2D(dst, -1, kernel)
        # img=cv2.adaptiveThreshold(dst,maxValue=255,blockSize=7,adaptiveMethod=cv2.ADAPTIVE_THRESH_MEAN_C,thresholdType=cv2.THRESH_BINARY,C=5)
        # cv2.imshow('img',img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        img=scan_adaptive(dst,val=21)
        # img=cv2.fastNlMeansDenoising(img,None,7,7,21)
        img=Image.fromarray(cv2.cvtColor(img,cv2.COLOR_GRAY2RGB))
        plt.imshow(img)
        plt.show()


        """        
        while(1):
            k = cv2.waitKey(1) & 0xFF
            if k == ord('q'):
                break
            c_val=cv2.getTrackbarPos('Threshold','image')
            # ret,img=cv2.threshold(dst,thresh,255,cv2.THRESH_BINARY)
            # img=cv2.adaptiveThreshold(dst,maxValue=255,blockSize=25,adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,thresholdType=cv2.THRESH_BINARY,C=c_val)
            # img=cv2.fastNlMeansDenoising(img,None,7,7,21)
            # img=scan(dst,c_val)
            img=scan_adaptive(dst,c_val)
            # img = cv2.erode(img, kernel, iterations=1)
            # img = cv2.dilate(img, kernel, iterations=1)
            cv2.imshow('image',img)
            # print(thresh)
        cv2.destroyAllWindows()
        """


    def create_token(self, x, y, color):
        """Create a token at the given coordinate in the given color"""
        id1=self.canvas.create_oval(
            x - 5,
            y - 5,
            x + 5,
            y + 5,
            outline=color,
            fill=color,
            tags=("token",),
        )
        return id1
    def drag_start(self, event):
        """Begining drag of an object"""
        # record the item and its location
        self._drag_data["item"] = self.canvas.find_closest(event.x, event.y)[0]
        # print(self._drag_data['item'])
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def drag_stop(self, event):
        """End drag of an object"""
        # reset the drag information
        self._drag_data["item"] = None
        self._drag_data["x"] = 0
        self._drag_data["y"] = 0

    def drag(self, event):
        """Handle dragging of an object"""
        # compute how much the mouse has moved
        delta_x = event.x - self._drag_data["x"]
        delta_y = event.y - self._drag_data["y"]
        # move the object the appropriate amount
        self.canvas.move(self._drag_data["item"], delta_x, delta_y)
        # record the new position
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y
        # print(self.canvas.coords(self.id1))
        if self._drag_data['item']==self.id_topleft:
            self.canvas.coords(self.line_top,event.x,event.y,self.x_topright,self.y_topright)
            self.canvas.coords(self.line_leftvert,event.x,event.y,self.x_bottomleft,self.y_bottomleft)
            self.x_topleft=event.x
            self.y_topleft=event.y
        elif self._drag_data['item']==self.id_topright:
            # print("hi")
            self.canvas.coords(self.line_top,self.x_topleft,self.y_topleft,event.x,event.y)
            self.canvas.coords(self.line_rightvert,event.x,event.y,self.x_bottomright,self.y_bottomright)
            self.x_topright=event.x
            self.y_topright=event.y
        elif self._drag_data['item']==self.id_bottomleft:
            # print("hi")
            self.canvas.coords(self.line_leftvert,self.x_topleft,self.y_topleft,event.x,event.y)
            self.canvas.coords(self.line_bottom,event.x,event.y,self.x_bottomright,self.y_bottomright)
            self.x_bottomleft=event.x
            self.y_bottomleft=event.y
        elif self._drag_data['item']==self.id_bottomright:
            # print("hi")
            self.canvas.coords(self.line_bottom,self.x_bottomleft,self.y_bottomleft,event.x,event.y)
            self.canvas.coords(self.line_rightvert,self.x_topright,self.y_topright,event.x,event.y)
            self.x_bottomright=event.x
            self.y_bottomright=event.y
if __name__ == "__main__":
    image_name="test.jpg"
    root = tk.Tk()
    root.title("Image Scanner")
    # root.wm_geometry("1100x1100")
    Example(root,image_name).pack(fill="both", expand=True)
    root.mainloop()
# exit(0)











# def draw_circle(event,x,y,flags,param):
#     global mouseX,mouseY
#     if event == cv2.EVENT_LBUTTONDBLCLK:
#         cv2.circle(img,(x,y),2,(255,0,0),-1)
#         mouseX,mouseY = x,y

# img = cv2.imread('pages.jpg')
# print(img.shape)
# cv2.namedWindow('image')
# cv2.setMouseCallback('image',draw_circle)
# lists=[]
# while(1):
#     cv2.imshow('image',img)
#     k = cv2.waitKey(20) & 0xFF
#     if k == 27:
#         break
#     elif k == ord('a'):
#         print(mouseX,mouseY)
#         lists.append([mouseX,mouseY])
#     elif k==ord('q'):
#         cv2.destroyAllWindows()
#         break
# # exit(0)
# # img = cv2.imread('sudokusmall.png')

# rows,cols,ch = img.shape

# # pts1 = np.float32([[56,65],[368,52],[28,387],[389,390]])
# pts1=np.float32(lists)
# pts2 = np.float32([[0,0],[300,0],[0,300],[300,300]])
# print(pts1)
# M = cv2.getPerspectiveTransform(pts1,pts2)

# dst = cv2.warpPerspective(img,M,(300,300))

# plt.subplot(121),plt.imshow(img),plt.title('Input')
# plt.subplot(122),plt.imshow(dst),plt.title('Output')
# plt.show()

# warped = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
# # T = threshold_local(warped, 11, offset = 10, method = "gaussian")
# # print(T.shape)
# for i in range(50,150,10):
#     # warped = (warped > i).astype("uint8") * 255
#     ret, thresh2 = cv2.threshold(warped, i, 255, cv2.THRESH_BINARY_INV) 

#     # cv2.imshow("Scanned", imutils.resize(warped, height = 650))
#     cv2.imshow('scanned',thresh2)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
# exit(0)

# img = cv2.imread('drawing.png')
# rows,cols,ch = img.shape

# pts1 = np.float32([[50,50],[200,50],[50,200]])
# pts2 = np.float32([[10,100],[200,50],[100,250]])

# M = cv2.getAffineTransform(pts1,pts2)

# dst = cv2.warpAffine(img,M,(cols,rows))

# plt.subplot(121),plt.imshow(img),plt.title('Input')
# plt.subplot(122),plt.imshow(dst),plt.title('Output')
# plt.show()
