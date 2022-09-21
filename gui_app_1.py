import sys
from PyQt5.QtWidgets import QFormLayout, QLabel, QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget,QVBoxLayout,QHBoxLayout,QComboBox,QLineEdit,QAbstractButton
from PyQt5.QtGui import QIcon,QKeyEvent, QRegExpValidator,QColor,QPainter,QPen,QRadialGradient,QFont
from PyQt5.QtCore import pyqtSlot, QRegExp,Qt,QPointF
from xc9283_84 import XC9283_84

class Worker(QObject):
    finished = pyqtSignal()
    # progress = pyqtsignal(int)

    def execute_clicked(self):
        print("Current index:",self.dropdown1.currentIndex())
        if (self.dropdown1.currentIndex() == 0):
            self.cot_board.TME()
            self.onpressbutton()
        elif (self.dropdown1.currentIndex() == 1):
            # name, done1 = QInputDialog.getText(self, 'Input Dialog', 'Enter your name:')
            data = self.reg_data["line_edit"].text()
            assert data,"invalid data input"
            reg_data = int(data,0)
            reg_addr = int(self.reg_addr["line_edit"].text(),0)
            # print(self.reg_addr["line_edit"].text())
            print(reg_addr, reg_data)
            # print(ord(self.reg_addr["line_edit"].text()))
            self.cot_board.reg_write(reg_addr,reg_data)
        elif(self.dropdown1.currentIndex() == 2):
            address = int(self.reg_addr["line_edit"].text(),0)
            # return_data = self.cot_board.reg_read(address)
            self.read_data["line_edit"].setText(self.cot_board.reg_read(address).hex())
        elif (self.dropdown1.currentIndex() == 3):
            self.onpressbutton()
        self.finished.emit()

class ValueInput(QLineEdit):
    def __init__(self, max_val, parent=None):
        QLineEdit.__init__(self)

        regexp = QRegExp(r'[0-9a-fA-Fx]+')
        self.validator = QRegExpValidator(regexp)
        self.max_val = max_val
        self.setStyleSheet('color:blue; width:50px')

    def keyPressEvent(self, a0: QKeyEvent):
        state = self.validator.validate(a0.text(), 0)

        if state[1] == 'x' or state[1] in ('\x08'):
            return super().keyPressEvent(a0)

        if state[0] == QRegExpValidator.Acceptable and int(self.text()+state[1], 0) <= self.max_val:
            return super().keyPressEvent(a0)

##create an LED indicator
class LedIndicator(QAbstractButton):
    scaledSize = 1000.0

    def __init__(self, parent=None):
        QAbstractButton.__init__(self, parent)

        self.setMinimumSize(24, 24)
        self.setCheckable(True)

        # Green
        self.on_color_1 = QColor(0, 255, 0)
        self.on_color_2 = QColor(0, 192, 0)
        self.off_color_1 = QColor(0, 28, 0)
        self.off_color_2 = QColor(0, 128, 0)

    def resizeEvent(self, QResizeEvent):
        self.update()

    def paintEvent(self, QPaintEvent):
        realSize = min(self.width(), self.height())

        painter = QPainter(self)
        pen = QPen(Qt.black)
        pen.setWidth(1)

        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)
        painter.scale(realSize / self.scaledSize, realSize / self.scaledSize)
        painter.setPen(pen)
        if self.isChecked():
            gradient = QRadialGradient(QPointF(-500, -500), 1500, QPointF(-500, -500))
            gradient.setColorAt(0, self.on_color_1)
            gradient.setColorAt(1, self.on_color_2)
        else:
            gradient = QRadialGradient(QPointF(500, 500), 1500, QPointF(500, 500))
            gradient.setColorAt(0, self.off_color_1)
            gradient.setColorAt(1, self.off_color_2)
        painter.setBrush(gradient)
        painter.drawEllipse(QPointF(0, 0), 400, 400)
        painter.setFont(QFont(None,500))
        painter.drawText(QPointF(500, 300), "TME")

class App(QMainWindow):     

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 tabs - pythonspot.com'
        self.left = 0
        self.top = 0
        self.width = 600
        self.height = 400
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)
        self.show()
    
class MyTableWidget(QWidget):
    
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QHBoxLayout(self)
        
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tabs.resize(300,200)
        
        # Add tabs
        self.tabs.addTab(self.tab1,"XC9283-84 Supply")
        self.tabs.addTab(self.tab2,"Blocks")
        self.tabs.addTab(self.tab3,"Register Interface")
        
        # Create first tab
        self.tab1.layout = QVBoxLayout(self)
        # self.layout1 = QHBoxLayout(self)
        self.pushButton1 = QPushButton("PyQt5 button")
        # self.pushButton2 = QPushButton("PyQt5_1 button")
        self.pushButton1.clicked.connect(self.on_click)
        self.tab1.layout.addWidget(self.pushButton1)
        # self.layout.addWidget(self.pushButton1)
        self.tab1.setLayout(self.tab1.layout)
        
        #Create third tab
        self.tab3.layout = QVBoxLayout(self)
        self.led = LedIndicator(self)
        self.led.setDisabled(True)      #make led non clickable
        self.dropdown1 = QComboBox()
        self.pushButton2 = QPushButton("Execute")
        self.dropdown1.addItems(["Test Mode Entry","REG Write","REG Read","Test Mode Exit"])
        self.dropdown1.currentIndexChanged.connect(self.data)

        self.pushButton2.clicked.connect(self.execute_clicked)
        self.tab3.layout.addWidget(self.dropdown1)
        self.tab3.layout.addWidget(self.pushButton2)
        self.tab3.layout.addWidget(self.led)
        self.tab3.setLayout(self.tab3.layout)

        #create reg address/data input box
        self.reg_addr = {"label" : QLabel("Reg"), "line_edit" : ValueInput(66)}
        self.reg_data = {"label" : QLabel("Data"), "line_edit" : ValueInput(255)}
        self.read_data = {"label" : QLabel("Read Data"), "line_edit" : QLineEdit()}
        layout1= QFormLayout()
        layout1.addRow(self.reg_addr["label"], self.reg_addr["line_edit"])
        layout1.addRow(self.reg_data["label"], self.reg_data["line_edit"])
        layout1.addRow(self.read_data["label"], self.read_data["line_edit"])
        self.tab3.layout.addLayout(layout1)
        self.reg_data["label"].hide()
        self.reg_data["line_edit"].hide()
        self.reg_addr["label"].hide()
        self.reg_addr["line_edit"].hide()
        self.read_data["label"].hide()
        self.read_data["line_edit"].hide()

        # Add tabs to widget
        self.layout.addWidget(self.tabs)

        # self.setLayout(self.layout)

        self.cot_board = XC9283_84()
        
    def on_click(self):         ##slot 
        print("Clicked")
        self.cot_board.set_led('1')
   
    def data(self):
        if (self.dropdown1.currentIndex() == 0):
            self.reg_data["label"].hide()
            self.reg_data["line_edit"].hide()
            self.reg_addr["label"].hide()
            self.reg_addr["line_edit"].hide()
            self.read_data["label"].hide()
            self.read_data["line_edit"].hide()
            
        elif (self.dropdown1.currentIndex() == 1):
            self.reg_data["label"].show()
            self.reg_data["line_edit"].show()
            self.reg_addr["label"].show()
            self.reg_addr["line_edit"].show()
            self.read_data["label"].hide()
            self.read_data["line_edit"].hide()

        elif(self.dropdown1.currentIndex() == 2):
            self.reg_data["label"].hide()
            self.reg_data["line_edit"].hide()
            self.reg_addr["label"].show()
            self.reg_addr["line_edit"].show()
            self.read_data["label"].show()
            self.read_data["line_edit"].show()

        elif (self.dropdown1.currentIndex() == 3):
            self.reg_data["label"].hide()
            self.reg_data["line_edit"].hide()
            self.reg_addr["label"].hide()
            self.reg_addr["line_edit"].hide()
            self.read_data["label"].hide()
            self.read_data["line_edit"].hide()
            
    def onpressbutton(self):
        self.led.setChecked(not self.led.isChecked())
        
    def execute_clicked(self):
        print("Current index:",self.dropdown1.currentIndex())
        if (self.dropdown1.currentIndex() == 0):
            self.cot_board.TME()
            self.onpressbutton()
        elif (self.dropdown1.currentIndex() == 1):
            # name, done1 = QInputDialog.getText(self, 'Input Dialog', 'Enter your name:')
            data = self.reg_data["line_edit"].text()
            assert data,"invalid data input"
            reg_data = int(data,0)
            reg_addr = int(self.reg_addr["line_edit"].text(),0)
            # print(self.reg_addr["line_edit"].text())
            print(reg_addr, reg_data)
            # print(ord(self.reg_addr["line_edit"].text()))
            self.cot_board.reg_write(reg_addr,reg_data)
        elif(self.dropdown1.currentIndex() == 2):
            address = int(self.reg_addr["line_edit"].text(),0)
            return_data = self.cot_board.reg_read(address)
            self.read_data["line_edit"].setText(return_data.hex())
        elif (self.dropdown1.currentIndex() == 3):
            self.onpressbutton()


    


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())##event loop called