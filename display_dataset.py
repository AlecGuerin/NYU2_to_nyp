import numpy as np
import os
import sys
import torch
import matplotlib.pyplot as plt
import torchvision.transforms as T
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import matplotlib
from PyQt5 import QtCore, QtWidgets, QtGui

matplotlib.use("Qt5Agg")
DATA_PATH = 'data'
DATA_SET_PATH = os.path.join(DATA_PATH, 'datset')

class Ui_MainWindow(QtCore.QObject):

    keyPressed = QtCore.pyqtSignal(QtCore.QEvent)

    img_max = 1148
    i = 0
    def __init__(self) -> None:
        super(Ui_MainWindow, self).__init__()
        
    def setupUi(self, MainWindow, img_max=img_max):

        self.img_max=img_max        

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(50, 10)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")

        # Manage the plot to display
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        f = get_plot(self.i)
        self.canvas = FigureCanvasQTAgg(f)
        plt.close(f)
        self.canvas.setSizePolicy(sizePolicy)
        self.canvas.setObjectName("canvas")
        self.verticalLayout.addWidget(self.canvas)

        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_prev = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_prev.sizePolicy().hasHeightForWidth())
        self.pushButton_prev.setSizePolicy(sizePolicy)
        self.pushButton_prev.setObjectName("pushButton_prev")
        self.horizontalLayout.addWidget(self.pushButton_prev)
        self.pushButton_next = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_next.sizePolicy().hasHeightForWidth())
        self.pushButton_next.setSizePolicy(sizePolicy)
        self.pushButton_next.setObjectName("pushButton_next")
        self.horizontalLayout.addWidget(self.pushButton_next)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.frame)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)




    def retranslateUi(self, MainWindow):
        # Draw data
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "dataset displayer"))
        self.pushButton_prev.setText(_translate("MainWindow", "Previous"))
        self.pushButton_next.setText(_translate("MainWindow", "Next"))
        self.canvas.draw()
        # Set event
        self.pushButton_next.clicked.connect(lambda: self.on_clicked(self.pushButton_next.objectName()))
        self.pushButton_prev.clicked.connect(lambda: self.on_clicked(self.pushButton_prev.objectName()))
        self.keyPressed.connect(self.on_key)
        
    def update_img(self, inc):

        self.i += inc
        if self.i > self.img_max: self.i = 0
        elif self.i < 0: self.i = self.img_max
        
        f = get_plot(self.i)
        self.canvas.figure = f
        self.canvas.draw()
        plt.close(f)


    def keyPressEvent(self, event):
        super(QtWidgets.QMainWindow, self).keyPressEvent(event)
        self.keyPressed.emit(event)

    def on_key(self, event):
        if event.key() == QtCore.Qt.Key_N:
            self.update_img(1)
        elif event.key() == QtCore.Qt.Key_P:
            self.update_img(-1)
        

    def on_clicked(self, name):
        if name == self.pushButton_next.objectName():
            self.update_img(1)
        elif name == self.pushButton_prev.objectName():
            self.update_img(-1)



def get_plot(i):
    img_path = os.path.join(DATA_SET_PATH, 'image')
    lab_path = os.path.join(DATA_SET_PATH, 'label')

    img_file = os.path.join(img_path, f'{i}.npy')
    lab_file = os.path.join(lab_path, f'{i}.npy')

    img = torch.from_numpy(np.moveaxis(np.load(img_file), -1, 0))
    lab = torch.from_numpy(np.load(lab_file))

    img = torch.squeeze(img)
    lab = torch.squeeze(lab)

    transform = T.ToPILImage()
    lab = lab.detach().numpy()+1
    img = transform(img)

    f, axs = plt.subplots(nrows=1, ncols=2, figsize=(10, 5))
    axs[0].imshow(img)
    f.colorbar(axs[1].imshow(lab), orientation='horizontal')
    return f

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow,)
    MainWindow.show()
    sys.exit(app.exec_())