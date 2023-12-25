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
pixmapBos = int()
pixmapDolu = int()
waiterList = []
cookerList = []
kasa = int()
waiterL = [0, 1, 2]


class Customer():
    def __init__(self, customer_no, table_no, table, pixmapBos, pixmapDolu, age):
        super().__init__()
        self.customer_no = customer_no
        self.table = table
        self.pixmapBos = pixmapBos
        self.pixmapDolu = pixmapDolu
        self.table_no = table_no
        self.age = age
        
    def sit_at_table(self):
        text = f"{self.customer_no} no'lu müşteri {self.table_no} masaya oturdu (Yaş: {self.age})"
        print(text)
        
        Prb1Panel.addCustomerTable(text)
        
    def to_order(self):
        global waiterList
        
        text = f"{self.customer_no} no'lu müşteri garson çağırdı"
        print(text)
        Prb1Panel.addCustomerTable(text)
        time.sleep(0.2)
        
    def take_order(self):
        text = f"{self.customer_no} no'lu müşteri siparişini aldı"
        print(text)
        Prb1Panel.addCustomerTable(text)
        self.eat_order()
    
    def eat_order(self):
        time.sleep(3)
        text = f"{self.customer_no} no'lu müşteri siparişini yedi"
        print(text)
        Prb1Panel.addCustomerTable(text)
        
        time.sleep(1)
        t = threading.Thread(target=(self.pay()), args=())
        t.start()    
            
    def pay(self):
        global kasa
        global inQueue
        global waitQueue
        global waiterL
        
        
        text = f"{self.customer_no} no'lu müşteri hesabı ödedi ve restorandan ayrıldı"
        print(text)
        
        Prb1Panel.addCustomerTable(text)
        kasa.odeme(self.customer_no)
        
        try:
            time.sleep(0.2)
            print("Yeni müşteri geldi!!!!!!")
            c = waitQueue.pop(0)
            inQueue.append(c)
            a = inQueue[inQueue.index(self)]
            print(type(c))
            c.table_no = a.table_no
            
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
    def __init__(self, waiter_no):
        super().__init__()
        self.waiter_no = waiter_no
        self.table_no = 0
        self.lock = threading.Semaphore()
        self.cookerL = [0, 1]
        
    def siparis_al(self, customer):
        self.lock.acquire()
        try:
            text = f"{self.waiter_no} no'lu garson {customer.customer_no} no'lu müşterinin siparişini alıyor\n"
            print(text) 
            Prb1Panel.addWaiterTable(text)
            time.sleep(2)
            
            text = f"{self.waiter_no} no'lu garson {customer.customer_no} no'lu müşterinin siparişini aldı\n"
            print(text)
            Prb1Panel.addWaiterTable(text)
            self.mutfaga_ilet(customer)

        finally:
            self.lock.release()
            
    def mutfaga_ilet(self, customer):
        global cookerList
    
        text = f"{self.waiter_no} no'lu garson {customer.customer_no} no'lu müşterinin siparişini mutfağa iletti\n"
        print(text)
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
            print(text)
            Prb1Panel.addWaiterTable(text)
            
            t = threading.Thread(target=customer.take_order, args=())
            t.start()
            
            
        finally:
            self.lock.release()

class Cooker():
    def __init__(self, cooker_no):
        super().__init__() 
        self.cooker_no = cooker_no
        self.table_no = 0
        self.semaphore = threading.Semaphore(2)
        
    def siparis_hazirla(self, customer):
        self.semaphore.acquire()
        try:
            text = f"{self.cooker_no} no'lu aşçı {customer.customer_no} no'lu müşterinin siparişini hazırlıyor\n"
            print(text)
            Prb1Panel.addCookerTable(text)
            time.sleep(3)
            self.siparis_hazir(customer)
        finally:
            self.semaphore.release()
        
        
    def siparis_hazir(self, customer):
        text = f"{self.cooker_no} no'lu aşçı {customer.customer_no} no'lu müşterinin siparişini hazırladı\n"
        print(text)
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
    def __init__(self):
        self.semaphore = threading.Semaphore()
        
    def odeme(self, customer_no):
        self.semaphore.acquire()
        try:
            text = f"{customer_no} no'lu müşterinin ödemesi alındı"
            print(text)
            Prb1Panel.addKasaTable(text)
            
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
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        
        self.lblMasa = QLabel("Masalar", self)
        self.lblMasa.move(100, 10)
        self.lblMasa.setFont(font)
        #self.lblNormal.setStyleSheet("color : white")
        self.lblMasa.setVisible(True)
        
        
        pixmapBos = QtGui.QPixmap('img/bos.jpg')
        pixmapDolu = QtGui.QPixmap('img/dolu.jpg')
        
        self.masa1 = QtWidgets.QLabel(self)
        self.masa1.setPixmap(pixmapBos)
        self.masa1.setGeometry(50, 50, 40, 40)
        self.masa1.setVisible(True)
        self.masa1.setScaledContents(True)
        masaList.append(self.masa1)
        
        self.masa2 = QtWidgets.QLabel(self)
        self.masa2.setPixmap(pixmapBos)
        self.masa2.setGeometry(120, 50, 40, 40)
        self.masa2.setVisible(True)
        self.masa2.setScaledContents(True)
        masaList.append(self.masa2)
                
        self.masa3 = QtWidgets.QLabel(self)
        self.masa3.setPixmap(pixmapBos)
        self.masa3.setGeometry(190, 50, 40, 40)
        self.masa3.setVisible(True)
        self.masa3.setScaledContents(True)
        masaList.append(self.masa3)
        
        self.masa4 = QtWidgets.QLabel(self)
        self.masa4.setPixmap(pixmapBos)
        self.masa4.setGeometry(50, 120, 40, 40)
        self.masa4.setVisible(True)
        self.masa4.setScaledContents(True)
        masaList.append(self.masa4)
        
        self.masa5 = QtWidgets.QLabel(self)
        self.masa5.setPixmap(pixmapBos)
        self.masa5.setGeometry(120, 120, 40, 40)
        self.masa5.setVisible(True)
        self.masa5.setScaledContents(True)
        masaList.append(self.masa5)
        
        self.masa6 = QtWidgets.QLabel(self)
        self.masa6.setPixmap(pixmapBos)
        self.masa6.setGeometry(190, 120, 40, 40)
        self.masa6.setVisible(True)
        self.masa6.setScaledContents(True)
        masaList.append(self.masa6)
        
        
        self.lblGarson = QLabel("Garsonlar", self)
        self.lblGarson.move(320, 10)
        self.lblGarson.setFont(font)
        self.lblGarson.setVisible(True)
          
        self.garson1 = QtWidgets.QLabel(self)
        self.garson1.setPixmap(pixmapBos)
        self.garson1.setGeometry(300, 50, 20, 40)
        self.garson1.setVisible(True)
        self.garson1.setScaledContents(True)
        garson = Waiter(1)
        waiterList.append(garson)
        
        self.garson2 = QtWidgets.QLabel(self)
        self.garson2.setPixmap(pixmapBos)
        self.garson2.setGeometry(350, 50, 20, 40)
        self.garson2.setVisible(True)
        self.garson2.setScaledContents(True)
        garson = Waiter(2)
        waiterList.append(garson)
        
        self.garson3 = QtWidgets.QLabel(self)
        self.garson3.setPixmap(pixmapBos)
        self.garson3.setGeometry(400, 50, 20, 40)
        self.garson3.setVisible(True)
        self.garson3.setScaledContents(True)
        garson = Waiter(3)
        waiterList.append(garson)
        
        
        
        self.lblAsci = QLabel("Aşçılar", self)
        self.lblAsci.move(510, 10)
        self.lblAsci.setFont(font)
        self.lblAsci.setVisible(True)
        
        
        self.asci1 = QtWidgets.QLabel(self)
        self.asci1.setPixmap(pixmapBos)
        self.asci1.setGeometry(500, 50, 20, 40)
        self.asci1.setVisible(True)
        self.asci1.setScaledContents(True)
        asci = Cooker(1)
        cookerList.append(asci)
        
        self.asci2 = QtWidgets.QLabel(self)
        self.asci2.setPixmap(pixmapBos)
        self.asci2.setGeometry(550, 50, 20, 40)
        self.asci2.setVisible(True)
        self.asci2.setScaledContents(True)
        asci = Cooker(2)
        cookerList.append(asci)
    
        self.lblKasa = QLabel("Kasa", self)
        self.lblKasa.move(660, 10)
        self.lblKasa.setFont(font)
        self.lblKasa.setVisible(True)
        
        self.kasa = QtWidgets.QLabel(self)
        self.kasa.setPixmap(pixmapBos)
        self.kasa.setGeometry(650, 50, 60, 60)
        self.kasa.setVisible(True)
        self.kasa.setScaledContents(True)
        kasa = Kasa()
        
        
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
        self.btnStart.setText("Başlat")
        
    def run(self):
        saniye = int(self.inputSaniye.text())
        customer = int(self.inputCustomer.text())
        topSure = int(self.inputSure.text())
        
        
        self.inputSaniye.close()
        self.labelSaniye.close()
        self.inputCustomer.close()
        self.labelCustomer.close()
        self.inputSure.close()
        self.labelSure.close()
        self.btnStart.close()
        
    
    
    
    
        
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