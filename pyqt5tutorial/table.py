import sys
import test
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor
from PyQt5.QtCore import *

class specify_RowAndColumn(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Making table'
        self.left = 400
        self.top = 300
        self.width =300
        self.height = 200
        self.initUI()
    def initUI(self):
        self.setWindowTitle(self.title)
        self.layout = QHBoxLayout()
        self.table_row=QLineEdit()
        self.table_row.setPlaceholderText('rowCount')
        self.table_column = QLineEdit()
        self.table_column.setPlaceholderText('columnCount')
        self.sendbtn = QPushButton("Send",self)
        self.layout.addWidget(self.table_row)
        self.layout.addWidget(self.table_column)
        self.layout.addWidget(self.sendbtn)
        self.setLayout(self.layout)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()

class App(QWidget):
    def __init__(self,r,c):
        super().__init__()
        self.title = 'Statistics Test'
        self.left = 100
        self.top = 100
        self.width = 0
        self.height = 200
        self.initUI(r,c)

    def initUI(self,r,c):
        self.setWindowTitle(self.title)
        self.tableWidget = QTableWidget()
        self.createTable(r,c)#tablewidget create

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)#add tableWidget
        #print(self.tableWidget.width())
        self.groupBox= QGroupBox()
        self.layout2 = QVBoxLayout()

        self.layout3=QVBoxLayout()
        self.textLabel = QLabel("1. Test type", self)
        self.layout2.addWidget(self.textLabel)

        self.vcombo = QComboBox()
        self.vcombo.addItem("CHOICE")
        self.vcombo.addItem("Pearson’s chi-squared test")
        self.vcombo.addItem("Likelihood ratio(LR) G-test")
        self.vcombo.addItem("Fisher’s exact test")
        self.vcombo.addItem("Residuals")
        self.vcombo.addItem("CMH test")
        self.vcombo.addItem("직접입력")
        self.layout2.addWidget(self.vcombo)

        self.textLabel2 = QLabel("2. Alpha", self)
        self.layout2.addWidget(self.textLabel2)

        self.combo = QComboBox()
        self.combo.addItem("0.1")
        self.combo.addItem("0.05")
        self.combo.addItem("0.01")
        self.combo.addItem("직접입력")
        self.combo.currentIndexChanged.connect(self.combo_on_select)
        self.layout2.addWidget(self.combo)

        self.lineEdit = QLineEdit("", self)
        self.layout2.addWidget(self.lineEdit)
        self.lineEdit.hide()

        self.textLabel3 = QLabel("3. Alternative(default=equal)", self)
        self.layout2.addWidget(self.textLabel3)

        self.gl_combo = QComboBox()
        self.gl_combo.addItem("Greater")
        self.gl_combo.addItem("Less")
        self.layout2.addWidget(self.gl_combo)
        self.gl_combo.hide()

        self.vcombo.currentIndexChanged.connect(self.vcombo_on_select)

        self.textLabel4 = QLabel("4. Comparing Proportions", self)
        self.layout2.addWidget(self.textLabel4)

        self.cp_combo = QComboBox()
        self.cp_combo.addItem("CHOICE")
        self.cp_combo.addItem("Difference in proportions(D)")
        self.cp_combo.addItem("Relative Risk (RR)")
        self.cp_combo.addItem("Odd Ratio (OR)")
        self.layout2.addWidget(self.cp_combo)

        self.layout4=QHBoxLayout()
        self.showResiduals= QCheckBox("Show Residuals")
        self.showResiduals.stateChanged.connect(lambda: self.btnstate(self.showResiduals))
        self.layout4.addWidget(self.showResiduals)

        self.Q_button=QPushButton("?",self)
        self.Q_button.clicked.connect(self.Q_button_on_click)
        self.layout4.addWidget(self.Q_button)
        self.layout2.addLayout(self.layout4)

        self.groupBox.setLayout(self.layout2)
        self.layout3.addWidget(self.groupBox)

        self.button = QPushButton('show result', self)
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
        #print(self.textLabel.width())
        self.width=self.tablewidth+self.textLabel.width()
        #print(self.tableWidget.height())
        if(self.height<self.tableheight):
           self.height=self.tableheight
        #print(self.height)


        self.setGeometry(self.left, self.top, self.width, self.height)
        # Add box layout, add table to box layout and add box layout to widget

        self.show()

    def btnstate(self, b):
        allRows = self.tableWidget.rowCount()
        allColumns = self.tableWidget.columnCount()
        matrix = [[0 for col in range(allColumns)] for row in range(allRows)]
        print(allRows)
        print(allColumns)
        if b.text() == "Show Residuals":
            if b.isChecked() == True:
                alpha=self.combo.currentText()
                for i in range(allRows):
                    for j in range(allColumns):
                        # print(type(self.tableWidget.item(i, j).text()))
                        print(self.tableWidget.item(i, j).text())
                        matrix[i][j] = int(self.tableWidget.item(i, j).text())
                Rmatrix,pm_matrix = test.Residuals(matrix)
                for i in range(self.tableWidget.rowCount()):
                    for j in range(self.tableWidget.columnCount()):
                        if pm_matrix[i][j]!=0:
                            self.tableWidget.setItem(i, j, QTableWidgetItem(str(matrix[i][j]) +"\n(" + str(Rmatrix[i][j]) + ")\n"+pm_matrix[i][j]))
                        else:
                            self.tableWidget.setItem(i, j, QTableWidgetItem(str(matrix[i][j]) + "\n(" + str(Rmatrix[i][j]) + ")"))
                            # self.tableWidget.setRowHeight(self,)
            else:

                for i in range(allRows):
                    for j in range(allColumns):
                        # print(type(self.tableWidget.item(i, j).text()))
                        print(self.tableWidget.item(i, j).text())
                        matrix[i][j] = int(self.tableWidget.item(i, j).text().split('(')[0])
                for i in range(self.tableWidget.rowCount()):
                    for j in range(self.tableWidget.columnCount()):
                        self.tableWidget.setItem(i, j, QTableWidgetItem(str(matrix[i][j])))

                        # self.tableWidget.setRowHeight(self,)

            self.tableWidget.resizeRowsToContents()

    @pyqtSlot()
    def Q_button_on_click(self):
        QMessageBox.about(self, "Title", "Note : \n + Represents a strong evidence of lack of fit, \n "
                                         "i.e. subjects in the ith row are more likely to be in the jth column\n"
                                         " - also represents a strong evidence of lack of fit, \n"
                                         "i.e. subjects in the ith row are less likely to be in the jth column")
    @pyqtSlot()
    def vcombo_on_select(self):
        if self.vcombo.currentIndex() == 4:
            self.gl_combo.show()
        else:
            self.gl_combo.hide()

    @pyqtSlot()
    def combo_on_select(self):
        if self.combo.currentIndex() == 3:
            self.lineEdit.show()
        else:
            self.lineEdit.hide()

    def createTable(self,r,c):
       # Create table
        self.tableWidget.setRowCount(int(r))
        self.tableWidget.setColumnCount(int(c))
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
                #print(type(self.tableWidget.item(i, j).text()))
                #print(self.tableWidget.item(i, j).text())
                matrix[i][j] = int(self.tableWidget.item(i, j).text())

        np_matrix=np.array(matrix)
        print("Min : " + str(np.min(np_matrix)))
        # Message=self.tableWidget.item(0,1).text()
        if (self.vcombo.currentIndex()==1):

            if np.min(np_matrix)==0.0:
                for i in range(allRows):
                    for j in range(allColumns):
                        matrix[i][j]+=0.5
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
        elif (self.cp_combo.currentIndex()==1):
            if self.lineEdit.text() is not "":
                print(type(self.lineEdit.text()))
                print(self.lineEdit.text())
            else:
                alpha = float(self.combo.currentText())
            print(alpha)
            pi1,pi2,plus,minus,text=test.Cal_D_value(matrix,alpha)
            Message = "2-sample test for equality of proportions" + "\n" + \
                      "D : " + str(round(pi1,4))+"-"+str(round(pi2,4))+"="+str(round(pi1-pi2),4)+ "\n" \
                    "100 *(1-"+str(alpha)+")% confidence interval for D :"+"\n"\
                    "("+str(round(minus,4))+","+str(round(plus,4))+")"+"\n" +\
                    text
        elif (self.cp_combo.currentIndex()==2):
            if self.lineEdit.text() is not "":
                print(type(self.lineEdit.text()))
                print(self.lineEdit.text())
            else:
                alpha = float(self.combo.currentText())
            RR,logminus,logplus,minus,plus=test.Cal_RR_value(matrix,alpha)
            Message = "Relative risk(RR) : " +str(round(RR,4)) +"\n" + \
                      "100 *(1-" + str(alpha) + ")% confidence interval for log RR :\n" \
                    "(" + str(round(logminus, 4)) + "," + str(round(logplus, 4)) + ")" + "\n" + \
                    "100 *(1-"+str(alpha)+")% confidence interval for RR :"+"\n"\
                    "("+str(round(minus,4))+","+str(round(plus,4))+")"+"\n" +\
                    "Subjects in the first row are "+str(RR)+" times higher to have success than those in the second row."
        elif (self.cp_combo.currentIndex()==3):
            if self.lineEdit.text() is not "":
                print(type(self.lineEdit.text()))
                print(self.lineEdit.text())
            else:
                alpha = float(self.combo.currentText())
            OR,logminus,logplus,minus,plus=test.Cal_OR_value(matrix,alpha)
            print(round(OR,4))
            Message = "Odds ratio(OR) : " +str(round(OR),4) +"\n" + \
                      "100 *(1-" + str(alpha) + ")% confidence interval for log OR :\n" \
                    "(" + str(round(logminus, 4)) + "," + str(round(logplus, 4)) + ")" + "\n" + \
                    "100 *(1-"+str(alpha)+")% confidence interval for OR :"+"\n"\
                    "("+str(round(minus,4))+","+str(round(plus,4))+")"+"\n" +\
                    "The odds for success is "+str(round(OR, 4))+" times higher in the first row than the second row."
        elif (self.vcombo.currentIndex() == 3):
            N11,greater,less = test.greater_less(matrix)
            alpha=float(self.combo.currentText())

            Message = "Test type : " + self.vcombo.currentText() + "\n" \
                    "P(n11) " + str(round(N11,4))+"\n"\
                    "alpha : " + str(alpha) + "\n"
            if greater > alpha or less > alpha:
                Message += "there is no correlation"
            elif greater < alpha:
                Message += "there is positive correlation"
            elif less < alpha:
                Message += "there is negative correlation"

        elif(self.vcombo.currentIndex()==4):
            Message="check your table"
            Rmatrix=test.Residuals(matrix)
            for i in range(self.tableWidget.rowCount()):
                for j in range(self.tableWidget.columnCount()):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(matrix[i][j])+"\n("+str(Rmatrix[i][j])+")"))
                    #self.tableWidget.setRowHeight(self,)
            self.tableWidget.resizeRowsToContents()
        elif(self.vcombo.currentIndex()==5):

            if self.lineEdit.text() is not "":
                print(type(self.lineEdit.text()))
                print(self.lineEdit.text())
            else:
                alpha = float(self.combo.currentText())
            sqrtM, rho,alpha= test.cmh_test(matrix, alpha)
            if alpha>sqrtM:
                print(alpha,sqrtM)
                print(">")
                Message = "CMH statistic M : " + str(round(sqrtM**2,4)) + "\n" \
                        "(sqrt M : " + str(round(sqrtM,4)) + ")\n" \
                        "(rho.hat : " + str(round(rho, 4)) + ")\n" \
                        "alpha : " +self.combo.currentText() + "\n"+\
                          "X and Y are not correlated.\n"
            elif alpha<sqrtM:
                print(alpha, sqrtM)
                print("<")
                Message = "CMH statistic M : " + str(round(sqrtM**2,4)) + "\n" + \
                          "(sqrt M : " + str(sqrtM) + ")\n" \
                        "(rho.hat " + str(round(rho, 4)) + ")\n" \
                        "alpha : " + self.combo.currentText() + "\n"
                if rho<0:
                    Message+="X and Y have a negative association"
                elif rho>0:
                    Message+="X and Y have a positive association"

        QMessageBox.about(self,"Title", Message)

    @pyqtSlot()
    def make_on_click(self):
        return True

class Controller:
    def __init__(self):
        pass
    def Show_FirstWindow(self):
        self.ui=specify_RowAndColumn()
        self.ui.sendbtn.clicked.connect(self.Show_SecondWindow)
    def Show_SecondWindow(self):
        row=self.ui.table_row.text()
        column=self.ui.table_column.text()
        self.ui2=App(row,column)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    Controller=Controller()
    Controller.Show_FirstWindow()

    sys.exit(app.exec_())  
