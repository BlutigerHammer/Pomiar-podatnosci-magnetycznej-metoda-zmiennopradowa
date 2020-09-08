from PyQt5 import QtWidgets, QtCore, uic, QtGui
from pathlib import Path
import sys
from main import Aparature
import save_to
from time import sleep


BACKGROUND_MAGNETISM = 1.45e-5


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi('gui-pl.ui', self)
        self.setWindowTitle('Pomiar podatnosci magnetycznej metodą zmiennopradową')

        self.x = []
        self.y = []
        self.csv_paths = []
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

    def closeEvent(self, event):
        result = QtGui.QMessageBox.question(self,
                                            "Zamknij program",
                                            "Czy zamknąć program? \
                                            \nCzy, przed zamknięciem, zapisać wszystkie dane z pomiarów do pliku Excel (.xlsx) ? ",
                                            QtGui.QMessageBox.Cancel | QtGui.QMessageBox.Close | QtGui.QMessageBox.Save)

        if result == QtGui.QMessageBox.Cancel:
            event.ignore()
        elif result == QtGui.QMessageBox.Close:
            event.accept()
        elif result == QtGui.QMessageBox.Save:
            path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "", "", "Excel Files (*.xlsx)")
            save_to.csv_to_xmls(path, self.csv_paths)

    def sample_setting_plot(self):
        self.data = self.Meters.sample_setting()
        if self.data is not None:
            self.x.append(self.data[0])
            self.y.append(self.data[1] - BACKGROUND_MAGNETISM)
            self.data_line.setData(self.x, self.y)  # Update the data.

    def phase_setting_plot(self):
        self.phase = - 90
        self.Meters.voltmeter.write(bytes(f"P {self.phase} \r", encoding='utf8'))
        # sleep(5)
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
        self.x = []
        self.y = []

    def save_data(self):
        path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "", "", "CSV Files (*.csv) ;;Text Files (*.txt)")
        parameters = {'magnetyzm tła': BACKGROUND_MAGNETISM, 'faza': self.phase, 'położenie próbki': 'nodata',
                      'czułość': 'no data', 'wartości x': self.xLabel.text(), 'wartości y': self.yLabel.text()}
        save_to.save_to_csv(path, parameters, self.x, self.y)
        self.csv_paths.append(path)


app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
w.show()
sys.exit(app.exec_())
