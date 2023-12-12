from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QSpinBox, QPushButton
import sys

adimSayisi = 0

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
        
        self.lblNormal.close()
        self.lblOncelik.close()
        self.pushButton.close()
        
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
        
        
        pixmapBos = QtGui.QPixmap('img/bos-masa.jpg')
        pixmapDolu = QtGui.QPixmap('img/dolu-masa.jpg')
        
        self.masa1 = QtWidgets.QLabel(self)
        self.masa1.setPixmap(pixmapBos)
        self.masa1.setGeometry(50, 50, 40, 40)
        self.masa1.setVisible(True)
        self.masa1.setScaledContents(True)
        
        self.masa2 = QtWidgets.QLabel(self)
        self.masa2.setPixmap(pixmapBos)
        self.masa2.setGeometry(120, 50, 40, 40)
        self.masa2.setVisible(True)
        self.masa2.setScaledContents(True)
        
        self.masa3 = QtWidgets.QLabel(self)
        self.masa3.setPixmap(pixmapBos)
        self.masa3.setGeometry(190, 50, 40, 40)
        self.masa3.setVisible(True)
        self.masa3.setScaledContents(True)
        
        self.masa4 = QtWidgets.QLabel(self)
        self.masa4.setPixmap(pixmapBos)
        self.masa4.setGeometry(50, 120, 40, 40)
        self.masa4.setVisible(True)
        self.masa4.setScaledContents(True)
        
        self.masa5 = QtWidgets.QLabel(self)
        self.masa5.setPixmap(pixmapBos)
        self.masa5.setGeometry(120, 120, 40, 40)
        self.masa5.setVisible(True)
        self.masa5.setScaledContents(True)
        
        self.masa6 = QtWidgets.QLabel(self)
        self.masa6.setPixmap(pixmapBos)
        self.masa6.setGeometry(190, 120, 40, 40)
        self.masa6.setVisible(True)
        self.masa6.setScaledContents(True)
        
        
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

 


        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    loginPanel = LoginPanel()

    loginPanel.show()

    sys.exit(app.exec_())