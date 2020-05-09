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
        self.threadactive = True

    @qtc.pyqtSlot()
    def call_api(self):
        self.status.emit(self.threadactive)
        while self.threadactive:
            print("Fetching")
            self.fetch_completed.emit(nse_driver.start_fetch())
            time.sleep(30)

    def stop(self):
        self.threadactive = False
        self.status.emit(self.threadactive)
        self.wait()


class MainDriver(QtWidgets.QMainWindow):
    fetch_requested = qtc.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.stock_data = nse_driver.start_fetch()
        self.ui = Ui_AppMainWindow()
        self.setWindowIcon(QtGui.QIcon("./icon.png"))
        self.ui.setupUi(self)
        self.ui.startFetch.released.connect(self.start_thread)
        self.ui.stopFetch.clicked.connect(self.stop_fetch)

        self.show()

    def start_thread(self):
        self.worker = Worker()
        self.worker_thread = qtc.QThread(self)
        self.worker.fetch_completed.connect(self.set_table)
        self.worker.fetch_completed.connect(self.set_stats)
        self.worker.status.connect(self.set_status)
        self.fetch_requested.connect(self.worker.call_api)
        self.worker.moveToThread(self.worker_thread)
        self.worker_thread.start()
        self.start_fetch()

    def start_fetch(self):
        self.fetch_requested.emit()

    def stop_fetch(self):
        self.worker.stop()
        print("Thread Killed")

    def set_status(self, status):
        if status:
            self.ui.status.setText("Active")
            self.ui.status.setStyleSheet("color: green")
        else:
            self.ui.status.setText("Inactive")
            self.ui.status.setStyleSheet("color: red")

    def set_table(self, stock_data):
        self.ui.priceTable.setRowCount(0)
        self.ui.priceTable.setColumnCount(8)
        for data_list in stock_data["priceDict"]:
            row = self.ui.priceTable.rowCount()
            self.ui.priceTable.setRowCount(row + 1)
            self.add_table_row(row, data_list)

    def add_table_row(self, row, data_list):
        col = 0
        for item in data_list:
            cell = QtWidgets.QTableWidgetItem(item)
            self.ui.priceTable.setItem(row, col, cell)
            col += 1

    def set_stats(self, stock_data):
        self.ui.total.setText(str(self.stock_data["stats"]["total"]))
        self.ui.profit.setText(str(self.stock_data["stats"]["profit"]))
        self.ui.profit.setStyleSheet("color: green")
        self.ui.loss.setText(str(self.stock_data["stats"]["loss"]))
        self.ui.loss.setStyleSheet("color: red")
        self.ui.noChange.setText(str(self.stock_data["stats"]["noChg"]))
        self.ui.noChange.setStyleSheet("color: grey")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainDriver()
    w.show()
    sys.exit(app.exec_())
