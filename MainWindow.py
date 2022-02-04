from PyQt5 import QtWidgets, QtCore, uic

from Aparature import Aparature
import save_to


class MainWindow(QtWidgets.QMainWindow):
    from _logic import sample_setting_plot, phase_setting_plot, measurement_plot, save_data
    from _messages import error_message, critical_message, input_temperature_message
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
            self.closeEvent('error')

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
        self.input_temperature_message()

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

        self.Meters.thermometer.write("SYStem:LOCal")
        self.save_data()
        self.x = []
        self.y = []
