#!/opt/python3.5.1/bin/python3
# -*- coding: utf-8 -*-

import sys
import time
import requests
import threading

STOCK_THRESHOLD = 10
QUERY_TIMEOUT   = 3
URL             = 'http://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=tse_'
STOCK_ID        = '2317'
URL_INF         = '.tw&json=1&delay=0&_='
TWSE_HOME_URL 	= 'http://mis.twse.com.tw/stock/fibest.jsp?stock='

def print_same_line (string):
    t = time.strftime("[%Y-%m-%d %H:%M:%S] ", time.localtime()) 

    sys.stdout.write(t + string + '\r')
    sys.stdout.flush()

def get_cookies (url):
    return requests.get(url).cookies

def get_stock_info (stock):
    c = dict(get_cookies(TWSE_HOME_URL + STOCK_ID));
    r = requests.get(URL + STOCK_ID + URL_INF + str(int(time.time()) * 1000), cookies=c)
    
    data = r.json()
    if 'msgArray' not in data:
        # print ('waiting for retry in ' + str(QUERY_TIMEOUT / 1000) + ' seconds...')
        print_same_line ('waiting for retry in ' + str(QUERY_TIMEOUT / 1000) + ' seconds...')
    else:
        #print (' Code:' + data['msgArray'][0]['c'] + '  |  ' +  'Price:' + data['msgArray'][0]['z'])
        print_same_line (' Code:' + data['msgArray'][0]['c'] + '  |  ' +  'Price:' + data['msgArray'][0]['z'])
        
class stock_thread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        print ("Starting " + self.name)

        while 1:
            get_stock_info (STOCK_ID)
            time.sleep(QUERY_TIMEOUT)
        
        print ("Exiting " + self.name)
            
def main ():
    thread1 = stock_thread(1, 'get_stock_thread', 1)
    thread1.start()
    thread1.join()
    print ('Exiting Main Thread')

if __name__ == '__main__':
    main()
