#-*- coding:utf-8 -*-
import requests
import pymysql
import logging.handlers
import sys
import math
from scipy.optimize import fsolve, root
from  datetime  import  *
import time
from multiprocessing.dummy import Pool
reload(sys)
sys.setdefaultencoding('utf8')
lat = [37.2549979,38.1337899,38.4497298]
lng = [-122.3832533,-121.2912278,-123.1153394]

global dis1
dis1 = 0
global dis2
dis2 = 0
global dis3
dis3 = 0
handler = logging.handlers.RotatingFileHandler('/home/tst.txt', maxBytes=1024*1024*1024*1024,backupCount = 5) # ʵ����handler
fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
formatter = logging.Formatter(fmt)  # ʵ����formatter
handler.setFormatter(formatter)  # Ϊhandler���formatter

logger = logging.getLogger('logging')  # ��ȡ��Ϊtst��logger
logger.addHandler(handler)  # Ϊlogger���handler
logger.setLevel(logging.DEBUG)

logger.info('first info message')



if __name__ == '__main__':
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='zhuzhu66', db='san',
                           charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cur = conn.cursor()
    cur.execute("USE san")
    offset = 0

    cur.execute("select * from location")
    location = cur.fetchall()
    print len(location)
    logger.info(str(len(location)))

    for i in location:
        add = i['address']
        headers = {'Connection':'close'}
        url = 'https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=AIzaSyCRKF1ZHrzbO5JgaLGLfHbq4cdXkX9MKTg' % add
        #print url
        content = ""
        try:
            res = requests.get(url, timeout=30.0, verify=False, headers=headers)
            content = res.json()
        except Exception as e:
            ifError = 3
            # ifError = 3表示调用谷歌API失败，没有得到近似城市经纬度值
            logger.info(str(e.message) + "google api fail"+add)

        cityLat = 0
        cityLng = 0
        address =None

        try:
            results = content['results']
            cityLat = results[0]['geometry']['location']['lat']
            cityLng = results[0]['geometry']['location']['lng']
            address = results[0]['formatted_address']
        except Exception as e:
                print str(e.message) + " jiexi fail" + add
                logger.info(str(e.message) + " jiexi fail" + add)

        executeString = 'update location set citylat = %.10lf, citylng = %.10lf ,add_google = \'%s\' where address = \'%s\''%(cityLat,cityLng,address,add)
        try:
            cur.execute(executeString)
            cur.connection.commit()
        except Exception as e :
            logger.info(str(e.message)+str(executeString)+'save fail')









