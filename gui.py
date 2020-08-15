from PyQt5 import QtWidgets, QtCore, uic
import sys  


import fake_meters 


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi('gui-pl.ui', self)
        
        self.x = []  
        self.y = []
        self.i = 0
        self.data = None

        self.startButton.clicked.connect(self.startButton_clicked)
        self.stopButton.clicked.connect(self.stopButton_clicked)
        self.stopButton.setEnabled(False)

        self.phaseSetting.clicked.connect(self.phaseSetting_clicked)
        self.sampleSetting.clicked.connect(self.sampleSetting_clicked)
        self.measurement.clicked.connect(self.measurement_clicked)

    def phaseSetting_clicked(self):
        print('pip phase')

    def sampleSetting_clicked(self):
        print('pip sample')

    def measurement_clicked(self):
        print('pip meas')

    def plot_data_init(self):
        self.plotWidget.setBackground('w')
        self.data_line = self.plotWidget.plot(self.x, self.y, symbol='o', symbolSize=5, symbolBrush='k', symbolPen=None, pen=None)

        self.timer = QtCore.QTimer()
        self.timer.setInterval(5)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

    def update_plot_data(self):
        self.data = fake_meters.data_generator(self.i)
        if self.data is not False:
            self.x.append(self.data[0])
            self.y.append(self.data[1])
            self.data_line.setData(self.x, self.y)  # Update the data.
            self.i += 1

    def startButton_clicked(self):
        self.startButton.setEnabled(False)
        self.stopButton.setEnabled(True)
        self.plot_data_init()

    def stopButton_clicked(self):
        self.startButton.setEnabled(True)
        self.stopButton.setEnabled(False)


app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
w.show()
sys.exit(app.exec_())
