from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QSpinBox, QPushButton, QTableWidget, QTableWidgetItem
import sys
import threading
import time
import random


adimSayisi = 0
normalQueue = []
oncelikliQueue = []
inQueue = []
waitQueue = []
availableTables = [1, 2, 3, 4, 5, 6]
customerCounter = 1
masaList = []
value1List = []
value2List = []
pixmapBos = object()
pixmapDolu = object()
waiterList = []
cookerList = []
kasa = object()
waiterL = [0, 1, 2]
kasaUI = object()


class Customer():
    def __init__(self, customer_no, table_no, table, pixmapBos, pixmapDolu, age):
        super().__init__()
        self.customer_no = customer_no
        self.table = table
        self.pixmapBos = pixmapBos
        self.pixmapDolu = pixmapDolu
        self.table_no = table_no
        self.age = age
        self.time = time.time()
        
    def calculate_time(self):
        while True:
            currTime = time.time()
            fark = currTime - self.time
            if fark >= 20 and self in waitQueue:
                index = waitQueue.index(self)
                del waitQueue[index]
                text = f"{self.customer_no} no'lu müşteri 20 saniye bekledikten sonra ayrıldı"
                Prb1Panel.addCustomerTable(text)
                break
            print(f"{self.customer_no} fark: {fark}\n")
            if self not in waitQueue:
                break
            time.sleep(1)
                   
    def sit_at_table(self):
        text = f"{self.customer_no} no'lu müşteri {self.table_no} masaya oturdu (Yaş: {self.age})"
        self.table.setPixmap(self.pixmapDolu)
        
        Prb1Panel.addCustomerTable(text)
        
    def to_order(self):
        global waiterList
        
        text = f"{self.customer_no} no'lu müşteri garson çağırdı"
        Prb1Panel.addCustomerTable(text)
        time.sleep(0.2)
        
    def take_order(self):
        text = f"{self.customer_no} no'lu müşteri siparişini aldı"
        Prb1Panel.addCustomerTable(text)
        self.eat_order()
    
    def eat_order(self):
        global kasaUI
        
        time.sleep(3)
        text = f"{self.customer_no} no'lu müşteri siparişini yedi"
        Prb1Panel.addCustomerTable(text)
        
        
        t = threading.Thread(target=(kasa.odeme), args=(self.customer_no, self))
        t.start()
            
    def pay(self):
        global kasa
        global inQueue
        global waitQueue
        global waiterL
        
        
        text = f"{self.customer_no} no'lu müşteri hesabı ödedi ve restorandan ayrıldı"
        self.table.setPixmap(self.pixmapBos)
        Prb1Panel.addCustomerTable(text)
        
        
        try:
            time.sleep(0.2)
            c = waitQueue.pop(0)
            inQueue.append(c)
            a = inQueue[inQueue.index(self)]
            c.table_no = a.table_no
            c.table = a.table
            
            t = threading.Thread(target=c.sit_at_table, args=())
            t.start()
            
            
            t = threading.Thread(target=c.to_order, args=())
            t.start()
        
            waiter = waiterList[waiterL[0]]
            waiterL.pop(0)
            if len(waiterL) == 0:
                waiterL = [0, 1, 2]
            time.sleep(1)
            
            t_siparis = threading.Thread(target=waiter.siparis_al, args=(c,))
            t_siparis.start()
            
        except Exception as e:
            print(e)
        


class Waiter():
    def __init__(self, waiter_no, waiterUI, pixmapBos, pixmapDolu):
        super().__init__()
        self.waiter_no = waiter_no
        self.table_no = 0
        self.lock = threading.Semaphore()
        self.cookerL = [0, 1]
        self.waiterUI = waiterUI
        self.pixmapBos = pixmapBos
        self.pixmapDolu = pixmapDolu
        
    def siparis_al(self, customer):
        self.lock.acquire()
        try:
            self.waiterUI.setPixmap(pixmapDolu)
            text = f"{self.waiter_no} no'lu garson {customer.customer_no} no'lu müşterinin siparişini alıyor\n"
            Prb1Panel.addWaiterTable(text)
            time.sleep(2)
            
            text = f"{self.waiter_no} no'lu garson {customer.customer_no} no'lu müşterinin siparişini aldı\n"
            Prb1Panel.addWaiterTable(text)
            self.mutfaga_ilet(customer)
            self.waiterUI.setPixmap(pixmapBos)
            time.sleep(0.2)

        finally:
            self.lock.release()
            
    def mutfaga_ilet(self, customer):
        global cookerList
    
        text = f"{self.waiter_no} no'lu garson {customer.customer_no} no'lu müşterinin siparişini mutfağa iletti\n"
        Prb1Panel.addWaiterTable(text)
        
        cooker = cookerList[self.cookerL[0]]
        self.cookerL.pop(0)
        if len(self.cookerL) == 0:
            self.cookerL = [0, 1]
        
        cooker.siparis_hazirla(customer)
    
    def siparis_teslim(self, customer):
        self.lock.acquire()
        try:
            text = f"{self.waiter_no} no'lu garson {customer.customer_no} no'lu müşterinin siparişini teslim etti\n"
            Prb1Panel.addWaiterTable(text)
            
            t = threading.Thread(target=customer.take_order, args=())
            t.start()
            
            
        finally:
            self.lock.release()

class Cooker():
    def __init__(self, cooker_no, cookerUI, pixmapBos, pixmapDolu):
        super().__init__() 
        self.cooker_no = cooker_no
        self.table_no = 0
        self.semaphore = threading.Semaphore(2)
        self.cookerUI = cookerUI
        self.pixmapBos = pixmapBos
        self.pixmapDolu = pixmapDolu
        
    def siparis_hazirla(self, customer):
        self.semaphore.acquire()
        try:
            self.cookerUI.setPixmap(self.pixmapDolu)
            text = f"{self.cooker_no} no'lu aşçı {customer.customer_no} no'lu müşterinin siparişini hazırlıyor\n"
            Prb1Panel.addCookerTable(text)
            time.sleep(3)
            self.siparis_hazir(customer)
        finally:
            self.semaphore.release()
        
        
    def siparis_hazir(self, customer):
        self.cookerUI.setPixmap(pixmapBos)
        text = f"{self.cooker_no} no'lu aşçı {customer.customer_no} no'lu müşterinin siparişini hazırladı\n"
        Prb1Panel.addCookerTable(text)

        waiterL = [0, 1, 2]
        waiter = waiterList[waiterL[0]]
        waiterL.pop(0)
        if len(waiterL) == 0:
            waiterL = [0, 1, 2]
        
        #waiter.siparis_teslim(customer_no)
        #t_siparis = threading.Thread(target=waiter.siparis_teslim, args=(customer,))
        #t_siparis.start()

        t = threading.Thread(target=customer.take_order, args=())
        t.start()


class Kasa():
    def __init__(self, kasaUI, pixmapBos, pixmapDolu):
        self.semaphore = threading.Semaphore()
        self.kasaUI = kasaUI
        self.pixmapBos = pixmapBos
        self.pixmapBosDolu = pixmapDolu
        
    def odeme(self, customer_no, customer):
        self.semaphore.acquire()
        try:
            self.kasaUI.setPixmap(pixmapDolu)
            time.sleep(1)
            text = f"{customer_no} no'lu müşterinin ödemesi alındı"
            Prb1Panel.addKasaTable(text)
            self.kasaUI.setPixmap(pixmapBos)
            t = threading.Thread(target=(customer.pay), args=())
            t.start()
            time.sleep(0.2)
            
        finally:
            self.semaphore.release()




class LoginPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YazLab 1.3")
        self.move(220, 80)
        self.setFixedSize(700, 500)
        self.initUI()

    def initUI(self):
        self.backgroundLabel = QLabel(self)
        pixmap = QPixmap('img/image.png')
        self.backgroundLabel.setPixmap(pixmap)
        
        self.backgroundLabel.setGeometry(0, 0, self.width(), self.height())
        self.backgroundLabel.setScaledContents(True)        
        
        self.btnPrb1 = QtWidgets.QPushButton(self)
        self.btnPrb1.setEnabled(True)
        self.btnPrb1.setGeometry(QtCore.QRect(235, 210, 230, 70))
        font = QtGui.QFont()
        font.setFamily("Noto Serif Cond")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.btnPrb1.setFont(font)
        self.btnPrb1.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.btnPrb1.setObjectName("btnPrb1")
        self.btnPrb1.clicked.connect(self.btn1)
        
        
        self.btnPrb2 = QtWidgets.QPushButton(self)
        self.btnPrb2.setEnabled(True)
        self.btnPrb2.setGeometry(QtCore.QRect(235, 320, 231, 71))
        font = QtGui.QFont()
        font.setFamily("Noto Serif Cond")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.btnPrb2.setFont(font)
        self.btnPrb2.setObjectName("btnPrb2")
        self.btnPrb2.clicked.connect(self.btn2)
        
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(270, 20, 151, 51))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(235, 90, 231, 61))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "YazLab 1.3"))
        self.btnPrb1.setText(_translate("Form", "Problem 1"))
        self.btnPrb2.setText(_translate("Form", "Problem 2"))
        self.label.setText(_translate("Form", "KOU YazLab 1.3"))
        self.label_2.setText(_translate("Form", "Restoran Yönetim Sistemi"))
     
        
    def btn1(self):
        self.prbPanel1 = Prb1Panel()
        self.prbPanel1.show()
        self.setVisible(False)


    def btn2(self):
        self.prbPanel2 = Prb2Panel()
        self.prbPanel2.show()
        self.setVisible(False)
    
    
class Prb1Panel(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Problem 1")
        self.move(220, 80)
        self.setFixedSize(700, 500)
        self.initUI()
        
        font = QFont()
        font.setBold(True)
        
        # Tablo tanımları
        Prb1Panel.customerTable = QTableWidget(self)
        Prb1Panel.customerTable.setColumnCount(1)
        Prb1Panel.customerTable.move(20, 200)
        Prb1Panel.customerTable.setFixedSize(400, 550)
        Prb1Panel.customerTable.setVisible(False)
        Prb1Panel.customerTable.setHorizontalHeaderLabels(["Müşteri"])
        Prb1Panel.customerTable.horizontalHeader().setFont(font)
        Prb1Panel.customerTable.setColumnWidth(0, 400)
        
        Prb1Panel.waiterTable = QTableWidget(self)
        Prb1Panel.waiterTable.setColumnCount(1)
        Prb1Panel.waiterTable.move(450, 200)
        Prb1Panel.waiterTable.setFixedSize(400,550)
        Prb1Panel.waiterTable.setVisible(False)
        Prb1Panel.waiterTable.setHorizontalHeaderLabels(["Garson"])
        Prb1Panel.waiterTable.horizontalHeader().setFont(font)
        Prb1Panel.waiterTable.setColumnWidth(0, 400)
        

        Prb1Panel.cookerTable = QTableWidget(self)
        Prb1Panel.cookerTable.setColumnCount(1)
        Prb1Panel.cookerTable.move(880, 200)
        Prb1Panel.cookerTable.setFixedSize(400,550)
        Prb1Panel.cookerTable.setVisible(False)
        Prb1Panel.cookerTable.setHorizontalHeaderLabels(["Aşçı"])
        Prb1Panel.cookerTable.horizontalHeader().setFont(font)
        Prb1Panel.cookerTable.setColumnWidth(0, 400)
        
        Prb1Panel.kasaTable = QTableWidget(self)
        Prb1Panel.kasaTable.setColumnCount(1)
        Prb1Panel.kasaTable.move(1310, 200)
        Prb1Panel.kasaTable.setFixedSize(400,550)
        Prb1Panel.kasaTable.setVisible(False)
        Prb1Panel.kasaTable.setHorizontalHeaderLabels(["Kasa"])
        Prb1Panel.kasaTable.horizontalHeader().setFont(font)
        Prb1Panel.kasaTable.setColumnWidth(0, 400)


        Prb1Panel.pixmapBos = QtGui.QPixmap('img/bos.jpg')
        Prb1Panel.pixmapDolu = QtGui.QPixmap('img/dolu.jpg')
        



    def initUI(self):
        self.normalSpnList = []
        self.oncelikSpnList = []
        self.lblList = []
        
        self.backgroundLabel = QtWidgets.QLabel(self)
        pixmap = QtGui.QPixmap('img/image.png')
        self.backgroundLabel.setPixmap(pixmap)
        self.backgroundLabel.setGeometry(0, 0, self.width(), self.height())
        self.backgroundLabel.setScaledContents(True)
        
        
        
        # Adım sayısı giriniz QLabel
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(250, 80, 170, 70))
        self.label.setText("Adım Sayısı Giriniz")
        font = QtGui.QFont()
        font.setFamily("Noto Serif Georgian")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        
        self.inputAdimSayisi = QLineEdit(self)
        self.inputAdimSayisi.setGeometry(QtCore.QRect(290, 150, 81, 61))
        font = QtGui.QFont()
        font.setFamily("Noto Sans Lao")
        font.setBold(True)
        font.setWeight(75)
        self.inputAdimSayisi.setFont(font)
        self.inputAdimSayisi.setObjectName("inputAdimSayisi")
        
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setText("Onayla")
        self.pushButton.setGeometry(QtCore.QRect(270, 250, 121, 51))
        font = QtGui.QFont()
        font.setFamily("Noto Sans Lao")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")    
        self.pushButton.clicked.connect(self.btn1)
        
    
    def btn1(self):
        global adimSayisi
        adimSayisi = self.inputAdimSayisi.text()
        
        self.label.close()
        self.inputAdimSayisi.close()
        self.pushButton.close()
        
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        
        self.lblNormal = QLabel("Normal Müşteri", self)
        self.lblNormal.move(190, 10)
        self.lblNormal.setFont(font)
        #self.lblNormal.setStyleSheet("color : white")
        self.lblNormal.setVisible(True)
        
        
        self.lblOncelik = QLabel("Öncelikli Müşteri", self)
        self.lblOncelik.move(400, 10)
        self.lblOncelik.setFont(font)
        #self.lblNormal.setStyleSheet("color : white")
        self.lblOncelik.setVisible(True)
        
        
        for i in range(int(adimSayisi)):
            text = str(i+1) + ". adım"
    
            self.lbl = QLabel(text, self)
            self.lbl.move(20, 50 + i*60)
            self.lbl.setFont(font)
            #self.lblNormal.setStyleSheet("color : white")
            self.lbl.setVisible(True)
            self.lblList.append(self.lbl)
            
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            
            self.spnNormal = QSpinBox(self)
            self.spnNormal.move(230, 50 + i*60)
            self.spnNormal.setFont(font)
            self.spnNormal.setVisible(True)
            self.normalSpnList.append(self.spnNormal)
            
            self.spnOncelik = QSpinBox(self)
            self.spnOncelik.move(440, 50 + i*60)
            self.spnOncelik.setFont(font)
            self.spnOncelik.setVisible(True)
            self.oncelikSpnList.append(self.spnOncelik)
        
        
        
        self.pushButton = QPushButton(self)
        self.pushButton.setText("Simülasyonu Başlat")
        self.pushButton.setFont(font)
        self.pushButton.resize(200, 60)
        self.pushButton.move(240, 375)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setVisible(True)
        self.pushButton.clicked.connect(self.btn2)
        
        print("Adım Sayısı: ", adimSayisi)
        pass
    
    
    def btn2(self):
        global adimSayisi
        global inQueue
        global oncelikliQueue
        global normalQueue
        global customerCounter
        global value1List
        global value2List
        global pixmapDolu
        global pixmapBos
        global waiterList
        global cookerList
        global kasa
        global kasaUI
        
        self.lblNormal.close()
        self.lblOncelik.close()
        self.pushButton.close()
        
        font = QFont()
        font.setBold(True)
        
        
        Prb1Panel.customerTable.setVisible(True)
        Prb1Panel.waiterTable.setVisible(True)
        Prb1Panel.cookerTable.setVisible(True)
        Prb1Panel.kasaTable.setVisible(True)
        
        
        for i in range(int(adimSayisi)):
            value1List.append(self.oncelikSpnList[i].value())  
            value2List.append(self.normalSpnList[i].value())
        
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        
        self.lblMasa = QLabel("Masalar", self)
        self.lblMasa.move(170, 10)
        self.lblMasa.setFont(font)
        #self.lblNormal.setStyleSheet("color : white")
        self.lblMasa.setVisible(True)
        
        
        pixmapBos = QtGui.QPixmap('img/bos.jpg')
        pixmapDolu = QtGui.QPixmap('img/dolu.jpg')
        
        self.masa1 = QtWidgets.QLabel(self)
        self.masa1.setPixmap(pixmapBos)
        self.masa1.setGeometry(70, 50, 40, 40)
        self.masa1.setVisible(True)
        self.masa1.setScaledContents(True)
        masaList.append(self.masa1)
        
        self.masa2 = QtWidgets.QLabel(self)
        self.masa2.setPixmap(pixmapBos)
        self.masa2.setGeometry(180, 50, 40, 40)
        self.masa2.setVisible(True)
        self.masa2.setScaledContents(True)
        masaList.append(self.masa2)
                
        self.masa3 = QtWidgets.QLabel(self)
        self.masa3.setPixmap(pixmapBos)
        self.masa3.setGeometry(290, 50, 40, 40)
        self.masa3.setVisible(True)
        self.masa3.setScaledContents(True)
        masaList.append(self.masa3)
        
        self.masa4 = QtWidgets.QLabel(self)
        self.masa4.setPixmap(pixmapBos)
        self.masa4.setGeometry(70, 120, 40, 40)
        self.masa4.setVisible(True)
        self.masa4.setScaledContents(True)
        masaList.append(self.masa4)
        
        self.masa5 = QtWidgets.QLabel(self)
        self.masa5.setPixmap(pixmapBos)
        self.masa5.setGeometry(180, 120, 40, 40)
        self.masa5.setVisible(True)
        self.masa5.setScaledContents(True)
        masaList.append(self.masa5)
        
        self.masa6 = QtWidgets.QLabel(self)
        self.masa6.setPixmap(pixmapBos)
        self.masa6.setGeometry(290, 120, 40, 40)
        self.masa6.setVisible(True)
        self.masa6.setScaledContents(True)
        masaList.append(self.masa6)
        
        
        self.lblGarson = QLabel("Garsonlar", self)
        self.lblGarson.move(610, 10)
        self.lblGarson.setFont(font)
        self.lblGarson.setVisible(True)
          
        self.garson1 = QtWidgets.QLabel(self)
        self.garson1.setPixmap(pixmapBos)
        self.garson1.setGeometry(530, 70, 40, 60)
        self.garson1.setVisible(True)
        self.garson1.setScaledContents(True)
        garson = Waiter(1, self.garson1, pixmapBos=pixmapBos, pixmapDolu=pixmapDolu)
        waiterList.append(garson)
        
        self.garson2 = QtWidgets.QLabel(self)
        self.garson2.setPixmap(pixmapBos)
        self.garson2.setGeometry(630, 70, 40, 60)
        self.garson2.setVisible(True)
        self.garson2.setScaledContents(True)
        garson = Waiter(2, self.garson2, pixmapBos=pixmapBos, pixmapDolu=pixmapDolu)
        waiterList.append(garson)
        
        self.garson3 = QtWidgets.QLabel(self)
        self.garson3.setPixmap(pixmapBos)
        self.garson3.setGeometry(730, 70, 40, 60)
        self.garson3.setVisible(True)
        self.garson3.setScaledContents(True)
        garson = Waiter(3, self.garson3, pixmapBos=pixmapBos, pixmapDolu=pixmapDolu)
        waiterList.append(garson)
        
        
        
        self.lblAsci = QLabel("Aşçılar", self)
        self.lblAsci.move(1020, 10)
        self.lblAsci.setFont(font)
        self.lblAsci.setVisible(True)
        
        
        self.asci1 = QtWidgets.QLabel(self)
        self.asci1.setPixmap(pixmapBos)
        self.asci1.setGeometry(1000, 70, 40, 60)
        self.asci1.setVisible(True)
        self.asci1.setScaledContents(True)
        asci = Cooker(1, self.asci1, pixmapBos=pixmapBos, pixmapDolu=pixmapDolu)
        cookerList.append(asci)
        
        self.asci2 = QtWidgets.QLabel(self)
        self.asci2.setPixmap(pixmapBos)
        self.asci2.setGeometry(1060, 70, 40, 60)
        self.asci2.setVisible(True)
        self.asci2.setScaledContents(True)
        asci = Cooker(2, self.asci2, pixmapBos=pixmapBos, pixmapDolu=pixmapDolu)
        cookerList.append(asci)
    
        self.lblKasa = QLabel("Kasa", self)
        self.lblKasa.move(1450, 10)
        self.lblKasa.setFont(font)
        self.lblKasa.setVisible(True)
        
        self.kasa = QtWidgets.QLabel(self)
        self.kasa.setPixmap(pixmapBos)
        self.kasa.setGeometry(1450, 70, 60, 60)
        self.kasa.setVisible(True)
        self.kasa.setScaledContents(True)
        kasa = Kasa(self.kasa, pixmapBos=pixmapBos, pixmapDolu=pixmapDolu)
        kasaUI = self.kasa
        
        for lbl in self.lblList:
            lbl.close()
        
        for normal in self.normalSpnList:
            normal.close()
        
        for oncelik in self.oncelikSpnList:
            oncelik.close()
        
        self.setFixedSize(1750, 800)
        self.backgroundLabel.setGeometry(0, 0, self.width(), self.height())
        t = threading.Thread(target=run, args=())
        t.start()
    
    
    def addCustomerTable(text):
        currRowNum = Prb1Panel.customerTable.rowCount()
        Prb1Panel.customerTable.setRowCount(currRowNum + 1)
        
        item = QTableWidgetItem(text)
        Prb1Panel.customerTable.setItem(currRowNum, 0, item)
    
    def addWaiterTable(text):
        currRowNum = Prb1Panel.waiterTable.rowCount()
        Prb1Panel.waiterTable.setRowCount(currRowNum + 1)
        
        item = QTableWidgetItem(text)
        Prb1Panel.waiterTable.setItem(currRowNum, 0, item)
    
    def addCookerTable(text):
        currRowNum = Prb1Panel.cookerTable.rowCount()
        Prb1Panel.cookerTable.setRowCount(currRowNum + 1)
        
        item = QTableWidgetItem(text)
        Prb1Panel.cookerTable.setItem(currRowNum, 0, item)
    
    def addKasaTable(text):
        currRowNum = Prb1Panel.kasaTable.rowCount()
        Prb1Panel.kasaTable.setRowCount(currRowNum + 1)
        
        item = QTableWidgetItem(text)
        Prb1Panel.kasaTable.setItem(currRowNum, 0, item)



class Prb2Panel(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Problem 2")
        self.move(220, 80)
        self.setFixedSize(700, 500)
        self.initUI()
        
        font = QFont()
        font.setBold(True)
        
        # Sonuç Tablosu
        Prb2Panel.resultTable = QTableWidget(self)
        Prb2Panel.resultTable.setColumnCount(1)
        Prb2Panel.resultTable.setRowCount(6)
        Prb2Panel.resultTable.move(100, 70)
        Prb2Panel.resultTable.setFixedSize(500, 250)
        Prb2Panel.resultTable.setVisible(False)
        Prb2Panel.resultTable.setHorizontalHeaderLabels(["Sonuç"])
        Prb2Panel.resultTable.horizontalHeader().setFont(font)
        Prb2Panel.resultTable.setColumnWidth(0, 500)

    def initUI(self):
        self.backgroundLabel = QtWidgets.QLabel(self)
        pixmap = QtGui.QPixmap('img/image.png')
        self.backgroundLabel.setPixmap(pixmap)
        self.backgroundLabel.setGeometry(0, 0, self.width(), self.height())
        self.backgroundLabel.setScaledContents(True)

        
        self.inputSaniye= QLineEdit(self)
        self.inputSaniye.setGeometry(QtCore.QRect(200, 170, 40, 30))
        font = QtGui.QFont()
        font.setFamily("Noto Sans Lao")
        font.setBold(True)
        font.setWeight(75)
        self.inputSaniye.setFont(font)
        self.inputSaniye.setObjectName("inputAdimSayisi")
        
        self.labelSaniye = QtWidgets.QLabel(self)
        self.labelSaniye.setGeometry(QtCore.QRect(250, 170, 85, 30))
        self.labelSaniye.setText("saniyede")
        font = QtGui.QFont()
        font.setFamily("Noto Serif Georgian")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.labelSaniye.setFont(font)
        self.labelSaniye.setObjectName("labelSaniye")
        
        self.inputCustomer= QLineEdit(self)
        self.inputCustomer.setGeometry(QtCore.QRect(350, 170, 40, 30))
        font = QtGui.QFont()
        font.setFamily("Noto Sans Lao")
        font.setBold(True)
        font.setWeight(75)
        self.inputCustomer.setFont(font)
        self.inputCustomer.setObjectName("inputCustomer")
        
        
        self.labelCustomer = QtWidgets.QLabel(self)
        self.labelCustomer.setGeometry(QtCore.QRect(400, 170, 85, 30))
        self.labelCustomer.setText("müşteri")
        font = QtGui.QFont()
        font.setFamily("Noto Serif Georgian")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.labelCustomer.setFont(font)
        self.labelCustomer.setObjectName("labelCustomer")
        
        self.labelSure = QtWidgets.QLabel(self)
        self.labelSure.setGeometry(QtCore.QRect(220, 200, 170, 70))
        self.labelSure.setText("Süre (Saniye): ")
        font = QtGui.QFont()
        font.setFamily("Noto Serif Georgian")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.labelSure.setFont(font)
        self.labelSure.setObjectName("labelSure")
        
        
        self.inputSure= QLineEdit(self)
        self.inputSure.setGeometry(QtCore.QRect(360, 210, 60, 40))
        font = QtGui.QFont()
        font.setFamily("Noto Sans Lao")
        font.setBold(True)
        font.setWeight(75)
        self.inputSure.setFont(font)
        self.inputSure.setObjectName("inputCustomer")
        
        self.btnStart = QtWidgets.QPushButton(self)
        self.btnStart.setEnabled(True)
        self.btnStart.setGeometry(QtCore.QRect(270, 300, 120, 50))
        font = QtGui.QFont()
        font.setFamily("Noto Serif Cond")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.btnStart.setFont(font)
        self.btnStart.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.btnStart.setObjectName("btnStart")
        self.btnStart.clicked.connect(self.run)
        self.btnStart.setText("Hesapla")
    
    
    def run(self):
        tmpKazanc = 0
        kazanc = 0
        
        table = 3
        waiter = 1
        cooker = 1
           
           
        kazanc = self.calculate(table, waiter, cooker)
        print(kazanc)
        
        # Optimum masa sayısını hesaplayan döngü
        while tmpKazanc < kazanc:
            table += 1
            tmpKazanc = kazanc
            kazanc = self.calculate(table, waiter, cooker) 
        table -= 1
        print(f"Optimum masa sayısı: {table}")
        
        waiter += 1
        kazanc = self.calculate(table, waiter, cooker)
        if tmpKazanc < kazanc:
        # Optimum garson sayısını hesaplayan döngü
            while tmpKazanc < kazanc:
                waiter += 1
                tmpKazanc = kazanc
                kazanc = self.calculate(table, waiter, cooker)
            waiter -= 1
        else:
            waiter -= 1
        
        print(f"Optimum garson sayısı {waiter}")
        cooker += 1
        kazanc = self.calculate(table, waiter, cooker)
        if tmpKazanc < kazanc:
        # Optimum aşçı sayısını hesaplayan döngü
            while tmpKazanc < kazanc:
                cooker += 1
                tmpKazanc = kazanc
                kazanc = self.calculate(table, waiter, cooker)
            cooker -= 1
        else:
            cooker -= 1
        print(f"Optimum aşçı sayısı: {cooker}")
        
        print(kazanc)
        
        self.inputSaniye.close()
        self.labelSaniye.close()
        self.inputCustomer.close()
        self.labelCustomer.close()
        self.inputSure.close()
        self.labelSure.close()
        self.btnStart.close()
        
    def calculate(self, table, waiter, cooker):
        saniye = int(self.inputSaniye.text())
        customer = int(self.inputCustomer.text())
        topSure = int(self.inputSure.text())
        checkGidis = []
        checkWaiter = [0 for i in range(waiter)]
        checkCooker = [2 for i in range(cooker*2)]
        leftCounter = 0
        waiterList = []
        cookerList = []
        
        totalCustomer = (topSure // saniye) * customer
        customers = []
    

        for i in range(topSure // saniye):
            for j in range(customer):
                customers.append({})
                customers[-1]["gelis"] = i * saniye

        for i in range(max(table, customer)):
            # Müşterinin restorana giriş saniyesi belirlenir
            customers[i]["giris"] = customers[i]["gelis"]
            
            # Müşterinin siparişinin alındığı saniye belirlenir
            index = checkWaiter.index(min(checkWaiter))
            if min(checkWaiter) < customers[i]["giris"]:
                takeOrder = customers[i]["giris"] + 2
            else:
                takeOrder = min(checkWaiter) + 2
            customers[i]["takeOrder"] = min(checkWaiter) + 2
            del checkWaiter[index]
            checkWaiter.append(customers[i]["takeOrder"])
            
            if i <= waiter:
                waiterList.append(customers[i]["takeOrder"])
            
            # Müşterinin siparişinin hazır olduğu saniye belirlenir
            index = checkCooker.index(min(checkCooker))
            if min(checkCooker) < customers[i]["takeOrder"]:
                readyOrder = customers[i]["takeOrder"] + 3
            else:
                readyOrder = min(checkCooker) + 3
            customers[i]["readyOrder"] = readyOrder
            del checkCooker[index]
            checkCooker.append(customers[i]["readyOrder"])
            
            if i <= cooker:
                cookerList.append(customers[i]["readyOrder"])
            
            # Müşterinin ayrıldığı saniye belirlenir
            gidis = customers[i]["readyOrder"] + 4
            
            if gidis in checkGidis:
                gidis += 1
            
            customers[i]["gidis"] = gidis
            checkGidis.append(customers[i]["gidis"])

        for i in range(max(table,customer), len(customers)):
            girisIndex = checkGidis.index(min(checkGidis))
            giris = checkGidis[girisIndex]
            
            # Müşterinin bekleme saniyesi kontrol edilir
            if giris - int(customers[i]["gelis"]) > 20:
                leftCounter += 1
                continue 
            
            customers[i]["giris"] = checkGidis[girisIndex]
            del checkGidis[girisIndex]
            
            # Müşterinin siparişinin alındığı saniye belirlenir
            takeOrderIndex = checkWaiter.index(min(checkWaiter))
            takeOrder = customers[i]["giris"] + 2
            
            if i < waiter:
                waiterList.append(takeOrder)
            elif takeOrder < min(checkWaiter):
                takeOrder = min(checkWaiter) + 2
            customers[i]["takeOrder"] = takeOrder
            del checkWaiter[takeOrderIndex]
            checkWaiter.append(customers[i]["takeOrder"])

            # Müşterinin siparişinin hazır olduğu saniye belirlenir
            readyOrderIndex = checkCooker.index(min(checkCooker))
            readyOrder = int(customers[i]["takeOrder"]) + 3
            if i < cooker:
                cookerList.append(readyOrder) 
            elif readyOrder < min(checkCooker):
                readyOrder = min(checkCooker) + 3
            customers[i]["readyOrder"] = readyOrder
            del checkCooker[readyOrderIndex] 
            checkCooker.append(customers[i]["readyOrder"])
            
            # Müşterinin restorandan ayrıldığı saniye belirlenir
            gidis = int(customers[i]["readyOrder"]) + 4
            if gidis in checkGidis:
                gidis += 1
            
            customers[i]["gidis"] = gidis
            checkGidis.append(gidis)
        
        # Kazanç hesaplanır = toplam müşteri - masa sayısı - garson sayısı - aşçı sayısı - ayrılan müşteri sayısı
        kazanc = totalCustomer - leftCounter - table - waiter - cooker
        
        Prb2Panel.resultTable.setVisible(True)
        text = f"Toplam Masa Sayısı: {table}"
        item = item = QTableWidgetItem(text)
        Prb2Panel.resultTable.setItem(0, 0, item)
        print(text)
        
        text = f"Toplam Garson Sayısı: {waiter}"
        item = item = QTableWidgetItem(text)
        Prb2Panel.resultTable.setItem(1, 0, item)
        print(text)
        
        text = f"Toplam Aşçı Sayısı: {cooker}"
        item = item = QTableWidgetItem(text)
        Prb2Panel.resultTable.setItem(2, 0, item)
        print(text)
        
        text = f"Toplam Müşteri sayısı: {totalCustomer}"
        item = item = QTableWidgetItem(text)
        Prb2Panel.resultTable.setItem(3, 0, item)
        print(text)
        
        text = f"Ayrılan müşteri sayısı: {leftCounter}"
        item = item = QTableWidgetItem(text)
        Prb2Panel.resultTable.setItem(4, 0, item)
        print(text)
        print("============================================")
        
        text = f"Toplam Kazanç: {kazanc}"
        item = item = QTableWidgetItem(text)
        Prb2Panel.resultTable.setItem(5, 0, item)
        print(text)
        print("============================================")
        
        return kazanc
        
        
def run():
    global value1List
    global value2List
    global pixmapBos
    global pixmapDolu
    global customerCounter
    global normalQueue
    global oncelikliQueue
    global inQueue
    global availableTables
    global waiterL
    global waitQueue
    
    # Toplam müşteri sayısı hesaplanıyor
    total = 0
    totalOncelik = 0
    
    # value1List öncelikli müşteriler 
    for value in value1List:
        total += value
        totalOncelik += value
    # value2List normal müşteriler
    for value in value2List:
        total += value
        
    print(f"Toplam {total} müşteri geldi. {totalOncelik} öncelikli")
    time.sleep(0.5)
    
    # Döngü adım sayısı kadar döner
    for i in range(int(adimSayisi)):
        value1 = value1List[i]
        value2 = value2List[i]
        
        # o adımdaki öncelikli müşterilerin thread ini tutacak bir list tanımlanır
        l = []
        # o adımdaki öncelikli müşteri sayısı kadar döngü döner
        for _ in range(value1):
            # her müşteri için thread açılır
            age = random.randint(65, 86)
            customer = Customer(customer_no=customerCounter, table_no=availableTables[0], table=masaList[availableTables[0]-1], pixmapBos=pixmapBos, pixmapDolu=pixmapDolu, age=age)
            availableTables.pop(0)
            if len(availableTables) == 0:
                availableTables = [1, 2, 3, 4, 5, 6]
            customerCounter += 1
            l.append(customer)
        # tüm öncelikli müşterileri tutan list e adımdaki liste eklenir
        oncelikliQueue.append(l)
        
        
        # adımdaki normal müşterileri tutan list tanımlanır
        l = []
        # adımdaki normal müşteri sayısı kadar döngü döner
        for _ in range(value2):
            # her müşteri için thread oluşturulur
            age = random.randint(15, 65)
            customer = Customer(customer_no=customerCounter, table_no=availableTables[0], table=masaList[availableTables[0]-1], pixmapBos=pixmapBos, pixmapDolu=pixmapDolu, age=age)
            availableTables.pop(0)
            if len(availableTables) == 0:
                availableTables = [1, 2, 3, 4, 5, 6]
            customerCounter += 1
            l.append(customer)
        # tüm normal müşterileri tutan list e  adımdaki list eklenir
        normalQueue.append(l)
    
    kalan = 6
    
    for i in range(int(adimSayisi)):
        num1 = len(oncelikliQueue[i])
        if num1 >= kalan:
            inQueue += oncelikliQueue[i][:kalan]
            oncelikliQueue[i] = oncelikliQueue[i][kalan:]
        else:
            inQueue += oncelikliQueue[i]
            oncelikliQueue[i] = []
            
        kalan -= num1
        num2 = len(normalQueue[i])
        if num2 >= kalan:
            inQueue += normalQueue[i][:kalan]
            normalQueue[i] = normalQueue[i][kalan:]
        else:
            inQueue += normalQueue[i]
            normalQueue[i] = []
            
        kalan -= num2
        if kalan <= 0:
            break
    
    normalQueue = list(filter(lambda x: x != [], normalQueue))
    oncelikliQueue = list(filter(lambda x: x != [], oncelikliQueue))
    
    totalNormal = 0
    totalOncelikli = 0
    
    for normal in normalQueue:
        totalNormal += len(normal)
    for oncelik in oncelikliQueue:
        totalOncelikli += len(oncelik)
    
    for customer in inQueue:
        t = threading.Thread(target=customer.sit_at_table, args=())
        t.start()
        t.join()
        time.sleep(0.5)
    print(f"{totalNormal + totalOncelikli} müşteri beklemede. {totalOncelikli} öncelikli")
    print("=========================================================")

    
    for queue in oncelikliQueue:
        waitQueue += queue
    for queue in normalQueue:
        waitQueue += queue
    
    for customer in waitQueue:
        t = threading.Thread(target=customer.calculate_time, args=())
        t.start()
    
    #while len(inQueue) != 0:
    # Garson Çağırma
    for customer in inQueue:
            t = threading.Thread(target=customer.to_order, args=())
            t.start()
            t.join()
            
    for customer in inQueue:
        waiter = waiterList[waiterL[0]]
        waiterL.pop(0)
        if len(waiterL) == 0:
            waiterL = [0, 1, 2]
        time.sleep(1)
                            
        t_siparis = threading.Thread(target=waiter.siparis_al, args=(customer,))
        t_siparis.start()
    
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    loginPanel = LoginPanel()

    loginPanel.show()

    sys.exit(app.exec_())