import numpy as np
import os
import sys
import torch
import matplotlib.pyplot as plt
import torchvision.transforms as T
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import matplotlib
import argparse
from PyQt5 import QtCore, QtWidgets


matplotlib.use("Qt5Agg")
DATA_PATH = 'data'
DATA_SET_PATH = os.path.join(DATA_PATH, 'datset')

class Ui_MainWindow(QtCore.QObject):

    keyPressed = QtCore.pyqtSignal(QtCore.QEvent)

    dataset_path=DATA_SET_PATH
    img_max = 1148
    i = 0

    def __init__(self) -> None:
        super(Ui_MainWindow, self).__init__()

    def initialze_canvas(self):
        # Manage the plot to display
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        f = get_plot(self.i, self.dataset_path)
        self.canvas = FigureCanvasQTAgg(f)
        plt.close(f)
        self.canvas.setSizePolicy(sizePolicy)
        self.canvas.setObjectName("canvas")
        self.verticalLayout.addWidget(self.canvas)

    def setupUi(self, MainWindow, dataset_path=None, img_max=None):


        if img_max != None:
            self.img_max=img_max
        if dataset_path != None:
            self.dataset_path=dataset_path


        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.initialze_canvas()
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_prev = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_prev.sizePolicy().hasHeightForWidth())
        self.pushButton_prev.setSizePolicy(sizePolicy)
        self.pushButton_prev.setObjectName("pushButton_prev")
        self.horizontalLayout.addWidget(self.pushButton_prev)
        self.pushButton_next = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_next.sizePolicy().hasHeightForWidth())
        self.pushButton_next.setSizePolicy(sizePolicy)
        self.pushButton_next.setObjectName("pushButton_next")
        self.horizontalLayout.addWidget(self.pushButton_next)
        self.horizontalLayout_3.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.spinBox_index = QtWidgets.QSpinBox(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBox_index.sizePolicy().hasHeightForWidth())
        self.spinBox_index.setSizePolicy(sizePolicy)
        self.spinBox_index.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.spinBox_index.setObjectName("spinBox_index")
        self.horizontalLayout_2.addWidget(self.spinBox_index)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)
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
        self.label.setText(_translate("MainWindow", "image index:"))
        self.canvas.draw()
        self.spinBox_index.setMaximum(self.img_max)
        # Set event
        self.pushButton_next.clicked.connect(lambda: self.on_clicked(self.pushButton_next.objectName()))
        self.pushButton_prev.clicked.connect(lambda: self.on_clicked(self.pushButton_prev.objectName()))
        self.spinBox_index.valueChanged.connect(self.on_spinBox_value_changed)
        self.statusbar.showMessage(self.dataset_path)
        self.keyPressed.connect(self.on_key)
        
    def update_img(self):

        f = get_plot(self.i, self.dataset_path)
        self.canvas.figure = f
        self.canvas.draw()
        plt.close(f)

    def on_spinBox_value_changed(self):
        self.i = self.spinBox_index.value()
        self.update_inc(0)

    def update_inc(self, inc):
        self.i += inc
        if self.i > self.img_max:
            self.i = 0
        elif self.i < 0:
            self.i = self.img_max

        self.update_inc_dependencies()


    def update_inc_dependencies(self):
        self.update_img()
        self.update_select()

    def update_select(self):
        if self.i != self.spinBox_index.value():
            self.spinBox_index.setValue(self.i)

    def keyPressEvent(self, event):
        super(QtWidgets.QMainWindow, self).keyPressEvent(event)
        self.keyPressed.emit(event)

    def on_key(self, event):
        if event.key() == QtCore.Qt.Key_N:
            self.update_inc(1)
        elif event.key() == QtCore.Qt.Key_P:
            self.update_inc(-1)
        

    def on_clicked(self, name):
        if name == self.pushButton_next.objectName():
            self.update_inc(1)
        elif name == self.pushButton_prev.objectName():
            self.update_inc(-1)



def get_plot(i, dataset_path):
    img_path = os.path.join(dataset_path, 'image')
    lab_path = os.path.join(dataset_path, 'label')

    img_file = os.path.join(img_path, f'{i}.npy')
    lab_file = os.path.join(lab_path, f'{i}.npy')

    img = torch.from_numpy(np.moveaxis(np.load(img_file), -1, 0))
    lab = torch.from_numpy(np.load(lab_file))

    img = torch.squeeze(img)
    lab = torch.squeeze(lab)

    transform = T.ToPILImage()
    lab = lab.detach().numpy()+1
    img = transform(img)

    f, axs = plt.subplots(nrows=1, ncols=2, figsize=(15, 7))
    axs[0].imshow(img)
    f.colorbar(axs[1].imshow(lab), orientation='horizontal')
    return f

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', help='Path to the directory containing the image, label and depth directories')
    parser.add_argument('--count', type=int, help='Number of data to display')
    args = parser.parse_args()


    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow, args.dataset, args.count)
    MainWindow.show()
    sys.exit(app.exec_())