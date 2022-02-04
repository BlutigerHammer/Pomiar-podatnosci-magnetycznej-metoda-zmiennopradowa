import sys
from PyQt5 import QtWidgets, QtCore
from MainWindow import MainWindow

app = QtWidgets.QApplication(sys.argv)

locale = QtCore.QLocale.system().name()
qtTranslator = QtCore.QTranslator()
if qtTranslator.load("qt_" + locale):
    app.installTranslator(qtTranslator)

w = MainWindow()
w.show()
sys.exit(app.exec_())
