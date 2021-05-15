from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWebEngine import *
from PyQt5.QtNetwork import *

import sys
import os


class UrlInput(QLineEdit):
    def __init__(self, browser):
        super(UrlInput, self).__init__()
        self.browser = browser
        # add event listener on "enter" pressed
        self.returnPressed.connect(self._return_pressed)

    def _return_pressed(self):
        url = QUrl(self.text())
        # load url into browser frame
        browser.load(url)
class RequestsTable(QTableWidget):
    header = ["Url", "Status", "Content-Type"]

    def __init__(self):
        super(RequestsTable, self).__init__()
        self.setColumnCount(3)
        self.setHorizontalHeaderLabels(self.header)
        header = self.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(QHeaderView.ResizeToContents)

    def update(self, data):
        last_row = self.rowCount()
        next_row = last_row + 1
        self.setRowCount(next_row)
        for col, dat in enumerate(data, 0):
            if not dat:
                continue
            self.setItem(last_row, col, QTableWidgetItem(dat))



if __name__ == "__main__":
    app = QApplication(sys.argv)

    grid = QGridLayout()
    browser = QWebEngineView()
    url_input = UrlInput(browser)
    requests_table = RequestsTable()



    # to tell browser to use network access manager
    # you need to create instance of QWebEnginePage
    page = QWebEnginePage()
    browser.setPage(page)
    action_box = ActionInputBox(page)

    grid.addWidget(url_input, 1, 0)
    grid.addWidget(action_box, 2, 0)
    grid.addWidget(browser, 3, 0)
    grid.addWidget(requests_table, 4, 0)


    main_frame = QWidget()
    main_frame.setLayout(grid)
    main_frame.setWindowTitle("BackS/ash")
    main_frame.setWindowIcon(QIcon('icon.png'))
    main_frame.show()

    sys.exit(app.exec_())
