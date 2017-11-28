import sys
import abc
from PyQt5 import QtWidgets
from sip import wrappertype
import client_ui

# from .client_view import BaseClientView

class ClientMeta(wrappertype, abc.ABCMeta): pass

class BaseClientObserver(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def model_is_changed(self):
        pass


class QTClientView(QtWidgets.QMainWindow, BaseClientObserver, metaclass=ClientMeta):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)

        text, ok = QtWidgets.QInputDialog.getText(self, "Login",
                                                  "Enter your name")
        if ok and text:
            print(text)
        self.ui = client_ui.Ui_MainWindow()
        self.ui.setupUi(self)

    def model_is_changed(self):
        pass


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = QTClientView()
    window.show()
    sys.exit(app.exec_())