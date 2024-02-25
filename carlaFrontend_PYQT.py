import sys
import socket
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QThread, pyqtSignal
import pickle
import struct

from Qt_UI import Ui_Form

class ImageReceiver(QThread):
    # image_received = pyqtSignal(np.ndarray)
    image_received = pyqtSignal(QImage)

    def __init__(self, host, port):
        super().__init__()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))

    def run(self):
        while True:
            # Receive the data and convert it into a numpy array
            # img_bytes = self.socket.recv(1024)
            # img_array = np.frombuffer(img_bytes, dtype=np.uint8)
            # img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            def receive_data(sock, size):
                data = b''
                while len(data) < size:
                    data += sock.recv(size - len(data))
                return data

            array_length = receive_data(self.socket, 4)
            array_length = struct.unpack('!I', array_length)[0]
            array_bytes = b''
            while len(array_bytes) < array_length:
                to_read = array_length - len(array_bytes)
                array_bytes += self.socket.recv(4096 if to_read > 4096 else to_read)
            
            img = pickle.loads(array_bytes)

            if img is None:
                print("Failed to decode imaage")
                continue

            height, width, channel = img.shape
            bytesPerLine = 3 * width
            # qimg = QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
            qimg = QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888)
            # data = self.socket.recv(500 * 500 * 3)
            # img = np.frombuffer(data, dtype=np.uint8).reshape((500, 500, 3))

            # Emit a signal with the image
            self.image_received.emit(qimg)

class ImageReceiver1(QThread):
    # image_received = pyqtSignal(np.ndarray)
    image_received = pyqtSignal(QImage)

    def __init__(self, host, port):
        super().__init__()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))

    def run(self):
        while True:
            # Receive the data and convert it into a numpy array
            # img_bytes = self.socket.recv(1024)
            # img_array = np.frombuffer(img_bytes, dtype=np.uint8)
            # img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

            def receive_data(sock, size):
                data = b''
                while len(data) < size:
                    data += sock.recv(size - len(data))
                return data


            array_length = receive_data(self.socket, 4)
            array_length = struct.unpack('!I', array_length)[0]
            array_bytes = b''
            while len(array_bytes) < array_length:
                to_read = array_length - len(array_bytes)
                array_bytes += self.socket.recv(4096 if to_read > 4096 else to_read)
            
            img = pickle.loads(array_bytes)

            if img is None:
                print("Failed to decode imaage")
                continue

            height, width, channel = img.shape
            bytesPerLine = 3 * width
            # qimg = QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
            qimg = QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888)
            # data = self.socket.recv(500 * 500 * 3)
            # img = np.frombuffer(data, dtype=np.uint8).reshape((500, 500, 3))

            # Emit a signal with the image
            self.image_received.emit(qimg)


# class ImageFlowWidget(QWidget, Ui_Form):
class ImageFlowWidget(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # self.image_label = QLabel(self)
        # layout = QVBoxLayout()
        # layout.addWidget(self.image_label)
        # self.setLayout(layout)

        self.image_receiver = ImageReceiver('localhost',35650)
        self.image_receiver.image_received.connect(self.update_image)
        self.image_receiver.start()

        self.image_receiver_1 = ImageReceiver1('localhost',23149)
        self.image_receiver_1.image_received.connect(self.update_image_1)
        self.image_receiver_1.start()

    def update_image(self, qimg):
        # Convert the image to a QImage
        # qimg = QImage(img.data, img.shape[1], img.shape[0], img.strides[0], QImage.Format_RGB888).rgbSwapped
        # Convert the QImage to a QPixmap and show it
        # self.image_label.setPixmap(QPixmap.fromImage(qimg))
        self.rgb_Qlabel.setPixmap(QPixmap.fromImage(qimg))
    def update_image_1(self, qimg):
        self.lidar_Qlabel.setPixmap(QPixmap.fromImage(qimg))


app = QApplication(sys.argv)
widget = ImageFlowWidget()
widget.show()
sys.exit(app.exec_())