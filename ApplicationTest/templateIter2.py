# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Paolo\Desktop\templateIter2.ui'
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

class Ui_CustomWidget(object):
    def setupUi(self, CustomWidget):
        CustomWidget.setObjectName(_fromUtf8("CustomWidget"))
        CustomWidget.resize(517, 440)
        self.gridLayout = QtGui.QGridLayout(CustomWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.checkBox = QtGui.QCheckBox(CustomWidget)
        self.checkBox.setChecked(True)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.gridLayout.addWidget(self.checkBox, 1, 0, 1, 1)
        self.plotWidget = PlotWidget(CustomWidget)
        self.plotWidget.setObjectName(_fromUtf8("plotWidget"))
        self.gridLayout.addWidget(self.plotWidget, 0, 0, 1, 1)
        self.pushButton = QtGui.QPushButton(CustomWidget)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.gridLayout.addWidget(self.pushButton, 2, 0, 1, 1)
        self.pushButton_2 = QtGui.QPushButton(CustomWidget)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.gridLayout.addWidget(self.pushButton_2, 3, 0, 1, 1)
        self.pushButton_3 = QtGui.QPushButton(CustomWidget)
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.gridLayout.addWidget(self.pushButton_3, 4, 0, 1, 1)

        self.retranslateUi(CustomWidget)
        QtCore.QMetaObject.connectSlotsByName(CustomWidget)

    def retranslateUi(self, CustomWidget):
        CustomWidget.setWindowTitle(_translate("CustomWidget", "Form", None))
        self.checkBox.setText(_translate("CustomWidget", "Mouse Enabled", None))
        self.pushButton.setText(_translate("CustomWidget", "Breath Speed", None))
        self.pushButton_2.setText(_translate("CustomWidget", "Volumetric Flow", None))
        self.pushButton_3.setText(_translate("CustomWidget", "Volume", None))

from pyqtgraph import PlotWidget

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    CustomWidget = QtGui.QWidget()
    ui = Ui_CustomWidget()
    ui.setupUi(CustomWidget)
    CustomWidget.show()
    sys.exit(app.exec_())

