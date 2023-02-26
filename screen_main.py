import tkinter
from PIL import ImageGrab
from aip import AipOcr
import time
import os
from tkinter import ttk
import random
import string
from PyQt5.QtWidgets import *

class nanaCapture:
    def __init__(self):
        self.X = tkinter.IntVar(value=0)
        self.Y = tkinter.IntVar(value=0)
        self.sel = False
        self.capture_png_path = 'C:\\screen_image\\'
        self.createFolder(self.capture_png_path) # 스크린샷 디렉토리

        self.capture_btn = tkinter.Button(text='스크린샷', command=self.capture_cmd) 
        self.capture_btn.place(x=80, y=10, anchor='nw', width=60, height=20)

        # 화면크기 셋
        app = QApplication([])
        # 주 모니터 선택
        # screen = app.primaryScreen()
        screen_rect = app.desktop().screenGeometry()
        width,height = screen_rect.width(), screen_rect.height()
        self.screenWidth = width
        self.screenHeight = height

        self.temp_png = 'temp.png'
        # self.screenWidth = window.winfo_screenwidth()
        # self.screenHeight = window.winfo_screenheight()
        # self.temp_png = [self.resource_path('images/temp.png')]
        print("width x height = %d x %d (pixels)" %(self.screenWidth , self.screenHeight))
        
        # 파일 이름에 쓰일 랜덤 문자
        self.str_len = 10	# 문자의 개수(문자열의 크기)
        self.rand_str = ''	# 문자열

    def capture_cmd(self):
        window.iconify()  # 최소화
        self.create_canvas()     # 전체 스크린샷 표시
        self.capture_btn.wait_window(self.top)
    
    def create_canvas(self):
        time.sleep(0.2)
        im = ImageGrab.grab()
        im.save(self.temp_png)
        im.close()

        # 최상위 컨테이너
        self.top = tkinter.Toplevel(window, width=self.screenWidth, height=self.screenHeight)
        
        # 최대 최소화 없음
        self.top.overrideredirect(True)
        self.canvas = tkinter.Canvas(self.top, bg='white', width=self.screenWidth, height=self.screenHeight)
        # 전체화면에 캡쳐 표시
        self.image = tkinter.PhotoImage(file=self.temp_png)
        self.canvas.create_image(self.screenWidth // 2, self.screenHeight // 2, image=self.image)

        # 마우스 왼쪽버튼 누른 위치
        self.canvas.bind('<Button-1>', self.mouse_left_down)
        # 마우스를 움직여 영역 표시
        self.canvas.bind('<B1-Motion>', self.mouse_move)
        # 스크린샷 저장
        self.canvas.bind('<ButtonRelease-1>', self.mouse_left_up)

        self.canvas.pack(fill=tkinter.BOTH, expand=tkinter.YES)
    
    def mouse_left_down(self, event):
        self.X.set(event.x)
        self.Y.set(event.y)
        self.sel = True 

    def mouse_move(self, event):
        if not self.sel:
            return
        try:
            self.canvas.delete(self.lastDraw)
        except Exception as e:
            pass

        self.lastDraw = self.canvas.create_rectangle(self.X.get(), self.Y.get(), event.x, event.y, outline='red')

    def mouse_left_up(self, event):
        self.sel = False
        try:
            self.canvas.delete(self.lastDraw)
        except Exception as e:
            pass

        x1, x2 = sorted([self.X.get(), event.x])
        y1, y2 = sorted([self.Y.get(), event.y])
        
        for i in range(self.str_len):
            self.rand_str += str(random.choice(string.ascii_uppercase + string.digits))

        self.capture_png_name = 'product_'+self.rand_str+'.png'
        pic = ImageGrab.grab((x1+1, y1+1, x2, y2))
        pic.save(os.path.join(self.capture_png_path, self.capture_png_name))
        

        self.top.destroy()

    def createFolder(self, directory):
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
            else:
                return directory
        except OSError:
            print ('Error: Creating directory.', directory)
            
window = tkinter.Tk()
window.title('Capture')
window.geometry('210x100') 
capture = nanaCapture()
window.mainloop()
