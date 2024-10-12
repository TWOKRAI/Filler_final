import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
from PyQt5.QtCore import QThread, pyqtSignal, QTimer

class CounterThread(QThread):
    update_signal = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self._running = False
        self.count = 0

    def run(self):
        self._running = True
        while self._running:
            self.update_signal.emit(self.count)
            self.count += 1
            QThread.msleep(1000)

    def stop(self):
        self._running = False

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.label = QLabel("Counter: 0", self)
        self.label.move(50, 50)

        self.button = QPushButton("Start", self)
        self.button.move(50, 100)
        self.button.clicked.connect(self.on_button_clicked)

        self.counter_thread = CounterThread()
        self.counter_thread.update_signal.connect(self.update_label)

    def on_button_clicked(self):
        if self.counter_thread.isRunning():
            self.counter_thread.stop()
            self.button.setText("Start")
        else:
            self.counter_thread = CounterThread()
            self.counter_thread.count = int(self.label.text().split(': ')[1])
            self.counter_thread.update_signal.connect(self.update_label)
            self.counter_thread.start()
            self.button.setText("Stop")

    def update_label(self, count):
        self.label.setText(f"Counter: {count}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("PyQt Counter")
    window.show()
    sys.exit(app.exec_())
