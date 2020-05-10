import sys
from PyQt5 import QtWidgets, QtGui
from main_ui import Ui_AppMainWindow
from PyQt5 import QtCore as qtc
import nse_driver
import time


class Worker(qtc.QThread):
    fetch_completed = qtc.pyqtSignal(dict)
    status = qtc.pyqtSignal(bool)

    def __init__(self, parent=None):
        super(Worker, self).__init__(parent)
        self.thread_active = True

    @qtc.pyqtSlot(int)
    def call_api(self, interval):
        self.status.emit(self.thread_active)
        try:
            while self.thread_active:
                print(interval)
                self.fetch_completed.emit(nse_driver.start_fetch())
                time.sleep(interval)
        except OverflowError:
            print("Time Interval Too Large")

    def stop(self):
        self.thread_active = False
        self.status.emit(self.thread_active)
        self.wait()


class MainDriver(QtWidgets.QMainWindow):
    fetch_requested_signal = qtc.pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.stock_data = nse_driver.start_fetch()
        self.ui = Ui_AppMainWindow()
        self.setWindowIcon(QtGui.QIcon("./icon.ico"))
        self.ui.setupUi(self)
        self.ui.start_button.released.connect(self.start_thread)
        self.ui.stop_button.clicked.connect(self.stop_thread)
        self.ui.stop_button.setEnabled(False)
        self.show()

    def start_thread(self):
        self.worker = Worker()
        self.worker_thread = qtc.QThread(self)
        self.worker.fetch_completed.connect(self.set_table)
        self.worker.fetch_completed.connect(self.set_stats)
        self.worker.status.connect(self.set_status)
        self.fetch_requested_signal.connect(self.worker.call_api)
        self.worker.moveToThread(self.worker_thread)
        self.worker_thread.start()
        self.start_fetch()

    def start_fetch(self):
        interval = self.get_interval()
        if interval is None:
            self.ui.status_bar.showMessage("Default Time Interval Selected: 30s", 5000)
            self.fetch_requested_signal.emit(30)
        else:
            self.fetch_requested_signal.emit(interval)
            self.ui.status_bar.showMessage(
                "Time Interval Selected: {}s".format(str(interval)), 5000
            )
        self.ui.start_button.setEnabled(False)
        self.ui.stop_button.setEnabled(True)
        print("Thread Started")

    def stop_thread(self):
        self.worker.stop()
        self.ui.start_button.setEnabled(True)
        self.ui.stop_button.setEnabled(False)
        print("Thread Killed")

    def get_interval(self):
        options = ("1", "15", "30", "60")
        item, submitted = QtWidgets.QInputDialog.getItem(
            self, "Set Time Interval", "Seconds:", options, 2, False,
        )
        if submitted and item:
            return int(item)

    def set_status(self, status):
        if status:
            self.ui.connection.setText("Active")
            self.ui.connection.setStyleSheet("color: green")
        else:
            self.ui.connection.setText("Inactive")
            self.ui.connection.setStyleSheet("color: red")

    def set_table(self, stock_data):
        self.ui.price_table.setRowCount(0)
        self.ui.price_table.setColumnCount(8)
        for data_list in stock_data["priceDict"]:
            row = self.ui.price_table.rowCount()
            self.ui.price_table.setRowCount(row + 1)
            self.add_table_row(row, data_list)

    def add_table_row(self, row, data_list):
        col = 0
        for item in data_list:
            cell = QtWidgets.QTableWidgetItem(item)
            self.ui.price_table.setItem(row, col, cell)
            col += 1

    def set_stats(self, stock_data):
        self.ui.total_num.setText(str(self.stock_data["stats"]["total"]))
        self.ui.profit_num.setText(str(self.stock_data["stats"]["profit"]))
        self.ui.profit_num.setStyleSheet("color: green")
        self.ui.loss_num.setText(str(self.stock_data["stats"]["loss"]))
        self.ui.loss_num.setStyleSheet("color: red")
        self.ui.no_change_num.setText(str(self.stock_data["stats"]["noChg"]))
        self.ui.no_change_num.setStyleSheet("color: grey")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainDriver()
    w.show()
    sys.exit(app.exec_())
