from PyQt5 import QtWidgets, QtCore, uic

import sys
from main import Aparature
import save_to
from time import sleep

BACKGROUND = 1.45e-5
MAX_POSITION = 72


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi('gui-pl.ui', self)
        self.setWindowTitle('Pomiar podatnosci magnetycznej metodą zmiennopradową')

        self.x = []
        self.y = []
        self.csv_paths = []
        self.phase = -87
        self.position = 0
        self.sensivity = '500uV'
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
        try:
            self.Meters = Aparature()
        except Exception as errors:
            self.critical_message("Następujące urządzenia nie są podłączone poprawnie:\n" + str(errors)
                                  + "\nSprawdź połączenie USB i uruchom ponownie program")

    def closeEvent(self, event):
        result = QtWidgets.QMessageBox.question(self, "Zamknij program",
                                                "Czy zapisać dane z pomiarów do pliku Excel (.xlsx)?",
                                                QtWidgets.QMessageBox.Cancel | QtWidgets.QMessageBox.No |
                                                QtWidgets.QMessageBox.Yes)

        if result == QtWidgets.QMessageBox.Cancel:
            event.ignore()
        elif result == QtWidgets.QMessageBox.No:
            try:
                self.Meters.change_position(0, self.position)
            except AttributeError:
                pass
            event.accept()
        elif result == QtWidgets.QMessageBox.Yes:
            path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "", "", "Excel Files (*.xlsx)")
            try:
                save_to.csv_to_xlsx(path, self.csv_paths)
            except Exception:
                event.ignore()
            try:
                self.Meters.change_position(0, self.position)
            except AttributeError:
                pass

    def sample_setting_plot(self):
        x = self.Meters.change_position(0, self.position)
        sleep(x*0.5)
        for position in range(MAX_POSITION):
            self.position = position
            data = self.Meters.sample_setting(position)
            try:
                self.x.append(position)
                self.y.append(data[1] - BACKGROUND)
                self.data_line.setData(self.x, self.y)  # Update the data
                QtCore.QCoreApplication.sendPostedEvents()
                self.xValue.setText(str(data[0]))
                self.yValue.setText(str(data[1]))
            except:
                self.xValue.setText('ERROR')
                self.yValue.setText('ERROR')
        self.sensivity = self.Meters.change_sensivity(abs(max(self.y, key=abs)))
        print('sesn:', self.sensivity)
        self.position = self.x[self.y.index(max(self.y, key=abs))]
        self.xValue.setText(str(self.position))
        self.yValue.setText('')
        self.Meters.change_position(0, MAX_POSITION - self.position)
        self.stopButton_clicked()

    def phase_setting_plot(self):
        self.phase = - 80
        sleep(5)
        for phase in range(80, 100):
            data = self.Meters.phase_setting(-phase)
            try:
                self.x.append(data[0])
                self.y.append(data[1] - BACKGROUND)
                self.data_line.setData(self.x, self.y)  # Update the data
                QtCore.QCoreApplication.sendPostedEvents()
                self.xValue.setText(str(data[0]))
                self.yValue.setText(str(data[1]))
            except:
                self.xValue.setText('ERROR')
                self.yValue.setText('ERROR')
        self.phase = self.x[self.y.index(max(self.y, key=abs))]
        self.xValue.setText(str(self.phase))
        self.yValue.setText('')
        self.Meters.voltmeter.write(bytes(f"P {self.phase} \r", encoding='utf8'))
        self.stopButton_clicked()

    def measurement_plot(self):
        data = self.Meters.measurement()
        try:
            self.x.append(data[0])
            self.y.append(data[1] - BACKGROUND)
            self.data_line.setData(self.x, self.y)  # Update the data
            self.xValue.setText(str(round(data[0], 1)))
            self.yValue.setText(str(data[1]))
        except:
            self.xValue.setText('ERROR')
            self.yValue.setText('ERROR')

    def sampleSetting_clicked(self):
        self.data_function = self.sample_setting_plot
        self.startButton.setEnabled(True)
        self.plotWidget.setTitle("Ustawienie próbki", color='k')
        self.plotWidget.setLabel('left', 'Napięcie [V]', color='k')
        self.plotWidget.setLabel('bottom', 'Położenie', color='k')
        self.xLabel.setText('Położenie')
        self.yLabel.setText('Napięcie [V]')

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
        parameters = {'tło[V]': BACKGROUND, 'faza[°]': self.phase, 'położenie próbki': self.position,
                      'czułość': self.sensivity, 'wartości x': self.xLabel.text(), 'wartości y': self.yLabel.text()}
        try:
            save_to.save_to_csv(path, parameters, self.x, self.y)
            self.csv_paths.append(path)
        except:
            self.error_message()

    def error_message(self):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Critical)
        msgBox.setText("Nie udało się zapisać pliku, czy chcesz spróbować ponownie?")
        msgBox.setWindowTitle("Błąd zapisu")
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)
        self.save_data()

    def critical_message(self, text):
        QtWidgets.QMessageBox.critical(self, "Zamknij program", text, QtWidgets.QMessageBox.Ok)


app = QtWidgets.QApplication(sys.argv)

locale = QtCore.QLocale.system().name()
qtTranslator = QtCore.QTranslator()
if qtTranslator.load("qt_" + locale):
    app.installTranslator(qtTranslator)

w = MainWindow()
w.show()
sys.exit(app.exec_())
