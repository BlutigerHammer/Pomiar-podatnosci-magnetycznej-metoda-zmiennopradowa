from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QInputDialog

def error_message(self):
    msgBox = QtWidgets.QMessageBox()
    msgBox.setIcon(QtWidgets.QMessageBox.Critical)
    msgBox.setText("Nie udało się zapisać pliku, czy chcesz spróbować ponownie?")
    msgBox.setWindowTitle("Błąd zapisu")
    msgBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)
    self.save_data()


def critical_message(self, text):
    QtWidgets.QMessageBox.critical(self, "Zamknij program", text, QtWidgets.QMessageBox.Ok)


def input_temperature_message(self):
    temp, ok_pressed = QInputDialog.getDouble(self, "Welcome",
                                              "Program opened properly, please specify the temperature (in celsius):",
                                              20, 15, 30, 1)
    if ok_pressed:
        self.Meters.cold_junction_compesation = 0.04029 * temp - 0.01591