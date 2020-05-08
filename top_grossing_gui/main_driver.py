import sys
from PyQt5 import QtWidgets, QtGui
from main_ui import Ui_AppMainWindow
from PyQt5 import QtCore as qtc
import nse_driver
import time


class Worker(qtc.QObject):
    fetch_completed = qtc.pyqtSignal(dict)

    @qtc.pyqtSlot(bool)
    def call_api(self, fetch_flag):
        while fetch_flag:
            print("Fetching")
            self.fetch_completed.emit(nse_driver.start_fetch())
            time.sleep(60)


class MainDriver(QtWidgets.QMainWindow):
    fetch_flag = True
    fetch_requested = qtc.pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.stock_data = nse_driver.start_fetch()
        self.ui = Ui_AppMainWindow()
        self.setWindowIcon(QtGui.QIcon("./icon.png"))
        self.ui.setupUi(self)
        self.ui.startFetch.released.connect(self.fetch_results)
        self.ui.stopFetch.clicked.connect(self.change_flag)

        self.worker = Worker()
        self.worker_thread = qtc.QThread()
        self.worker.fetch_completed.connect(self.set_table)
        self.worker.fetch_completed.connect(self.set_stats)
        self.fetch_requested.connect(self.worker.call_api)
        self.worker.moveToThread(self.worker_thread)
        self.worker_thread.start()

        self.show()

    def change_flag(self):
        self.fetch_requested.emit(False)

    def add_table_row(self, row, data_list):
        col = 0
        for item in data_list:
            cell = QtWidgets.QTableWidgetItem(item)
            self.ui.priceTable.setItem(row, col, cell)
            col += 1

    def set_table(self, stock_data):
        self.ui.priceTable.setRowCount(0)
        self.ui.priceTable.setColumnCount(8)
        for data_list in stock_data["priceDict"]:
            row = self.ui.priceTable.rowCount()
            self.ui.priceTable.setRowCount(row + 1)
            self.add_table_row(row, data_list)

    def fetch_results(self):
        self.fetch_requested.emit(self.fetch_flag)
        # time.sleep(30)

    def set_stats(self, stock_data):
        self.ui.total.setText(str(self.stock_data["stats"]["total"]))
        self.ui.profit.setText(str(self.stock_data["stats"]["profit"]))
        self.ui.loss.setText(str(self.stock_data["stats"]["loss"]))
        self.ui.noChange.setText(str(self.stock_data["stats"]["noChg"]))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainDriver()
    w.show()
    sys.exit(app.exec_())
