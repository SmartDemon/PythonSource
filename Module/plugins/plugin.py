#coding:utf-8
import os

def alert():
	print('plugins working...................')
    #输出重定向到日志文件
	logfile=open("plugins/log.txt","a") 
	#print("plugins working...................",file=logfile)    #python3.0
	print >> logfile,"plugins working..................." 
	logfile.close()

class Plugin:
    def setPlatform(self, platform):
        self.platform=platform

    def start(self):
        self.platform.sayHello("plugin")
        alert()

    def stop(self):
        self.platform.sayGoodbye("plugin")

def getPluginClass():
    return Plugin


alert()