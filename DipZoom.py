from os import remove
from PyQt5.Qt import *
import sys
from PyQt5.QtWidgets import QFileDialog
import cv2
import numpy as np
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os

class Window(QWidget):
	def __init__(self):
		super().__init__()
		#窗口大小
		self.resize(1000,800)
		self.setFixedSize(1000,800)
		#窗口标题
		self.setWindowTitle("DipZoom")
		#窗口背景图
		palette = QPalette()
		palette.setBrush(QPalette.Background, QBrush(QPixmap("background.jpg").scaled(self.width(),self.height())))
		self.setPalette(palette)
		#全局字体
		self.setFont(QFont(None,12))

		self.setup_ui()

	def setup_ui(self):
        #按钮
		btn_open = QPushButton(self)
		#文本
		btn_open.setText('打开图片')
		#坐标
		btn_open.move(250, 50)
		#透明
		btn_open.setFlat(True)
		
		btn_cancel = QPushButton(self)
		btn_cancel.setText('退出程序')
		btn_cancel.move(650, 50)
		btn_cancel.setFlat(True)

		btn_save= QPushButton(self)
		btn_save.setText('保存图片')
		btn_save.move(450, 50)
		btn_save.setFlat(True)

		btn_translation= QPushButton(self)
		btn_translation.setText('平移图片')
		btn_translation.move(150, 600)
		btn_translation.setFlat(True)

		btn_zoom= QPushButton(self)
		btn_zoom.setText('缩放图片')
		btn_zoom.move(300, 600)
		btn_zoom.setFlat(True)

		btn_reversal= QPushButton(self)
		btn_reversal.setText('翻转图片')
		btn_reversal.move(450, 600)
		btn_reversal.setFlat(True)

		btn_cut= QPushButton(self)
		btn_cut.setText('裁剪图片')
		btn_cut.move(600, 600)
		btn_cut.setFlat(True)

		btn_gray = QPushButton(self)
		btn_gray.setText('灰度图')
		btn_gray.move(750, 600)
		btn_gray.setFlat(True)

		btn_filter = QPushButton(self)
		btn_filter.setText('平滑滤波')
		btn_filter.move(150, 700)
		btn_filter.setFlat(True)

		btn_gradient= QPushButton(self)
		btn_gradient.setText('轮廓提取')
		btn_gradient.move(300, 700)
		btn_gradient.setFlat(True)

		btn_tophat = QPushButton(self)
		btn_tophat.setText('噪声提取')
		btn_tophat.move(450, 700)
		btn_tophat.setFlat(True)

		btn_segmentation = QPushButton(self)
		btn_segmentation.setText('图片分割')
		btn_segmentation.move(600, 700)
		btn_segmentation.setFlat(True)

		btn_edge = QPushButton(self)
		btn_edge.setText('边缘检测')
		btn_edge.move(750, 700)
		btn_edge.setFlat(True)

		#图片展示区域
		label_left = QLabel(self)
		#大小
		label_left.setFixedSize(400, 400)
		#坐标
		label_left.move(50, 150)
		#透明
		label_left.setStyleSheet("QLabel{background:none;}")

		label_right = QLabel(self)
		label_right.setFixedSize(400, 400)
		label_right.move(550, 150)
		label_right.setStyleSheet("QLabel{background:none;}")

		label_mid = QLabel(self)
		label_mid.setFixedSize(50, 200)
		label_mid.move(475, 250)
		label_mid.setStyleSheet("QLabel{background:none;}"
								 "QLabel{color:black;font-size:25px;}" )				 

		def cancel():
			exit(0)
		btn_cancel.clicked.connect(cancel)

		def openImage():
			directory = QFileDialog.getOpenFileName(self,
			  "getOpenFileName","./",
			  "All Files (*);;Text Files (*.txt)") 
			self.imgpath = directory[0]
			img = QtGui.QPixmap(self.imgpath).scaled(label_left.width(), label_left.height())
			label_left.setPixmap(img)
		btn_open.clicked.connect(openImage)

		def saveImage():
			img = label_right.pixmap().toImage()
			img.save(os.path.split(os.path.splitext(self.imgpath)[0])[1]+'_result.jpg',"JPG",100)
		btn_save.clicked.connect(saveImage)

		def translation():
			label_mid.setText('平移\n\ndx:\n100\n\ndy:\n100')
			img = cv2.imread(self.imgpath)
			x=100
			y=100
			rows, cols = img.shape[:2]
			M = np.float32([[1, 0, x], [0, 1, y]])
			res = cv2.warpAffine(img, M, (cols, rows),borderValue=(255,255,255)) # 用仿射变换实现平移
			cv2.imwrite('temp.jpg', res)
			img_new = QtGui.QPixmap('temp.jpg').scaled(label_right.width(), label_right.height())
			remove('temp.jpg')
			label_right.setPixmap(img_new)
		btn_translation.clicked.connect(translation)

		def zoom():
			label_mid.setText('缩放\n\ndx:\n0.1\n\ndy:\n0.1')
			img = cv2.imread(self.imgpath)
			x=0.1
			y=0.1
			res=cv2.resize(img, None, fx=x, fy=y)
			cv2.imwrite('temp.jpg', res)
			img_new = QtGui.QPixmap('temp.jpg').scaled(label_right.width(), label_right.height())
			remove('temp.jpg')
			label_right.setPixmap(img_new)
		btn_zoom.clicked.connect(zoom)

		def cut():
			label_mid.setText('平移\ndx:\n100\ndy:\n100\ndw:\n500\ndh:\n500')
			img = cv2.imread(self.imgpath)
			x=100
			y=100
			h=500
			w=500
			res = img[y:y+h,x:x+w]
			cv2.imwrite('temp.jpg', res)
			img_new = QtGui.QPixmap('temp.jpg').scaled(label_right.width(), label_right.height())
			remove('temp.jpg')
			label_right.setPixmap(img_new)
		btn_cut.clicked.connect(cut)	

		def reversal():
			label_mid.setText('翻转')
			img = cv2.imread(self.imgpath)
			res = cv2.flip(img, 0)
			cv2.imwrite('temp.jpg', res)
			img_new = QtGui.QPixmap('temp.jpg').scaled(label_right.width(), label_right.height())
			remove('temp.jpg')
			label_right.setPixmap(img_new)
		btn_reversal.clicked.connect(reversal)

		def gray():
			label_mid.setText('灰度\n图')
			img = cv2.imread(self.imgpath,cv2.IMREAD_GRAYSCALE)
			cv2.imwrite('temp.jpg', img)
			img_new = QtGui.QPixmap('temp.jpg').scaled(label_right.width(), label_right.height())
			remove('temp.jpg')
			label_right.setPixmap(img_new)
		btn_gray.clicked.connect(gray)

		def gradient():
			label_mid.setText('梯度\n运算')
			img = cv2.imread(self.imgpath)
			k=np.ones((5,5),np.uint8)
			r=cv2.morphologyEx(img,cv2.MORPH_GRADIENT,k)
			cv2.imwrite('temp.jpg', r)
			img_new = QtGui.QPixmap('temp.jpg').scaled(label_right.width(), label_right.height())
			remove('temp.jpg')
			label_right.setPixmap(img_new)
		btn_gradient.clicked.connect(gradient)	

		def filter():
			label_mid.setText('中值\n滤波')
			img = cv2.imread(self.imgpath)
			blur = cv2.medianBlur(img, 3)
			cv2.imwrite('temp.jpg', blur)
			img_new = QtGui.QPixmap('temp.jpg').scaled(label_right.width(), label_right.height())
			remove('temp.jpg')
			label_right.setPixmap(img_new)
		btn_filter.clicked.connect(filter)	

		def tophat():
			label_mid.setText('礼帽\n操作')
			img = cv2.imread(self.imgpath)
			k=np.ones((5,5),np.uint8)
			r=cv2.morphologyEx(img,cv2.MORPH_TOPHAT,k)
			cv2.imwrite('temp.jpg', r)
			img_new = QtGui.QPixmap('temp.jpg').scaled(label_right.width(), label_right.height())
			remove('temp.jpg')
			label_right.setPixmap(img_new)
		btn_tophat.clicked.connect(tophat)	

		def segmentation():
			label_mid.setText('OTSU\n分割')
			img = cv2.imread(self.imgpath,cv2.IMREAD_GRAYSCALE)		
			ret, th = cv2.threshold(img, 50, 100,cv2.THRESH_OTSU)
			cv2.imwrite('temp.jpg', th)
			img_new = QtGui.QPixmap('temp.jpg').scaled(label_right.width(), label_right.height())
			remove('temp.jpg')
			label_right.setPixmap(img_new)
		btn_segmentation.clicked.connect(segmentation)

		def edgeDector():
			label_mid.setText('canny\n边缘\n检测')
			img = cv2.imread(self.imgpath)
			edges = cv2.Canny(img, 100, 100)  
			cv2.imwrite('temp.jpg', edges)
			img_new = QtGui.QPixmap('temp.jpg').scaled(label_right.width(), label_right.height())
			remove('temp.jpg')
			label_right.setPixmap(img_new)
		btn_edge.clicked.connect(edgeDector)

if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = Window()
	window.show()
	sys.exit(app.exec_())
