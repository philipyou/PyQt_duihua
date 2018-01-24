
import math
import random
import string
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import duihua
import duihua1
import duihua2

class Form(QDialog):
    X_MAX = 26
    Y_MAX = 60

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        self.numberFormatDlg = None
        self.format = dict(thousandsseparator=",", decimalmarker=".",
                decimalplaces=2, rednegatives=False)
        self.numbers = {}
        for x in range(self.X_MAX):
            for y in range(self.Y_MAX):
                self.numbers[(x, y)] = (10000 * random.random()) - 5000

        self.table = QTableWidget()
        formatButton1 = QPushButton("Set Number Format... (&Modal)")
        formatButton2 = QPushButton("Set Number Format... (Modele&ss)")
        formatButton3 = QPushButton("Set Number Format... (`&Live')")

        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch()
        buttonLayout.addWidget(formatButton1)
        buttonLayout.addWidget(formatButton2)
        buttonLayout.addWidget(formatButton3)
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addLayout(buttonLayout)
        self.setLayout(layout)

        formatButton1.clicked.connect(self.setNumberFormat1)
        formatButton2.clicked.connect(self.setNumberFormat2)
        formatButton3.clicked.connect(self.setNumberFormat3)

        self.setWindowTitle("Numbers")
        self.refreshTable()

    def refreshTable(self):
        self.table.clear()
        self.table.setColumnCount(self.X_MAX)
        self.table.setRowCount(self.Y_MAX)
        self.table.setHorizontalHeaderLabels(list(string.ascii_uppercase))

        fraction, whole = math.modf(self.numbers[(0,0)])
        whole = "{}".format(int(math.floor(abs(whole))))
        print("%s",)

        for x in range(self.X_MAX):
            for y in range(self.Y_MAX):
                fraction, whole = math.modf(self.numbers[(x,y)])
                sign = "-" if whole < 0 else ""
                whole = "{}".format(int(math.floor(abs(whole))))
                digits = []
                for i , digit in enumerate(reversed(whole)):
                    if i and i % 3 == 0:
                        digits.insert(0,self.format["thousandsseparator"])
                    digits.insert(0,digit)
                if self.format["decimalplaces"]:
                    fraction = "{0:.7f}".format(abs(fraction))
                    fraction = (self.format["decimalmarker"] +
                                fraction[2:self.format["decimalplaces"] + 2])
                else:
                    fraction = ""
                text = "{}{}{}".format(sign, "".join(digits), fraction)
                item = QTableWidgetItem(text)
                item.setTextAlignment(Qt.AlignRight |
                                      Qt.AlignVCenter)
                if sign and self.format["rednegatives"]:
                    item.setBackground(Qt.green)
                self.table.setItem(y, x, item)

    def setNumberFormat1(self):
        dialog = duihua.NumberFormatDlg(self.format, self)
        if dialog.exec_():
            self.format = dialog.numberFormat()
            self.refreshTable()

    def setNumberFormat2(self):
        dialog = duihua1.NumberFormatDlg(self.format, self)
        dialog.mysignal.connect(self.refreshTable)
        dialog.show()

    def setNumberFormat3(self):
        if self.numberFormatDlg is None:
            self.numberFormatDlg = duihua2.NumberFormatDlg(
                self.format, self.refreshTable, self)
        self.numberFormatDlg.show()
        self.numberFormatDlg.raise_()
        self.numberFormatDlg.activateWindow()

app = QApplication(sys.argv)
form = Form()
form.show()
app.exec_()

