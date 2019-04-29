#!/usr/bin/python3
import os
import subprocess
import sys
from PyQt5.QtWidgets import (QWidget, QApplication, QVBoxLayout, QLabel, QPushButton)
from PyQt5.QtCore import (Qt, QObject)

class gyroscope(object):
    def __init__(self, address):
        self.address = address

    accelX = 0
    accelY = 0
    accelZ = 0
    gyroX = 0
    gyroY = 0
    gyroZ = 0
    count = 0

    PWR_MGMT_1 = "0x6B"
    ACCEL_X_OUT_H = "0x3B"
    ACCEL_X_OUT_L = "0x3C"
    ACCEL_Y_OUT_H = "0x3D"
    ACCEL_Y_OUT_L = "0x3E"
    ACCEL_Z_OUT_H = "0x3F"
    ACCEL_Z_OUT_L = "0x40"
    GYRO_X_OUT_H = "0x43"
    GYRO_X_OUT_L = "0x44"
    GYRO_Y_OUT_H = "0x45"
    GYRO_Y_OUT_L = "0x46"
    GYRO_Z_OUT_H = "0x47"
    GYRO_Z_OUT_L = "0x48"

    bashSet = "i2cset -y 2"
    bashGet = "i2cget -y 2"

    def exec(self, cmd):
        cmdList = cmd.split()
        res = subprocess.check_output(cmdList).decode('utf-8').strip('\n')
        return res

    def set(self, reg1, reg2, val):
        cmd = self.bashSet + " " + reg1 + " " + reg2 + " " + val
        execute = self.exec(cmd)

    def get(self, reg1, reg2):
        cmd = self.bashGet + " " + reg1 + " " + reg2
        res = self.exec(cmd)
        return res

    def twosComplement(self, hex, bits):
        val = int(hex, 16)
        if val & (1 << (bits - 1)):
          val -= 1 << bits
        return val

    def doWork(self, function):
        while (self.count < 10000):
            self.accelX = round((self.twosComplement(self.get(self.address, self.ACCEL_X_OUT_H).split("x")[1] + self.get(self.address, self.ACCEL_X_OUT_L).split("x")[1], 16) / 16700) * 90, 1)
            self.accelY = round((self.twosComplement(self.get(self.address, self.ACCEL_Y_OUT_H).split("x")[1] + self.get(self.address, self.ACCEL_Y_OUT_L).split("x")[1], 16) / 16700) * 90, 1)
            self.accelZ = round((self.twosComplement(self.get(self.address, self.ACCEL_Z_OUT_H).split("x")[1] + self.get(self.address, self.ACCEL_Z_OUT_L).split("x")[1], 16) / 18000) * 90, 1)

            self.gyroX = round(self.twosComplement(self.get(self.address, self.GYRO_X_OUT_H).split("x")[1] + self.get(self.address, self.GYRO_X_OUT_L).split("x")[1], 16) / 131, 1)
            self.gyroY = round(self.twosComplement(self.get(self.address, self.GYRO_Y_OUT_H).split("x")[1] + self.get(self.address, self.GYRO_Y_OUT_L).split("x")[1], 16) / 131, 1)
            self.gyroZ = round(self.twosComplement(self.get(self.address, self.GYRO_Z_OUT_H).split("x")[1] + self.get(self.address, self.GYRO_Z_OUT_L).split("x")[1], 16) / 131, 1)

            function(str(self.accelX), str(self.accelY), str(self.accelZ), str(self.gyroX), str(self.gyroY), str(self.gyroZ))
            self.count = self.count + 1

class myWidget(QWidget):
    def __init__(self, gyroscope, app):
        super().__init__()

        self.initUI()
        self.gyroscope = gyroscope
        self.app = app

    def initUI(self):
        self.setWindowTitle("Gyroscope Data")
        self.setStyleSheet("QLabel {font: 20pt Arial}")
        self.button = QPushButton("The Button", self)
        self.button.clicked.connect(self.doTheThing)
        self.accelX = QLabel("0")
        self.accelY = QLabel("0")
        self.accelZ = QLabel("0")
        self.gyroX = QLabel("0")
        self.gyroY = QLabel("0")
        self.gyroZ = QLabel("0")
        vbox = QVBoxLayout()
        vbox.addWidget(self.button)
        vbox.addWidget(self.accelX)
        vbox.addWidget(self.accelY)
        vbox.addWidget(self.accelZ)
        vbox.addWidget(self.gyroX)
        vbox.addWidget(self.gyroY)
        vbox.addWidget(self.gyroZ)
        self.setLayout(vbox)

    def updateText(self, num1, num2, num3, num4, num5, num6):
        self.accelX.setText(num1)
        self.accelY.setText(num2)
        self.accelZ.setText(num3)
        self.gyroX.setText(num4)
        self.gyroY.setText(num5)
        self.gyroZ.setText(num6)
        app.processEvents()

    def doTheThing(self):
        self.gyroscope.doWork(self.updateText)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gyro = gyroscope("0x68")
    gyro.set(gyro.address, gyro.PWR_MGMT_1, "0")
    window = myWidget(gyro, app)
    window.show()
    sys.exit(app.exec_())
