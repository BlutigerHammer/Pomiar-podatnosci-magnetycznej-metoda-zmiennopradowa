from PyQt5 import QtWidgets, QtCore, uic
import save_to
from time import sleep


BACKGROUND = 1.45e-5
MAX_POSITION = 72


def sample_setting_plot(self):
    x = self.Meters.change_position(0, self.position)
    sleep(x * 0.5)
    for position in range(MAX_POSITION):
        self.position = position
        try:
            data = self.Meters.sample_setting(position)
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
        try:
            data = self.Meters.phase_setting(-phase)
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
    try:
        data = self.Meters.measurement()
        self.x.append(data[0])
        self.y.append(data[1] - BACKGROUND)
        self.data_line.setData(self.x, self.y)  # Update the data
        self.xValue.setText(str(round(data[0], 1)))
        self.yValue.setText(str(data[1]))
    except:
        self.xValue.setText('ERROR')
        self.yValue.setText('ERROR')

def save_data(self):
    path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "", "", "CSV Files (*.csv) ;;Text Files (*.txt)")
    parameters = {'tło[V]': BACKGROUND, 'faza[°]': self.phase, 'położenie próbki': self.position,
                  'czułość': self.sensivity, 'wartości x': self.xLabel.text(), 'wartości y': self.yLabel.text()}
    try:
        save_to.save_to_csv(path, parameters, self.x, self.y)
        self.csv_paths.append(path)
    except:
        self.error_message()
