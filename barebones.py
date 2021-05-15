from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWebEngine import *
from PyQt5.QtNetwork import *

import sys
import os


class MainWindow(QMainWindow):
    #defining the main window
    def __init__(self, url):
        super(MainWindow, self).__init__()

        self.progress = 0



        QNetworkProxyFactory.setUseSystemConfiguration(True)

        #loading definitions from below
        self.view = QWebEngineView(self)
        self.view.load(url)
        self.view.loadFinished.connect(self.adjustLocation)
        self.view.titleChanged.connect(self.adjustTitle)
        self.view.loadProgress.connect(self.setProgress)
        self.view.loadFinished.connect(self.finishLoading)

        self.locationEdit = QLineEdit(self)
        self.locationEdit.setSizePolicy(QSizePolicy.Expanding,
                self.locationEdit.sizePolicy().verticalPolicy())
        self.locationEdit.returnPressed.connect(self.changeLocation)
        #toolbar
        backslash_home = QAction(QIcon('logo_1.png'), 'BackS/ash', self)
        backslash_home.setShortcut('Ctrl+Q')
        backslash_home.triggered.connect(self.backslashhtml)

        toolBar = self.addToolBar("Navigation")
        toolBar.addAction(backslash_home)
        toolBar.addAction(self.view.pageAction(QWebEnginePage.Back))
        toolBar.addAction(self.view.pageAction(QWebEnginePage.Forward))
        toolBar.addAction(self.view.pageAction(QWebEnginePage.Reload))
        toolBar.addAction(self.view.pageAction(QWebEnginePage.Stop))
        toolBar.addWidget(self.locationEdit)

        #menu actions
        viewMenu = self.menuBar().addMenu("&View")
        viewSourceAction = QAction("Page Source", self)
        viewSourceAction.triggered.connect(self.viewSource)
        viewMenu.addAction(viewSourceAction)

        effectMenu = self.menuBar().addMenu("&Effect")
        effectMenu.addAction("Highlight all links", self.highlightAllLinks)

        self.rotateAction = QAction(
                self.style().standardIcon(QStyle.SP_FileDialogDetailedView),
                "Turn images upside down", self, checkable=True,
                toggled=self.rotateImages)
        effectMenu.addAction(self.rotateAction)

        toolsMenu = self.menuBar().addMenu("&Tools")
        toolsMenu.addAction("Remove GIF images", self.removeGifImages)
        toolsMenu.addAction("Remove all inline frames",
                self.removeInlineFrames)
        toolsMenu.addAction("Remove all object elements",
                self.removeObjectElements)
        toolsMenu.addAction("Remove all embedded elements",
                self.removeEmbeddedElements)
        self.setCentralWidget(self.view)

    def viewSource(self):
        accessManager = self.view.page().networkAccessManager()
        request = QNetworkRequest(self.view.url())
        reply = accessManager.get(request)
        reply.finished.connect(self.slotSourceDownloaded)

    def slotSourceDownloaded(self):
        reply = self.sender()
        self.textEdit = QTextEdit()
        self.textEdit.setAttribute(Qt.WA_DeleteOnClose)
        self.textEdit.show()
        self.textEdit.setPlainText(QTextStream(reply).readAll())
        self.textEdit.resize(600, 400)
        reply.deleteLater()

    def adjustLocation(self):
        self.locationEdit.setText(self.view.url().toString())

    def changeLocation(self):
        url = QUrl.fromUserInput(self.locationEdit.text())
        self.view.load(url)
        self.view.setFocus()

    def backslashhtml(self):
        url = QUrl.fromLocalFile(os.path.abspath('backslash.html'))
        self.view.load(url)
        self.view.setFocus()


    def adjustTitle(self):
        if 0 < self.progress < 100:
            self.setWindowTitle("%s (%s%%)" % (self.view.title(), self.progress))
        else:
            self.setWindowTitle(self.view.title())

    def setProgress(self, p):
        self.progress = p
        self.adjustTitle()

    def finishLoading(self):
        self.progress = 100
        self.adjustTitle()
        self.rotateImages(self.rotateAction.isChecked())

    def highlightAllLinks(self):
        code = """$('a').each(
                    function () {
                        $(this).css('background-color', 'yellow')
                    }
                  )"""


    def rotateImages(self, invert):
        if invert:
            code = """
                $('img').each(
                    function () {
                        $(this).css('-webkit-transition', '-webkit-transform 2s');
                        $(this).css('-webkit-transform', 'rotate(180deg)')
                    }
                )"""
        else:
            code = """
                $('img').each(
                    function () {
                        $(this).css('-webkit-transition', '-webkit-transform 2s');
                        $(this).css('-webkit-transform', 'rotate(0deg)')
                    }
                )"""



    def removeGifImages(self):
        code = "$('[src*=gif]').remove()"
        self.view.page().mainFrame().evaluateJavaScript(code)

    def removeInlineFrames(self):
        code = "$('iframe').remove()"
        self.view.page().mainFrame().evaluateJavaScript(code)

    def removeObjectElements(self):
        code = "$('object').remove()"
        self.view.page().mainFrame().evaluateJavaScript(code)

    def removeEmbeddedElements(self):
        code = "$('embed').remove()"
        self.view.page().mainFrame().evaluateJavaScript(code)


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)

    if len(sys.argv) > 1:
        url = QUrl(sys.argv[1])
    else:
        url = QUrl('https://www.duckduckgo.com')

    browser = MainWindow(url)
    browser.show()

    sys.exit(app.exec_())
