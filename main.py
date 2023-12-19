from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QSpinBox, QPushButton
import sys
import threading
import time
 

adimSayisi = 0
normalQueue = []
oncelikliQueue = []
inQueue = []
musteriQueue = []

class Customer():
    def __init__(self, customer_no, table_no):
        super().__init__()
        self.customer_no = customer_no
        self.table_no = table_no
        
    def sit_at_table(self):
        print(f"{self.customer_no} no'lu müşteri {self.table_no} masaya oturdu")
        
    def to_order(self):
        print(f"{self.customer_no} no'lu müşteri sipariş verdi")
    
    def take_order(self):
        print(f"{self.customer_no} müşteri siparişini aldı")
    
    def pay(self):
        print("{self.customer_no} no'lu müşteri hesabı ödedi")
    
    def leave(self):
        print("{self.customer_no} no'lu müşteri restorandan ayrıldı")
    


class Waiter():
    def __init__(self):
        super().__init__() 
    
    def siparis_al():
        print("Müşteriden sipariş alındı")
    
    def mutfaga_ilet():
        print("Sipaiş mutfağa iletildi")
    
    def siparis_teslim():
        print("Sipariş teslim edildi")
        

class Cooker():
    def __init__(self):
        super().__init__() 
    
    def siparis_hazirla(self):
        print("Sipariş hazırlanıyor")
    
    def siparis_hazir(self):
        print("Sipariş hazırlandı")



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
        
        self.lblNormal.close()
        self.lblOncelik.close()
        self.pushButton.close()
        
        # Döngü adım sayısı kadar döner
        for i in range(int(adimSayisi)):
            value1 = self.oncelikSpnList[i].value()  
            value2 = self.normalSpnList[i].value()
            
            # o adımdaki öncelikli müşterilerin thread ini tutacak bir list tanımlanır
            l = []
            # o adımdaki öncelikli müşteri sayısı kadar döngü döner
            for _ in range(value1):
                # her müşteri için thread açılır
                t = threading.Thread(target=musteri, args=())
                l.append(t)
            # tüm öncelikli müşterileri tutan list e adımdaki liste eklenir
            oncelikliQueue.append(l)
            
            # adımdaki normal müşterileri tutan list tanımlanır
            l = []
            # adımdaki normal müşteri sayısı kadar döngü döner
            for _ in range(value2):
                # her müşteri için thread oluşturulur
                t = threading.Thread(target=musteri, args=())
                l.append(t)
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
        oncelikliQueue = list(filter(lambda x: x != [], normalQueue))

        
        print("inQueue: ", inQueue)
        print("normalQueue: ", normalQueue)
        print("oncelikliQueue: ", oncelikliQueue)
        
        
        for lbl in self.lblList:
            lbl.close()
        
        for normal in self.normalSpnList:
            normal.close()
        
        for oncelik in self.oncelikSpnList:
            oncelik.close()
        
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
        self.masa1.setPixmap(pixmapDolu)
        self.masa1.setGeometry(50, 50, 40, 40)
        self.masa1.setVisible(True)
        self.masa1.setScaledContents(True)
        
        self.masa2 = QtWidgets.QLabel(self)
        self.masa2.setPixmap(pixmapDolu)
        self.masa2.setGeometry(120, 50, 40, 40)
        self.masa2.setVisible(True)
        self.masa2.setScaledContents(True)
        
        self.masa3 = QtWidgets.QLabel(self)
        self.masa3.setPixmap(pixmapDolu)
        self.masa3.setGeometry(190, 50, 40, 40)
        self.masa3.setVisible(True)
        self.masa3.setScaledContents(True)
        
        self.masa4 = QtWidgets.QLabel(self)
        self.masa4.setPixmap(pixmapDolu)
        self.masa4.setGeometry(50, 120, 40, 40)
        self.masa4.setVisible(True)
        self.masa4.setScaledContents(True)
        
        self.masa5 = QtWidgets.QLabel(self)
        self.masa5.setPixmap(pixmapDolu)
        self.masa5.setGeometry(120, 120, 40, 40)
        self.masa5.setVisible(True)
        self.masa5.setScaledContents(True)
        
        self.masa6 = QtWidgets.QLabel(self)
        self.masa6.setPixmap(pixmapDolu)
        self.masa6.setGeometry(190, 120, 40, 40)
        self.masa6.setVisible(True)
        self.masa6.setScaledContents(True)
        
        
        
        
        
        self.lblGarson = QLabel("Garsonlar", self)
        self.lblGarson.move(320, 10)
        self.lblGarson.setFont(font)
        self.lblGarson.setVisible(True)
          
        self.garson1 = QtWidgets.QLabel(self)
        self.garson1.setPixmap(pixmapBos)
        self.garson1.setGeometry(300, 50, 20, 40)
        self.garson1.setVisible(True)
        self.garson1.setScaledContents(True)
        
        self.garson2 = QtWidgets.QLabel(self)
        self.garson2.setPixmap(pixmapBos)
        self.garson2.setGeometry(350, 50, 20, 40)
        self.garson2.setVisible(True)
        self.garson2.setScaledContents(True)
        
        self.garson3 = QtWidgets.QLabel(self)
        self.garson3.setPixmap(pixmapBos)
        self.garson3.setGeometry(400, 50, 20, 40)
        self.garson3.setVisible(True)
        self.garson3.setScaledContents(True)
        
        
        
        
        self.lblAsci = QLabel("Aşçılar", self)
        self.lblAsci.move(510, 10)
        self.lblAsci.setFont(font)
        self.lblAsci.setVisible(True)
        
        
        self.asci1 = QtWidgets.QLabel(self)
        self.asci1.setPixmap(pixmapBos)
        self.asci1.setGeometry(500, 50, 20, 40)
        self.asci1.setVisible(True)
        self.asci1.setScaledContents(True)
        
        self.asci2 = QtWidgets.QLabel(self)
        self.asci2.setPixmap(pixmapBos)
        self.asci2.setGeometry(550, 50, 20, 40)
        self.asci2.setVisible(True)
        self.asci2.setScaledContents(True)
        
    
    
        self.lblKasa = QLabel("Kasa", self)
        self.lblKasa.move(660, 10)
        self.lblKasa.setFont(font)
        self.lblKasa.setVisible(True)
        
        self.kasa = QtWidgets.QLabel(self)
        self.kasa.setPixmap(pixmapBos)
        self.kasa.setGeometry(650, 50, 60, 60)
        self.kasa.setVisible(True)
        self.kasa.setScaledContents(True)
        
        self.setFixedSize(1280, 720)
        self.backgroundLabel.setGeometry(0, 0, self.width(), self.height())
    
    

class Prb2Panel(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Problem 2")
        self.move(220, 80)
        self.setFixedSize(700, 500)
        self.initUI()

    def initUI(self):
        pass

 
def musteri():
    pass

        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    loginPanel = LoginPanel()

    loginPanel.show()

    sys.exit(app.exec_())