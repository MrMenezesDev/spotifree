from PyQt5 import QtCore, QtWidgets, QtGui
import win32gui
import pyautogui


class Window(QtWidgets.QDialog):
    def __init__(self):
        super(Window, self).__init__()
        self.messageGroupBox = QtWidgets.QGroupBox("")
        self.msg_wait = "Após clicar em iniciar vá para a tela do Spotify e aguarde 5 segundos"
        self.adv = False
        self.hwnd = None
        self.createMessageGroupBox()
        self.createActions()
        self.createTrayIcon()
        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addWidget(self.messageGroupBox)
        self.setLayout(mainLayout)

        self.trayIcon.show()
        self.iniciar_button.clicked.connect(self.start_find)
        self.ok_button.clicked.connect(self.ok)

        self.setWindowTitle("SpotiFree")
        self.resize(400, 100)
        icon = QtGui.QIcon("icon.png")
        self.trayIcon.setIcon(icon)
        self.setWindowIcon(icon)
        self.timer = QtCore.QBasicTimer()
        self.timer2 = QtCore.QTimer()
        self.timer2.timeout.connect(self.tick)

    def timerEvent(self, e):
        if self.step >= 5:
            self.timer.stop()

            if self.hwnd is None:
                self.hwnd = win32gui.GetForegroundWindow()
            self.typeLabel.setText('Caso esteja tocando '
                                   + win32gui.GetWindowText(self.hwnd) +
                                   ' \nclick em OK para não ouvir as propagandas.' +
                                   '\nCaso não seja a música clique novamente em iniciar.')
            self.ok_button.show()
            return
        self.step = self.step + 1
        self.typeLabel.setText(
            "Após clicar em iniciar vá para a tela do Spotify e aguarde %d segundos" % (5 - self.step))

    def tick(self):
        text = win32gui.GetWindowText(self.hwnd)
        new_adv = not '-' in text
        if self.adv != new_adv:
            pyautogui.press('volumemute')
        self.adv = new_adv

    def start_find(self):
        self.ok_button.hide()
        self.step = 0
        self.typeLabel.setText(self.msg_wait)
        self.timer2.stop()
        self.timer.start(1000, self)

    def ok(self):
        self.timer2.start(1000)
        self.hide()

    def createMessageGroupBox(self):
        self.typeLabel = QtWidgets.QLabel(self.msg_wait)
        self.iniciar_button = QtWidgets.QPushButton("Iniciar")
        self.ok_button = QtWidgets.QPushButton("Ok")
        self.ok_button.hide()
        self.iniciar_button.setDefault(True)
        messageLayout = QtWidgets.QGridLayout()
        messageLayout.addWidget(self.typeLabel, 0, 0)
        messageLayout.addWidget(self.iniciar_button, 1, 4)
        messageLayout.addWidget(self.ok_button, 1, 3)
        self.messageGroupBox.setLayout(messageLayout)

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, 'Confirmação de fechamento', 'Tem certeza de que deseja fechar a aplicação?', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            QtWidgets.QApplication.quit()
        else:
            event.ignore()


    def createActions(self):
        self.minimizeAction = QtWidgets.QAction("Minimizar", self, triggered=self.hide)
        self.restoreAction = QtWidgets.QAction("Restaurar", self, triggered=self.showNormal)
        self.quitAction = QtWidgets.QAction("Sair", self, triggered=self.close)

    def createTrayIcon(self):
        self.trayIconMenu = QtWidgets.QMenu(self)
        self.trayIconMenu.addAction(self.minimizeAction)
        self.trayIconMenu.addAction(self.restoreAction)
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(self.quitAction)

        self.trayIcon = QtWidgets.QSystemTrayIcon(self)
        self.trayIcon.setContextMenu(self.trayIconMenu)


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    QtWidgets.QApplication.setQuitOnLastWindowClosed(False)

    window = Window()
    window.show()
    sys.exit(app.exec())
