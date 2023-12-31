import os
import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import QThreadPool

from utils import init_logger
from guis.basicGUI import basicGUI
from guis.canonsGUI import canonsGUI
from guis.takePhotosGUI import takePhotosGUI

from guis.piEyedPiperGUI import piEyedPiperGUI
from guis.progressDialog import progressDialog
from guis.settings.settings import DEBUG, STORAGE_PATH


class entomoloGUI(basicGUI, QtWidgets.QMainWindow):
    """
    entomoloGUI is a graphical user interface designed for pinned insect imaging
      at the Natural History Museum of Denmark.

    The idea is to have two high resolution canon cameras. One focused on the dorsal view of
      the specimen and one on the lateral view.

    To image the labels, five 12MP raspberry pi (Pi-Eyes) are used. Based on the ALICE setup
      designed by the Natural History Museum of London, four Pi-Eyes will take angled images
      of the labels so that label information can be captured without the labels being removed.
      The fifth Pi-Eye is used for imaging the qr code added to the pins, or, if the digitizer
      decides the labels are important enough to be removed and imaged separately, it will focus
      on imaging the labels
    """

    def __init__(self):
        super(entomoloGUI, self).__init__()

        # Used to run worker threads in other guis
        self.threadpool = QThreadPool()

        # make a pop up to give users something pretty to look at
        # self.progress = progressDialog()
        # self.progress._open()

        # setup the pi-eyes gui
        self.piEyedPiper = piEyedPiperGUI(threadpool=self.threadpool)
        # self.progress.update(60, "Making Bacon..")

        # setup the canons guid
        self.canons = canonsGUI(threadpool=self.threadpool)
        # self.progress.update(70, "Doing Breakfast Dishes..")

        # setup the take photos button
        self.takePhotos = takePhotosGUI(STORAGE_PATH, threadpool=self.threadpool)
        # self.progress.update(100, "Grabbing Keys..")

        self.initUI()

        # self.progress._close()

    def initUI(self):
        """initUT
        Sets the layout of the UI
        """
        self.setWindowTitle("EntomoloGUI")
        self.setWindowIcon(QtGui.QIcon("EntomoloGUI/media/icon.png"))

        # specify the locations and size for each component
        self.grid.addWidget(self.piEyedPiper, 0, 0, 1, 5)
        self.grid.addWidget(self.canons, 1, 0, 1, 6)
        self.grid.addWidget(self.takePhotos, 2, 6, 1, 1)

        self.setLayout(self.grid)
        self.show()

        topLeftPoint = QtWidgets.QApplication.desktop().availableGeometry().topLeft()
        self.move(topLeftPoint)


if __name__ == "__main__":
    init_logger(debug=DEBUG)

    QtCore.QCoreApplication.addLibraryPath(
        os.path.join(
            os.path.dirname(QtCore.__file__)
        )
    )

    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon("/Users/dassco/Pi-Eyed-Piper/EntomoloGUI/media/icon.png"))
    gui = entomoloGUI()
    gui.show()
    sys.exit(app.exec_())
