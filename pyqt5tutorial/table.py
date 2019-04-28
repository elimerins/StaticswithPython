import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import *
import test
import numpy as np

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 table - pythonspot.com'
        self.left = 0
        self.top = 0
        self.width = 0
        self.height = 200
        self.initUI()

        
    def initUI(self):
        self.setWindowTitle(self.title)

        self.createTable()#tablewidget create

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)#add tableWidget
        print(self.tableWidget.width())
        self.groupBox= QGroupBox()
        self.layout2 = QVBoxLayout()

        self.layout3=QVBoxLayout()
        self.textLabel = QLabel("1. Test type", self)
        self.layout2.addWidget(self.textLabel)

        self.vcombo = QComboBox()
        self.vcombo.addItem("Pearson’s chi-squared test(without correction)")
        self.vcombo.addItem("Pearson’s chi-squared test(with correction)")
        self.vcombo.addItem("Likelihood ratio(LR) G-test")
        self.vcombo.addItem("Fisher’s exact test")
        self.vcombo.addItem("직접입력")
        self.layout2.addWidget(self.vcombo)

        self.textLabel2 = QLabel("2. Alpha", self)
        self.layout2.addWidget(self.textLabel2)

        self.combo = QComboBox()
        self.combo.addItem("0.1")
        self.combo.addItem("0.05")
        self.combo.addItem("0.01")
        self.combo.addItem("직접입력")
        self.layout2.addWidget(self.combo)

        self.lineEdit = QLineEdit("", self)
        self.layout2.addWidget(self.lineEdit)
        self.groupBox.setLayout(self.layout2)
        self.layout3.addWidget(self.groupBox)

        self.button = QPushButton('show value', self)
        self.button.clicked.connect(self.show_value_button)
        self.layout3.addWidget(self.button)

        self.button2= QPushButton('make array',self)
        self.button2.clicked.connect(self.make_on_click)
        self.layout3.addWidget(self.button2)

        self.p_layout = QHBoxLayout()
        self.p_layout.addLayout(self.layout)
        self.p_layout.addLayout(self.layout3)
        self.setLayout(self.p_layout)
        # Show widget
        print(self.textLabel.width())
        self.width=self.tablewidth+self.textLabel.width()
        print(self.tableWidget.height())
        if(self.height<self.tableheight):
           self.height=self.tableheight
        print(self.height)


        self.setGeometry(self.left, self.top, self.width, self.height)
        # Add box layout, add table to box layout and add box layout to widget

        self.show()

    def createTable(self):
       # Create table
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(2)
        self.tableWidget.setColumnCount(3)
        Rowcount=self.tableWidget.rowCount()
        Colcount = self.tableWidget.columnCount()
        print(self.tableWidget.height())
        print(self.tableWidget.width())
        self.tablewidth=self.tableWidget.width()+100*Colcount
        self.tableheight =40*Rowcount
        self.tableWidget.resize(self.tablewidth,self.tableheight)
        for i in range(self.tableWidget.rowCount()):
            for j in range(self.tableWidget.columnCount()):
                self.tableWidget.setItem(i,j, QTableWidgetItem("0"))
        self.tableWidget.move(0,0)

        print(self.tableWidget.item(0,1).text())

        # table selection change
        self.tableWidget.doubleClicked.connect(self.on_click)



    @pyqtSlot()
    def on_click(self):
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())

    @pyqtSlot()
    def show_value_button(self):

        allRows = self.tableWidget.rowCount()
        allColumns = self.tableWidget.columnCount()
        matrix = [[0 for col in range(allColumns)] for row in range(allRows)]
        print(allRows)
        print(allColumns)
        for i in range(allRows):
            for j in range(allColumns):
                print(type(self.tableWidget.item(i, j).text()))
                print(self.tableWidget.item(i, j).text())
                matrix[i][j] = int(self.tableWidget.item(i, j).text())

        np_matrix=np.array(matrix)
        print("Min : " + str(np.min(np_matrix)))
        # Message=self.tableWidget.item(0,1).text()
        if (self.vcombo.currentIndex()==0):
            p_value = test.Cal_x_value(matrix)
            alpha = float(self.combo.currentText())

            Message="Test type : "+self.vcombo.currentText()+"\n"+\
                    "p-value : "+str(p_value)+"\n"+\
                    "alpha : " +str(alpha)+"\n"
            if (p_value < alpha):
                Message +="X and Y are not independent"
            elif (p_value > alpha):
                Message += "X and Y are independent"
            if np.min(np_matrix)<5:
                Message+="\n\n"+\
                        "Note : The test might not be  appropriate" \
                        "due to the small expected frequency."
        elif (self.vcombo.currentIndex()==2):
            p_value = test.Cal_g_value(matrix)
            alpha = float(self.combo.currentText())

            Message="Test type : "+self.vcombo.currentText()+"\n"+\
                    "p-value : "+str(p_value)+"\n"+\
                    "alpha : " +str(alpha)+"\n"
            if (p_value < alpha):
                Message +="X and Y are not independent"
            elif (p_value > alpha):
                Message += "X and Y are independent"
            if np.min(np_matrix)<5:
                Message+="\n\n"+\
                        "Note : The test might not be  appropriate" \
                        "due to the small expected frequency."
        QMessageBox.about(self,"Title", Message)

    @pyqtSlot()
    def make_on_click(self):
        return True



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()

    sys.exit(app.exec_())  
