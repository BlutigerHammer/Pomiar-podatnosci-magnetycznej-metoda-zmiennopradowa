from PyQt5 import QtWidgets, QtCore, uic, QtGui
from pathlib import Path
import sys
from main import Aparature
import save_to
from time import sleep


class MainWindow(QtWidgets.QMainWindow):
    BACKGROUND_MAGNETISM = 1.45e-5

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi('gui-pl.ui', self)
        self.setWindowTitle('Pomiar podatnosci magnetycznej metodą zmiennopradową')

        self.x = []
        self.y = []
        self.data = None
        self.phase = -90
        self.data_function = None

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
        self.data_function = self.Meters.measurement()
        # save_to.create_xmls(Path('data/excel-31-08-20.xlsx'))

    def sample_setting_plot(self):
        self.data = self.Meters.sample_setting()
        if self.data is not None:
            self.x.append(self.data[0])
            self.y.append(self.data[1] - BACKGROUND_MAGNETISM)
            self.data_line.setData(self.x, self.y)  # Update the data.


    def phase_setting_plot(self):
        self.phase = - 90
        self.Meters.voltmeter.write(bytes(f"P {self.phase} \r", encoding='utf8'))
        sleep(5)
        for phase in range(90, 100):
            self.data = self.Meters.phase_setting(-phase)
            if self.data is not None:
                self.x.append(self.data[0])
                self.y.append(self.data[1] - BACKGROUND_MAGNETISM)
                self.data_line.setData(self.x, self.y)  # Update the data.
        self.phase = self.x[self.y.index(max(self.y))]
        print(self.phase)
        self.stopButton_clicked()

    def measurement_plot(self):
        self.data = self.Meters.measurement()
        if self.data is not None:
            # print(self.data)
            self.x.append(self.data[0])
            self.y.append(self.data[1] - BACKGROUND_MAGNETISM)
            self.data_line.setData(self.x, self.y)  # Update the data.
            self.xValue.setText(str(round(self.data[0], 1)))
            self.yValue.setText(str(self.data[1]))


    def sampleSetting_clicked(self):
        self.data_function = self.sample_setting_plot
        self.startButton.setEnabled(True)
        self.plotWidget.setTitle("Ustawienie próbki", color='k')
        self.plotWidget.setLabel('left', 'Napięcie [V]', color='k')
        self.plotWidget.setLabel('bottom', 'Położenie', color='k')

    def phaseSetting_clicked(self):
        self.data_function = self.phase_setting_plot
        self.startButton.setEnabled(True)
        self.plotWidget.setTitle("Ustawienie fazy", color='k')
        self.plotWidget.setLabel('left', 'Napięcie [V]', color='k')
        self.plotWidget.setLabel('bottom', 'Faza [°]', color='k')
        self.xLabel.setText('Faza [°]')
        self.yLabel.setText('Napięcie [V]')

    def measurement_clicked(self):
        self.data_function = self.measurement_plot
        self.startButton.setEnabled(True)
        self.plotWidget.setTitle("Pomiar", color='k')
        self.plotWidget.setLabel('left', 'Napięcie [V]', color='k')
        self.plotWidget.setLabel('bottom', 'Temperatura [K]', color='k')
        self.Meters.voltmeter.write(bytes(f"P {-self.phase} \r", encoding='utf8'))
        self.xLabel.setText('Temperatura [K]')
        self.yLabel.setText('Napięcie [V]')

    def startButton_clicked(self):
        self.startButton.setEnabled(False)
        self.stopButton.setEnabled(True)
        self.measurement.setEnabled(False)
        self.sampleSetting.setEnabled(False)
        self.phaseSetting.setEnabled(False)

        self.timer = QtCore.QTimer()
        self.timer.setInterval(100)

        self.timer.timeout.connect(self.data_function)
        self.timer.start()

    def stopButton_clicked(self):
        self.stopButton.setEnabled(False)
        self.timer.timeout.disconnect(self.data_function)
        self.startButton.setEnabled(True)
        self.measurement.setEnabled(True)
        self.sampleSetting.setEnabled(True)
        self.phaseSetting.setEnabled(True)

        self.save_data()
        self.file_name += 1
        self.x = []
        self.y = []

    def save_data(self):
        # path = Path('data/excel-31-08-20.xlsx')
        # sheet_name = 'a' + str(self.file_name)
        # save_to.save_to_xmls(path, self.x, self.y, sheet_name)
        path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "", "", "CSV Files (*.csv) ;;Text Files (*.txt)")
        save_to.save_to_csv(path, self.x, self.y)


app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
w.show()
sys.exit(app.exec_())
