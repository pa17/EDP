# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'WelcomePage.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(560, 446)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Al Bayan"))
        Dialog.setFont(font)
        Dialog.setAccessibleDescription(_fromUtf8(""))
        self.WelcomtoBreeze = QtGui.QLabel(Dialog)
        self.WelcomtoBreeze.setGeometry(QtCore.QRect(120, 60, 331, 141))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("MS Shell Dlg 2"))
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.WelcomtoBreeze.setFont(font)
        self.WelcomtoBreeze.setObjectName(_fromUtf8("WelcomtoBreeze"))
        self.SkipButton = QtGui.QPushButton(Dialog)
        self.SkipButton.setGeometry(QtCore.QRect(220, 270, 113, 32))
        self.SkipButton.setObjectName(_fromUtf8("SkipButton"))
        self.EnterPatientDetailsButton = QtGui.QPushButton(Dialog)
        self.EnterPatientDetailsButton.setGeometry(QtCore.QRect(190, 200, 181, 32))
        self.EnterPatientDetailsButton.setObjectName(_fromUtf8("EnterPatientDetailsButton"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.EnterPatientDetailsButton, self.SkipButton)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.WelcomtoBreeze.setText(_translate("Dialog", "Welcome to Breeze", None))
        self.SkipButton.setText(_translate("Dialog", "Skip", None))
        self.EnterPatientDetailsButton.setText(_translate("Dialog", "Enter Patient Details", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

