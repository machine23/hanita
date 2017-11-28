import sys
from PyQt5 import QtWidgets
import client_ui


class QTClientView(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)

        text, ok = QtWidgets.QInputDialog.getText(self, "Login",
                                                  "Enter your name")
        if ok and text:
            print(text)
        self.ui = client_ui.Ui_MainWindow()
        self.ui.setupUi(self)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = QTClientView()
    window.show()
    sys.exit(app.exec_())