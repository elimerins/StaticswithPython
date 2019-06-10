import sys
import test
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class specify_RowAndColumn(QWidget):#첫번째창
    def __init__(self):
        super().__init__()
        self.title = 'Make table'
        self.left = 400
        self.top = 300
        self.width =300
        self.height = 200
        self.initUI()#기
    def initUI(self):
        self.setWindowTitle(self.title)
        self.layout = QHBoxLayout() #horizon box
        self.table_row=QLineEdit() #row
        self.table_row.setPlaceholderText('rowCount')
        self.table_column = QLineEdit() #col
        self.table_column.setPlaceholderText('columnCount')
        self.sendbtn = QPushButton("Run",self)
        self.layout.addWidget(self.table_row)#widget을 layout에 add
        self.layout.addWidget(self.table_column)
        self.layout.addWidget(self.sendbtn)
        self.setLayout(self.layout)#layout을 최종세팅
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()

class App(QWidget):
    def __init__(self,r,c):
        super().__init__()
        self.title = 'Crosstab Analysis'
        self.left = 100
        self.top = 100
        self.width = 0
        self.height = 200
        self.initUI(r,c)

    def initUI(self,r,c):
        self.setWindowTitle(self.title)
        self.tableWidget = QTableWidget()#table widget
        self.createTable(r,c)#tablewidget create

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)#add tableWidget

        self.groupBox= QGroupBox()
        self.layout2 = QVBoxLayout()#vertical layout

        self.layout3=QVBoxLayout()
        self.textLabel = QLabel("1. Test type", self)#textlabel
        self.layout2.addWidget(self.textLabel)

        self.vcombo = QComboBox()#combo box
        self.vcombo.addItem("CHOICE")#콤보 박스에 아이템 add
        self.vcombo.addItem("Pearson’s chi-squared test")
        self.vcombo.addItem("Likelihood ratio(LR) G-test")
        self.vcombo.addItem("Fisher’s exact test")
        self.vcombo.addItem("CMH test")
        self.vcombo.addItem("직접입력")
        self.layout2.addWidget(self.vcombo)

        self.textLabel2 = QLabel("2. Alpha", self)
        self.layout2.addWidget(self.textLabel2)

        self.combo = QComboBox()#combo box
        self.combo.addItem("0.05")#콤보 박스에 아이템 add
        self.combo.addItem("0.1")
        self.combo.addItem("0.01")
        self.combo.addItem("직접입력")

        self.combo.currentIndexChanged.connect(self.combo_on_select)
        #combo box index가 바뀔 때마다 combo_on_select와 연결
        self.layout2.addWidget(self.combo)

        self.lineEdit = QLineEdit("", self)
        self.layout2.addWidget(self.lineEdit)
        self.lineEdit.hide()#기본적으로 숨겨져있는 lineEdit라는 이름의 QLineEdit

        self.textLabel3 = QLabel("3. Alternative", self)
        self.layout2.addWidget(self.textLabel3)

        self.gl_combo = QComboBox()#gl_combo box
        self.gl_combo.addItem("Equal")#add item
        self.gl_combo.addItem("Greater")
        self.gl_combo.addItem("Less")
        self.layout2.addWidget(self.gl_combo)#layout2에 widget add
        self.gl_combo.hide()#기본적으로 Hide

        self.vcombo.currentIndexChanged.connect(self.vcombo_on_select)
        #vcombox의 선택된 index가 바뀔때마다 vcombo_on_select를 호출

        self.textLabel4 = QLabel("4. Comparing Proportions", self)
        self.layout2.addWidget(self.textLabel4)

        self.cp_combo = QComboBox()#comparing proportions combo box 만듦.
        self.cp_combo.addItem("CHOICE")#combo box add item
        self.cp_combo.addItem("Difference in proportions(D)")
        self.cp_combo.addItem("Relative Risk (RR)")
        self.cp_combo.addItem("Odds Ratio (OR)")
        self.layout2.addWidget(self.cp_combo)

        self.layout4=QHBoxLayout()#horizon layout layout4 만듦
        self.showResiduals= QCheckBox("Check Residuals")#check box 만듦
        self.showResiduals.stateChanged.connect(lambda: self.btnstate(self.showResiduals))
        #showResidual 이라는 QCheckbox의 상태가 바뀔때마다 btnstate함수와 연결됨
        self.layout4.addWidget(self.showResiduals)

        self.Q_button=QPushButton("?",self)#pushbutton 만듦
        self.Q_button.clicked.connect(self.Q_button_on_click)
        #Q_button은 Q_button_on_click 함수와 연결됨
        self.layout4.addWidget(self.Q_button)
        self.layout2.addLayout(self.layout4)
        #layout2에 layout4를 add

        self.groupBox.setLayout(self.layout2)
        self.layout3.addWidget(self.groupBox)

        self.button = QPushButton('Run', self)
        self.button.clicked.connect(self.show_value_button)
        #button이라는 QPushButton은 show_value_button 함수와 연결
        self.layout3.addWidget(self.button)

        self.p_layout = QHBoxLayout()
        self.p_layout.addLayout(self.layout)
        self.p_layout.addLayout(self.layout3)
        self.setLayout(self.p_layout)#layout2, layout3을 p_layout에 add
        # Show widget

        self.width=self.tablewidth+self.textLabel.width()

        if(self.height<self.tableheight):
           self.height=self.tableheight

        self.setGeometry(self.left, self.top, self.width, self.height)
        # Add box layout, add table to box layout and add box layout to widget

        self.show()

    def btnstate(self, b):
        allRows = self.tableWidget.rowCount()#tablewidget의 rowCount
        allColumns = self.tableWidget.columnCount()#tablewidget의 colCount
        matrix = [[0 for col in range(allColumns)] for row in range(allRows)]
        #allColumns 개수의 열,allRows의 행을 가진 matrix 생성, matrix내 모든 값은 0
        print(allRows)
        print(allColumns)

        if b.isChecked() == True:#체크되어있다면
            alpha=self.combo.currentText()
            for i in range(allRows):
                for j in range(allColumns):
                    # print(type(self.tableWidget.item(i, j).text()))
                    #print(self.tableWidget.item(i, j).text())
                    matrix[i][j] = int(self.tableWidget.item(i, j).text())
                    #table widget에 있는 각 value를 matrix에 삽입
            Rmatrix,pm_matrix = test.Residuals(matrix)
            #matrix를 Residuals함수의 인자로 넘김

            #return 값으로, 함수에서 계산된 Integer값들이 들어있는 Rmatrix와 integer값에 맞는 +,-값이 있는 pm_matrix받음
            for i in range(self.tableWidget.rowCount()):
                for j in range(self.tableWidget.columnCount()):
                    if pm_matrix[i][j]!=0:
                        self.tableWidget.setItem(i, j, QTableWidgetItem(str(matrix[i][j]) +"\n(" + str(Rmatrix[i][j]) + ")\n"+pm_matrix[i][j]))
                    else:
                        self.tableWidget.setItem(i, j, QTableWidgetItem(str(matrix[i][j]) + "\n(" + str(Rmatrix[i][j]) + ")"))
                        # self.tableWidget.setRowHeight(self,)
        else:#체크되어있지 않다면
            for i in range(allRows):
                for j in range(allColumns):
                    # print(type(self.tableWidget.item(i, j).text()))
                    print(self.tableWidget.item(i, j).text())
                    matrix[i][j] = int(self.tableWidget.item(i, j).text().split('(')[0])
                    #현재 tablewidget의 각 value '(' 앞부분만 matrix에 담음
            for i in range(self.tableWidget.rowCount()):
                for j in range(self.tableWidget.columnCount()):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(matrix[i][j])))
                    #matrix의 각 value을 tablewidget 에 set함

                    # self.tableWidget.setRowHeight(self,)

        self.tableWidget.resizeRowsToContents()
        #각 상황에 맞게 tablewidget을 resize함

    @pyqtSlot()
    def Q_button_on_click(self):
        QMessageBox.about(self, "Title", "Note : \n + Represents a strong evidence of lack of fit, \n "
                                         "i.e. subjects in the ith row are more likely to be in the jth column\n"
                                         " - also represents a strong evidence of lack of fit, \n"
                                         "i.e. subjects in the ith row are less likely to be in the jth column")

        #qbutton을 클릭할 때 messagebox
    @pyqtSlot()
    def vcombo_on_select(self):
        if self.vcombo.currentIndex() == 3:
            #fisher's exact text인 경우
            self.gl_combo.show()
        else:
            self.gl_combo.hide()

    @pyqtSlot()
    def combo_on_select(self):
        if self.combo.currentIndex() == 3:
            #'직접입력'의 경우
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
        #tableheight를 40*행의 개수로 맞춤
        self.tableWidget.resize(self.tablewidth,self.tableheight)
        #테이블 위젯의 높이,너비 세팅
        for i in range(self.tableWidget.rowCount()):
            for j in range(self.tableWidget.columnCount()):
                self.tableWidget.setItem(i,j, QTableWidgetItem("0"))
                #table 각 value 0으로 세팅 0,0부터 마지막 까지
        self.tableWidget.move(0,0)

        print(self.tableWidget.item(0,1).text())

        # table selection change
        self.tableWidget.doubleClicked.connect(self.on_click)


    @pyqtSlot()
    def on_click(self):
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())
            #value 클릭할시 행, 열번호, value 출력

    @pyqtSlot()
    def show_value_button(self):
        #run 클릭 시
        if self.showResiduals.isChecked()==True:
            self.showResiduals.toggle()
            #Residual이 체크된경우 체크 풀어주고 계산 시작
        allRows = self.tableWidget.rowCount()
        allColumns = self.tableWidget.columnCount()
        matrix = [[0 for col in range(allColumns)] for row in range(allRows)]
        #matrix arrary에 0 할당 matrix의 행 개수 열 개수와 맞춰서 만듦
        print(allRows)
        print(allColumns)
        for i in range(allRows):
            for j in range(allColumns):
                #print(type(self.tableWidget.item(i, j).text()))
                #print(self.tableWidget.item(i, j).text())
                matrix[i][j] = int(self.tableWidget.item(i, j).text())
                #matrix에 tablewidget의 값을 넣음
        np_matrix=np.array(matrix)
        #np_matrix는 matrix를 numpy를 활용해서 Numpy의 행렬로 만듦

        print("Min : " + str(np.min(np_matrix)))
        #npmatrix의 min값 출력
        # Message=self.tableWidget.item(0,1).text()
        if self.combo.currentIndex()==3:
            if self.lineEdit.text() is not "":
                alpha=float(self.lineEdit.text())
                #alpha를 직접 입력으로 선택한경우 값을 입력할 수 있음 float형으로 변환되어 들어감
            else:
                alpha =0.05
                #직접입력으로 넣었지만 값을 넣지 않은경우 자동으로 0.05
        else:
            alpha=float(self.combo.currentText())
            #직접 입력이 아닌경우 현 combo의 선택된 값이 alpha가 됨

        if self.vcombo.currentIndex()!=0:
            if self.cp_combo.currentIndex()!=0:
                Message="choice Only one : \n Test type or Comparing Proportions"
                #test type과 comparing proportion 둘중하나만 선택할 수 있음
            else:
                if (self.vcombo.currentIndex() == 1):
                #피어슨 테스트인경우
                    if np.min(np_matrix) == 0:
                        for i in range(allRows):
                            for j in range(allColumns):
                                matrix[i][j] = float(matrix[i][j])
                    ksquare, p_value = test.Cal_x_value(matrix)
                    #X^2 값과 p_value를 계산함

                    Message = "Test type : " + self.vcombo.currentText() + "\n" + \
                              "X^2 : " + str(ksquare) + "\n" + \
                              "p-value : " + str(p_value) + "\n" + \
                              "alpha : " + str(alpha) + "\n"
                    print(Message)
                    #p_value에 따라 Message에 들어갈 값 변화
                    if (p_value < alpha):
                        Message += "X and Y are not independent"
                    elif (p_value > alpha):
                        Message += "X and Y are independent"
                    if np.min(np_matrix) < 5:
                        Message += "\n\n" + \
                                   "Note : The test might not be appropriate " \
                                   "due to the small expected frequency."
                elif (self.vcombo.currentIndex() == 2):
                    G, p_value = test.Cal_g_value(matrix)
                    # G^2 값과 p_value를 계산함

                    Message = "Test type : " + self.vcombo.currentText() + "\n" + \
                              "G^2 : " + str(G) + "\n" + \
                              "p-value : " + str(p_value) + "\n" + \
                              "alpha : " + str(alpha) + "\n"

                    # p_value에 따라 Message에 들어갈 값 변화
                    if (p_value < alpha):
                        Message += "X and Y are not independent"
                    elif (p_value > alpha):
                        Message += "X and Y are independent"
                    if np.min(np_matrix) < 5:
                        Message += "\n\n" + \
                                   "Note : The test might not be  appropriate " \
                                   "due to the small expected frequency."

                elif (self.vcombo.currentIndex() == 3):
                    greater, less, p_value = test.greater_less(matrix)
                    #fisher's exact 계산

                    if (self.gl_combo.currentIndex() == 0):
                        #glcombox가 equal인 경우
                        Message = "Test type : " + self.vcombo.currentText() + "\n" \
                                "alternative : true odds ratio is not equal to 1.\n" \
                                "p_value : " + str(round(p_value, 4)) + "\n" \
                                "alpha : " + str(alpha) + "\n"
                        if p_value < alpha:
                            Message += "Reject the null hypothesis. \nTrue odds ratio is not equal to 1."
                        elif p_value > alpha:
                            Message += "Do not reject the null hypothesis. \nX and Y are independent"
                    elif (self.gl_combo.currentIndex() == 1):
                        #glcombox가 greater인 경우

                        Message = "Test type : " + self.vcombo.currentText() + "\n" \
                                "alternative : true odds ratio is greater than 1.\n" \
                                "p_value : " + str(round(greater, 4)) + "\n" \
                                "alpha : " + str(alpha) + "\n"
                        if greater < alpha:
                            Message += "Reject the null hypothesis. \nTrue odds ratio is greater than 1."
                        elif greater > alpha or less > alpha or p_value > alpha:
                            Message += "Do not reject the null hypothesis. \nX and Y are independent"
                    elif (self.gl_combo.currentIndex() == 2):
                        #glcombox가 less인 경우

                        Message = "Test type : " + self.vcombo.currentText() + "\n" \
                               "alternative : true odds ratio is less than 1.\n" \
                                "p_value : " + str(round(less, 4)) + "\n" \
                                "alpha : " + str(alpha) + "\n"
                        if less < alpha:
                            Message += "Reject the null hypothesis. \nTrue odds ratio is less than 1."
                        elif less > alpha:
                            Message += "Do not reject the null hypothesis. \nX and Y are independent"

                elif (self.vcombo.currentIndex() == 4):
                    sqrtM, rho, alpha = test.cmh_test(matrix, alpha)
                    #cmh test에서 계산될 수 있는 값
                    if alpha > sqrtM:
                        #알파가 큰경우
                        print(alpha, sqrtM)
                        print(">")
                        Message = "CMH statistic M : " + str(round(sqrtM ** 2, 4)) + "\n" \
                                    "(sqrt M : " + str(round(sqrtM, 4)) + ")\n" \
                                    "(sample correlation : " + str(round(rho, 4)) + ")\n" \
                                    "alpha : " + self.combo.currentText() + "\n" + \
                                  "X and Y are not correlated.\n"
                    elif alpha < sqrtM:
                        #알파가 작은 경우
                        print(alpha, sqrtM)
                        print("<")
                        Message = "CMH statistic M : " + str(round(sqrtM ** 2, 4)) + "\n" + \
                                  "(sqrt M : " + str(sqrtM) + ")\n" \
                                    "(rho.hat " + str(round(rho, 4)) + ")\n" \
                                    "alpha : " + self.combo.currentText() + "\n"
                        if rho < 0:
                            Message += "X and Y have a negative association"
                        elif rho > 0:
                            Message += "X and Y have a positive association"

        elif self.cp_combo.currentIndex() != 0:
            if self.vcombo.currentIndex() != 0:
                Message = "choice Only one : \n Test type or Comparing Proportions"
            else:
                if (self.cp_combo.currentIndex() == 1):
                    #D_value 측
                    print(alpha)
                    pi1, pi2, plus, minus, text = test.Cal_D_value(matrix, alpha)
                    Message = "2-sample test for equality of proportions" + "\n" + \
                              "D : " + str(round(pi1, 4)) + "-" + str(round(pi2, 4)) + "=" + str(round(pi1 - pi2, 4)) + "\n" \
                                "100 *(1-" + str(alpha) + ")% confidence interval for D :" + "\n" \
                                "(" + str(round(minus, 4)) + "," + str(round(plus, 4)) + ")" + "\n" + \
                              text
                elif (self.cp_combo.currentIndex() == 2):
                    #RR 측정
                    RR, logminus, logplus, minus, plus = test.Cal_RR_value(matrix, alpha)
                    Message = "Relative risk(RR) : " + str(round(RR, 4)) + "\n" + \
                              "100 *(1-" + str(alpha) + ")% confidence interval for log RR :\n" \
                                "(" + str(round(logminus, 4)) + "," + str(round(logplus, 4)) + ")" + "\n" + \
                              "100 *(1-" + str(alpha) + ")% confidence interval for RR :" + "\n" \
                                "(" + str(round(minus, 4)) + "," + str(round(plus, 4)) + ")" + "\n" + \
                              "Subjects in the first row are " + str(RR) + " times higher to have success than those in the second row."
                elif (self.cp_combo.currentIndex() == 3):
                    #OR 측정
                    OR, logminus, logplus, minus, plus = test.Cal_OR_value(matrix, alpha)
                    if isinstance(OR, str) == True:
                        Message = OR
                    else:
                        print(round(OR, 4))
                        Message = "Odds ratio(OR) : " + str(round(OR, 4)) + "\n" + \
                                  "100 *(1-" + str(alpha) + ")% confidence interval for log OR :\n" \
                                    "(" + str(round(logminus, 4)) + "," + str(round(logplus, 4)) + ")" + "\n" + \
                                  "100 *(1-" + str(alpha) + ")% confidence interval for OR :" + "\n" \
                                    "(" + str(round(minus, 4)) + "," + str(round(plus, 4)) + ")" + "\n" + \
                                  "The odds for success is " + str(round(OR, 4)) + " times higher in the first row than the second row."


        QMessageBox.about(self,"Title", Message)

class Controller:
    def __init__(self):
        pass
    def Show_FirstWindow(self):
        self.ui=specify_RowAndColumn()
        self.ui.sendbtn.clicked.connect(self.Show_SecondWindow)#send button -> show secondwindow btn과 연
    def Show_SecondWindow(self):
        try:
            row=int(self.ui.table_row.text())#row text value integer로 바꿈
            column=int(self.ui.table_column.text())#col text value integer로 바꿈
            self.ui2 = App(row, column)#App ui에 row,col 값을 넘겨서
        except ValueError:
            Message="row, column data must be Integer."
            QMessageBox.about(self.ui,"Title", Message)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    Controller=Controller()
    Controller.Show_FirstWindow()

    sys.exit(app.exec_())  
