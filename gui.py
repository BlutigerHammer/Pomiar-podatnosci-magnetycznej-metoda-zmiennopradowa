from PyQt5 import QtWidgets, QtCore, uic
from pathlib import Path
import sys
from main import Aparature


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi('gui-pl.ui', self)
        self.setWindowTitle('Pomiar podatnosci magnetycznej metodą zmiennopradową')

        self.x = []  
        self.y = []
        self.i = 0
        self.data = None
        self.mode = 0

        self.plotWidget.setBackground('w')

        self.data_line = self.plotWidget.plot(self.x, self.y, symbol='o', symbolSize=5, symbolBrush='k', symbolPen=None,
                                              pen=None)

        self.startButton.clicked.connect(self.startButton_clicked)
        self.stopButton.clicked.connect(self.stopButton_clicked)
        self.stopButton.setEnabled(False)
        self.startButton.setEnabled(False)

        self.phaseSetting.clicked.connect(self.phaseSetting_clicked)
        self.sampleSetting.clicked.connect(self.sampleSetting_clicked)
        self.measurement.clicked.connect(self.measurement_clicked)

        self.Meters = Aparature()

    def sampleSetting_clicked(self):
        self.mode = 1
        self.startButton.setEnabled(True)
        self.plotWidget.setTitle("Ustawienie próbki", color='k')
        self.plotWidget.setLabel('left', 'Napięcie [V]')
        self.plotWidget.setLabel('bottom', 'Położenie')

    def phaseSetting_clicked(self):
        self.mode = 2
        self.startButton.setEnabled(True)
        self.plotWidget.setTitle("Ustawienie fazy", color='k')
        self.plotWidget.setLabel('left', 'Napięcie [V]')
        self.plotWidget.setLabel('bottom', 'Faza [°]')

    def measurement_clicked(self):
        self.mode = 3
        self.path = Path("data/measurement.txt")
        self.startButton.setEnabled(True)
        self.plotWidget.setTitle("Pomiar", color='k')
        self.plotWidget.setLabel('left', 'Napięcie [V]')
        self.plotWidget.setLabel('bottom', 'Temperatura [V]')

    def update_plot_data(self):
        if self.mode == 1:
            self.data = self.Meters.sample_setting(self.i)
        if self.mode == 2:
            self.data = self.Meters.phase_setting(self.i)
        if self.mode == 3:
            self.data = self.Meters.measurement()

        if self.data is not False:
            self.x.append(self.data[0])
            self.y.append(self.data[1])
            self.data_line.setData(self.x, self.y)  # Update the data.
            self.i += 1


    def startButton_clicked(self):
        self.startButton.setEnabled(False)
        self.stopButton.setEnabled(True)
        self.measurement.setEnabled(False)
        self.sampleSetting.setEnabled(False)
        self.phaseSetting.setEnabled(False)

        self.timer = QtCore.QTimer()
        self.timer.setInterval(1)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

    def stopButton_clicked(self):
        self.stopButton.setEnabled(False)
        self.startButton.setEnabled(True)
        self.measurement.setEnabled(True)
        self.sampleSetting.setEnabled(True)
        self.phaseSetting.setEnabled(True)
        self.x = []
        self.y = []
        self.i = 0
        self.timer.timeout.disconnect(self.update_plot_data)


app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
w.show()
sys.exit(app.exec_())
