# coding: UTF-8 
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import urllib2,urllib,cookielib,re,logging

def toLog():
    logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='myapp.log',
                filemode='w')

    #################################################################################################
    #定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s-%(name)-2s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    #################################################################################################

    logging.debug("debug message")
    logging.info("info message")
    logging.warn("warn message")
    logging.error("error message")
    logging.critical("critical message")

if __name__ == "__main__":
    toLog()
    cj = cookielib.CookieJar()
    body = (('nickname','rswofxd'), ('password','rsw173259'))
    opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    opener.addheaders = [('User-agent','Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')]
    urllib2.install_opener(opener)

    url = 'http://login.hi.mop.com/Login.do'
    req=urllib2.Request(url,urllib.urlencode(body))
    u=urllib2.urlopen(req)
    login=u.read().decode('utf-8').encode('gbk')
    print re.findall('\<title\>(.+)\<',login)[0]
    
    #打卡领MP
    mpurl='http://home.hi.mop.com/ajaxGetContinusLoginAward.do'
    mp=opener.open(urllib2.Request(mpurl)).read()
    if mp=='5':
        print ('打卡成功 MP+5')
    else:
 		print('已经打卡')

