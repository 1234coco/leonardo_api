from PyQt5.QtWidgets import *
from PyQt5 import uic
from selenium import webdriver
import mauvh
import time
import json
import sys
import threading

from PIL import Image
class main_app(QMainWindow):
    def __init__(self):
        self.image = None
        self.cookie = None
        self.cookies = None
        self.token = None
        self.toking = None
        self.tokin = None
        self.sub = None
        self.promt = None
        self.name = None
        super(main_app,self).__init__()
        uic.loadUi("RUN\\UI.ui",self)
        self.get_cookie.clicked.connect(self.tab_logins)
        self.get_jwt.clicked.connect(self.getJWT)
        self.send_without_image.clicked.connect(self.sendImage)
        self.see_without_image.clicked.connect(self.seeImage)
        self.save_without_image.clicked.connect(self.saveImage)
        self.show()
        #print(vars(self))
    def saveImage(self):
        a = QFileDialog.getExistingDirectory(
            self,
            "Chọn thư mục lưu."
        )
        mauvh.save_image(self.name,self.image,a)
    def seeImage(self):
        mauvh.show_image(self.image,self.name,self.cookies)
    def sendImage(self):
        print(self.token)
        self.toking = json.loads(self.token)
        self.sub = self.toking["user"]["sub"]
        self.tokin = self.toking["accessToken"]
        print("\n"+str(self.sub)+"\n"+str(self.tokin))
        userid = mauvh.get_user_id(self.tokin,self.sub)
        Au = mauvh.Authentication(self.tokin)
        a = mauvh.GenarationImage(Au,self.promt_without_image.toPlainText())
        self.promt = self.promt_without_image.toPlainText()
        self.image,self.name = mauvh.URL(userid,a,self.promt_without_image.toPlainText())
        print(self.image)
    def getJWT(self):
        #print(cookies)
        self.token = mauvh.get_user_token(self.cookies)
    def tab_logins(self):
        def login():
            driver = webdriver.Chrome()
            driver.get("https://app.leonardo.ai/auth/login")
            while True:
                if driver.current_url == "https://app.leonardo.ai/":
                    self.cookie = driver.get_cookies()
                    self.cookies = str()
                    for cook in self.cookie:
                        self.cookies += cook["name"]+"="+cook["value"]+";"
                    break
        logins = threading.Thread(target=login)
        logins.start()
        logins.join()
app = QApplication(sys.argv)
UIWindow = main_app()
app.exec_()

