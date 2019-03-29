import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton
#from PyQt5.QtCore import pyqtSlot



class MyApp(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.qle1 = QLineEdit(self)
        self.qle1.move(20, 20)
        self.qle1.resize(560, 80)

        self.btn1 = QPushButton('추출', self)
        self.btn1.move(20, 120)
        self.btn1.resize(560, 60)
        self.btn1.clicked.connect(self.btn1_clicked)

        self.qle2 = QLineEdit(self)
        self.qle2.move(20, 200)
        self.qle2.resize(560, 80)


        self.setWindowTitle('숫자 추출')
        self.setGeometry(1000, 300, 600, 300)
        self.show()

'''
(그냥 특수문자만 제거)
(거꾸로 쓰기)
(한글을 숫자로)
2(#*5^$2@(1@&6@&1^1(숫자를 모두 더하기한 값은?)
내@가%@조*($*선@%@의#($)땡^^초#!다(초성만 적으세요)
1@&2@*1@#&1@&(@&8@&8@*11(숫자를 한글로 적으세요)
1@&구@*이^&7@(6@)육@)삼@)3#오@^4@(7!!5!!1(숫자는 한글로 , 한글은 숫자로 적으세요)
'''


    def btn1_clicked(self):
        print('button clicked!!')
        text = self.qle1.text()
        answer = ''
        for c in text:
            if c == '@' or c=='#' or c=='*' or c=='%' or c=='(' or c==')' or c=='!' or c=='$' or c=='^' or c=='&' or c==' ' :
                continue
            answer+=c
        self.qle2.setText(answer)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
    