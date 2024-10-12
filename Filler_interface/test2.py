import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QProgressBar, QLabel, QDialog
from PyQt5.QtCore import QThread, pyqtSignal
import time

class Worker(QThread):
    update_progress = pyqtSignal(int)
    show_new_window = pyqtSignal()

    def runs(self):
        for i in range(11):
            time.sleep(1)
            self.update_progress.emit(i * 10)
            if i == 10:
                self.show_new_window.emit()


class WorkerThread(QThread):
    work = Worker()

    def run(self):
        self.work.runs()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt Progress Bar Example")
        self.setGeometry(100, 100, 400, 200)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)

        self.label = QLabel("Ready", self)

        self.start_button = QPushButton("Start", self)
        self.start_button.clicked.connect(self.start_thread)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.start_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.worker_thread = WorkerThread()
        self.worker_thread.work.update_progress.connect(self.update_progress)
        self.worker_thread.work.show_new_window.connect(self.show_new_window)

    def start_thread(self):
        self.worker_thread.start()

    def update_progress(self, value):
        self.progress_bar.setValue(value)
        self.update_label(value // 10)

    def update_label(self, value):
        if value == 0:
            self.label.setText("First message")
        elif value == 1:
            self.label.setText("Second message")
        elif value == 3:
            self.label.setText("Third message")
        else:
            self.label.setText(f"Progress: {value * 10}%")

    def show_new_window(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("New Window")
        dialog.setGeometry(150, 150, 300, 100)
        label = QLabel("Counter reached 10!", dialog)
        layout = QVBoxLayout()
        layout.addWidget(label)
        dialog.setLayout(layout)
        dialog.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())