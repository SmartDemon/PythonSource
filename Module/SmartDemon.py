#coding:utf-8
##########################################
#Author:rswofnd
#Vision:1.0
#DateTime:2012-6-7
##########################################
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import sys,os,datetime
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt,QTimer, QTime

############################################
#初始化Qt界面及行为
#向第三方类及模块暴露API接口
class SmartDemon(QtGui.QWidget):
	"""
	docstring for SmartDemon(精灵)
	"""
	def __init__(self,side):
		super(SmartDemon, self).__init__()
		self.side = side
		self.w = (self.side-20)/8 
		self.initui()
		self.handleChange()
		self.init_Plugins()

		self.timer = QTimer()
		self.timer.timeout.connect(self.update)
		self.timer.start(100) 
		self.show() 

	def initui(self):
		"""
		初始化UI界面
		"""
		self.setGeometry(300,300,self.side,self.side)

		self.popMenu()

		sizeGrip=QtGui.QSizeGrip(self)
		self.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint|Qt.SubWindow|Qt.WA_Moved)

		self.trans=False                                  #True?
		self.set_transparency(True)                       #设置窗口透明

	def popMenu(self):
		"""
		定义弹出菜单
		"""
		setupAction = QtGui.QAction(QtGui.QIcon('SetUp.png'), '&SetUp', self)       #定义动作抽象
		setupAction.triggered.connect(self.setUp)
		quitAction = QtGui.QAction( 'Quit', self)
		quitAction.triggered.connect(QtGui.qApp.quit)
		self.popMenu= QtGui.QMenu()                                              #定义右键弹出菜单
		self.popMenu.addAction(setupAction) 
		self.popMenu.addAction(quitAction)
		self.rightButton=False

	def set_transparency(self, enabled):
		"""
		窗口透明度显示实现

		"""
		if enabled:
			self.setAttribute(Qt.WA_Moved, True)                                         
			self.setAutoFillBackground(False)
		else:
			self.setAttribute(Qt.WA_NoSystemBackground, False)

        #	下面这种方式好像不行
		#	pal=QtGui.QPalette()
		#	pal.setColor(QtGui.QPalette.Background, QColor(127, 127,10,120))
		#	self.setPalette(pal) 

		self.setAttribute(Qt.WA_TranslucentBackground, enabled)
		self.update()
        #	self.repaint() no better than self.update()

	def resizeEvent(self,e):
		"""
		重新实现尺寸拖拽事件
		"""
		self.handleChange()

	def handleChange(self):
		"""
		改变控件大小
		"""
		self.side = min(self.width(), self.height()) 
		self.w = (self.side-20)/8

	def mouseReleaseEvent(self,e): 
		"""
		鼠标释放事件

		"""
		if self.rightButton == True:
			self.rightButton=False
			self.popMenu.popup(e.globalPos())

	def mouseMoveEvent(self, e):
		"""
		鼠标移动事件

		"""
		if e.buttons() & Qt.LeftButton:
			self.move(e.globalPos()-self.dragPos)
			e.accept()

	def mousePressEvent(self, e):
		"""
		鼠标按下事件

		"""
		if e.button() == Qt.LeftButton: 
			self.dragPos=e.globalPos()-self.frameGeometry().topLeft() 
			e.accept()
		if e.button() == Qt.RightButton and self.rightButton == False:
			self.rightButton=True

	def closeEvent(self,event):
		"""
		应用于窗口关闭弹出菜单
		是对系统默认关闭事件的‘重新实现’
		
		"""

		reply = QtGui.QMessageBox.question(self,'Message','sure to quit?',
			QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,QtGui.QMessageBox.No)

		if reply==QtGui.QMessageBox.Yes:
			event.accept()
		else:
			event.ignore()

	def paintEvent(self,event):
		"""
		重新实现组件绘制事件
		"""
		qp = QtGui.QPainter()
		#################################
		#时钟API接口
		timeAPI = TimeM(0,0,0)
		self.h = timeAPI.hour
		self.m = timeAPI.minute
		self.s = timeAPI.second
		self.ms = timeAPI.m_second
		
		#时，分，秒显示
		self.hour = -((15.0 * ((self.h + self.m/ 60.0)))*16)
		self.minute = -((6.0 * (self.m + ((self.s+self.ms/1000)/ 60.0)))*16)
		self.second = -(6.0*(self.s+float(self.ms)/1000)*16)
		
		qp.begin(self)
		#开始绘制		             
		qp.setRenderHint(QtGui.QPainter.Antialiasing)        #开启抗锯齿

		pen = QtGui.QPen(QtGui.QColor(112,166,18),self.w*0.382,QtCore.Qt.SolidLine)
		qp.setPen(pen)                             #设置画笔颜色，粗细和线型
		qp.drawArc((10+self.w),(10+self.w),(self.side-2*(10+self.w)),(self.side-2*(10+self.w)),90*16,self.second)      #绘制弧线段，x,y,w,h,a,alen

		pen = QtGui.QPen(QtGui.QColor(34,113,204),self.w*0.618,QtCore.Qt.SolidLine)
		qp.setPen(pen)                             #设置画笔颜色，粗细和线型
		qp.drawArc((10+2*self.w),(10+2*self.w),(self.side-2*(10+2*self.w)),(self.side-2*(10+2*self.w)),90*16,self.minute)      #绘制弧线段，x,y,w,h,a,alen

		pen = QtGui.QPen(QtGui.QColor(219,92,29),self.w*0.382,QtCore.Qt.SolidLine)
		qp.setPen(pen)                             #设置画笔颜色，粗细和线型
		qp.drawArc((10+3*self.w),(10+3*self.w),(self.side-2*(10+3*self.w)),(self.side-2*(10+3*self.w)),90*16,self.hour)      #绘制弧线段，x,y,w,h,a,alen
		#结束绘制
		qp.end()

	def setUp(self):
		"""
		定时，任务，插件等参数设置
		"""
		pass
	def init_Plugins(self):
		"""
		自动加载插件
		管理和运行插件
		"""
		self.plugin = Platform()
		self.plugins = self.plugin.plugins
		for x in self.plugins:
			Action = QtGui.QAction(QtGui.QIcon('Action.png'),x, self)
			Action.triggered.connect(self.plugin.runPlugin)
			self.popMenu.addAction(Action)
########################################
#时钟类
#向主类提供时钟API接口
class TimeM(object):
	"""
	docstring for TimeM
	"""
	def __init__(self,count_h,count_m,count_s):
		super(TimeM, self).__init__()
		self.year = 0
		self.month = 0
		self.day = 0
		self.wday = 0
		self.yday = 0
		self.hour = 0
		self.minute = 0
		self.second = 0
		self.m_second = 0
		self.c_h = count_h
		self.c_m = count_m
		self.c_s = count_s
		self.do_What()
	def do_What(self):
		if (self.c_h==0 and self.c_m==0 and self.c_s==0):
			self.now()
		else:
			self.counter()
	def now(self):
		t = datetime.datetime.now()
		self.year = t.year
		self.month = t.month
		self.day = t.day
		self.hour = t.hour
		self.minute = t.minute
		self.second = t.second
		self.m_second = t.microsecond/1000
		self.wday = t.isoweekday()
		self.str_time = t.strftime('%Y-%m-%d %H:%M:%S')
	def counter(self):
		pass
#######################################
#插件平台
#提供插件API接口
class Platform(SmartDemon):
	"""
	调用plugins目录下非Zip插件包
	该目录下必须包含一个__init__.py空文件和相关插件模块
	"""
	def __init__(self):
		self.plugins=[]
		self.loadPlugins()

	def sayHello(self, from_):
		print "hello from %s." % from_
	
	def sayGoodbye(self, from_):
		print "goodbye from %s." % from_

	def loadPlugins(self):
		for filename in os.listdir("plugins"):
			if not filename.endswith(".py") or filename.startswith("_"):
				continue
			self.plugins.append(filename)            #添加插件列表

	def runPlugin(self, filename):
		pluginName=os.path.splitext(filename)[0]
		plugin=__import__("plugins."+pluginName, fromlist=[pluginName])
		clazz=plugin.getPluginClass()                    
		o=clazz()
		o.setPlatform(self)
		o.start()                         #运行插件start()函数

	def shutdown(self):
		for o in self.plugins:
			o.stop()                      #运行插件stop()函数
			o.setPlatform(None)
		self.plugins=[]                   #清空插件列表		
#############################################
#模块入口主函数
def main_demon():
	app = QtGui.QApplication(sys.argv)
	demon = SmartDemon(100)
	sys.exit(app.exec_())

#############################################
#测试代码
if __name__ == '__main__':
	main_demon()