# -*- coding: utf-8 -*-
from PyQt5 import QtCore
import PyQt5.QtWidgets as QtGui
import urllib.request
import requests,locale
from bs4 import BeautifulSoup
import sys, webbrowser, scapy
from selenium import webdriver


class  FirstSpider(scapy.Spider):
    name = "first_spider"
    start_urls = [
        'http://aqicn.org/city/china/chengdu/yulin/cn/',
                  ]
    def parser(self, response):
        yield {
            
        }

class Fetch_Data_Thread(QtCore.QThread):
    data_signal = QtCore.pyqtSignal(str, str)
    def __init__(self):
        super(Fetch_Data_Thread, self).__init__()
        self.driver = webdriver.Firefox(executable_path='D:\Download\geckodriver')
    def run(self):
        while True:
            driver = self.driver
            try:
                driver.get("http://aqicn.org/city/china/chengdu/yulin/cn/")
                driver.find_element_by_xpath(
                    "(.//*[normalize-space(text()) and normalize-space(.)='Chengdu US Consulate'])[1]/following::span[1]").click()

                html = driver.page_source
                print(html)
                #webbrowser.open(html)
                soup = BeautifulSoup(html.text.decode('utf-8'), 'html.parser')
                self.data_signal.emit( soup.find('div', attrs={"class":"aqivalue","id":"aqiwgtvalue"}).get_text(),
                                       soup.find("span",attrs={"id":"aqiwgtutime"}).get_text() )
            except:
                self.data_signal.emit("N/A","N/A") 
            finally:
                self.sleep(3600)

class MyWidget(QtGui.QWidget):
    def __init__(self):
        super(MyWidget, self).__init__()
        self.color_grade = ["rgb(0,255,0)","rgb(255,222,51)", "rgb(255,130,51)","rgb(230,77,51)","rgb(102,0,153)"]
        self.main_layout = QtGui.QHBoxLayout()
        self.label_layout = QtGui.QVBoxLayout()
        self.text_label = QtGui.QLabel()
        self.text_aqi = QtGui.QLabel()
        self.time_label = QtGui.QLabel()
        self.time_label.setStyleSheet("QLabel{font-size:10px;font-family:Roman times;}")
        self.text_label.setStyleSheet("QLabel{font-size:40px;font-family:Roman times;}")
        self.text_label.setText("AQI: ")        
        
        self.label_layout.addWidget(self.text_label)
        self.label_layout.addWidget(self.time_label)
        self.main_layout.addLayout(self.label_layout)
        self.main_layout.addWidget(self.text_aqi)
        self.setLayout(self.main_layout)
        
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint |  
                            QtCore.Qt.WindowCloseButtonHint |      
                            QtCore.Qt.FramelessWindowHint |      
                            QtCore.Qt.SubWindow |      
                            QtCore.Qt.WindowSystemMenuHint |      
                            QtCore.Qt.WindowStaysOnTopHint) 
        self.setWindowOpacity(0.7)
        self.text_label.show()
        self.update() 
        self.fetch_data_th = Fetch_Data_Thread()        
        self.fetch_data_th.data_signal.connect(self.show_aqi)
        self.fetch_data_th.start()
        
    def mouseDoubleClickEvent(self, e):
        QtGui.qApp.quit()
    def mouseMoveEvent(self, e):
        self.move(e.globalPos())
    def show_aqi(self, aqi_data, update_time):
        self.text_aqi.setText(aqi_data)
        try:
            aqi = int(aqi_data)
            color = str()
            if aqi <= 50:
                color = self.color_grade[0]
            elif aqi <= 100:
                color = self.color_grade[1]
            elif aqi <= 130:
                color = self.color_grade[2]
            elif aqi <= 250:
                color = self.color_grade[3]
            else:
                color = self.color_grade[4]
            self.text_aqi.setStyleSheet("QLabel{background-color:%s; border-radius:5px; text-align:center; border-width:5px; font-size:80px;font-weight:bold;font-family:Roman times;}" % color)
            self.text_aqi.setText(aqi_data)
            self.text_aqi.update()            
        except:
            self.text_aqi.setStyleSheet("QLabel{background-color:white}"
                                        "QLabel{font-size:50px;font-weight:bold;font-family:Roman times;}")
            self.text_aqi.setText("N/A")
        finally:
            if update_time:    
                self.time_label.setText(update_time)
            else:
                self.time_label.setText("N/A")
            self.time_label.update()
            self.text_aqi.update()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)    
    mycode = locale.getpreferredencoding()    
    code = QtCore.QTextCodec.codecForName(mycode)
    QtCore.QTextCodec.setCodecForLocale(code)
    widget = MyWidget()
    widget.show()
    sys.exit(app.exec_())
