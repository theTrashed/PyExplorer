from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtWidgets import QVBoxLayout, QGridLayout, QScrollArea
from PyQt5.QtWidgets import QPushButton, QSizePolicy, QFrame, QMessageBox
from PyQt5.QtWidgets import QAction, QToolBar
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QTimeLine, QObjectCleanupHandler

import sys
import os

from functools import partial

import directory as d


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.path = os.path.dirname(__file__)
        self.btns = []
        self.btnCount = 0
        self.notAscending = False
        self.sort = True
        self.showHidden = True
        self.listView = False
        self.listSizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.gridSizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.initUI()

    def initUI(self):
        self.setGeometry(300, 250, 600, 450)
        self.setFont(QFont('Monospace'))

        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.main_widget = QWidget()
        if (self.listView):
            self.main_widget.setSizePolicy(self.listSizePolicy)

            dir_conts = d.get_dir_cont(sort=self.sort)
            self._generateFileItems(dir_conts)

            self.scroll.setWidget(self.main_widget)
            self.setCentralWidget(self.scroll)
        else:
            self.main_widget.setSizePolicy(self.gridSizePolicy)

            self.rows = 0
            self.columns = 0
            self.maxCols = 5

            dir_conts = d.get_dir_cont(sort=self.sort)
            self._generateFileItems(dir_conts)

            self.scroll.setWidget(self.main_widget)
            self.setCentralWidget(self.scroll)

    def _generateFileItems(self, dir_conts):
        self._generateToolBar(dir_conts)
        if (self.listView):
            self._generateListView(dir_conts)
        else:
            self._generateGridView(dir_conts)
        self.main_widget.update()

    def _clickHandle(self, bt, t):
        if (t == 'file'):
            d.open_file(bt.text().lstrip())
        else:
            txt = bt.text().lstrip()
            try:
                dir_conts = d.get_dir_cont(txt, self.sort, self.notAscending)
                self._generateToolBar(dir_conts)
                self._generateFileItems(dir_conts)
            except PermissionError:
                dialog = QMessageBox()
                dialog.setText('Failed to open directory/file.')
                dialog.setStyleSheet('text-align: center;')
                dialog.setStandardButtons(QMessageBox.Close)
                dialog.exec()

    def _generateToolBar(self, dir_conts):
        if hasattr(self, 'toolbar'):
            self.toolbar.clear()
            self.toolbar.setParent(None)

        sortAct = QAction('Sort', self)
        sortAct.setShortcut('Ctrl+S')
        sortAct.triggered.connect(partial(self._toggleSort, dir_conts))

        hiddenAct = QAction('Hidden', self)
        hiddenAct.setShortcut('Ctrl+H')
        hiddenAct.triggered.connect(partial(self._toggleHidden, dir_conts))

        self.toolbar = self.addToolBar('toolbar')
        self.toolbar.setMovable(False)
        self.toolbar.addAction(sortAct)
        self.toolbar.addAction(hiddenAct)
        if self.sort:
            ascendingAct = QAction('Ascending', self)
            ascendingAct.setShortcut('Ctrl+A')
            ascendingAct.triggered.connect(
                partial(self._toggleAscending, dir_conts))
            self.toolbar.addAction(ascendingAct)

    def _toggleHidden(self, dir_conts):
        self.showHidden = not self.showHidden
        self._generateFileItems(dir_conts)

    def _toggleSort(self, dir_conts):
        self.sort = not self.sort
        dir_conts = d.sort_dir_list(dir_conts, r=self.notAscending)
        self._generateFileItems(dir_conts)

    def _toggleAscending(self, dir_conts):
        if self.sort:
            self.notAscending = not self.notAscending
            dir_conts = d.sort_dir_list(dir_conts, r=self.notAscending)
            self._generateFileItems(dir_conts)

    def _generateListView(self, dir_conts):
        for i in range(self.main_layout.count()):
            self.main_layout.itemAt(i).widget().deleteLater()

        try:
            QObjectCleanupHandler().add(self.main_layout)
        except AttributeError:
            pass
        self.main_layout = QVBoxLayout()
        self.main_widget.setLayout(self.main_layout)

        del self.btns
        self.btns = []
        self.btnCount = 0

        self.setWindowTitle(os.getcwd())
        for name, t in zip(dir_conts.keys(), dir_conts.values()):
            if ((not self.showHidden) and (name[0] == '.') and (name != '..')):
                continue
            else:
                self.btns.append(QPushButton())
                self.btnCount = len(self.btns)
                self.btns[self.btnCount - 1].setText('\t' + name)
                if (t == 'dir'):
                    self.btns[self.btnCount -
                                1].setIcon(QIcon(os.path.join(self.path, 'images/folder.png')))
                else:
                    self.btns[self.btnCount -
                                1].setIcon(QIcon(os.path.join(self.path, 'images/file.png')))
                self.btns[self.btnCount -
                            1].setStyleSheet('text-align: left;')
                self.btns[self.btnCount - 1].setFlat(True)
                self.btns[self.btnCount - 1].setSizePolicy(self.listSizePolicy)
                self.btns[self.btnCount - 1].clicked.connect(
                    partial(self._clickHandle, self.btns[self.btnCount - 1], t))
                self.main_layout.addWidget(self.btns[self.btnCount - 1])
                separator = QFrame()
                separator.setFrameShape(QFrame.HLine)
                separator.setLineWidth(1)
                self.main_layout.addWidget(separator)

        self.scroll.verticalScrollBar().setValue(
            self.scroll.verticalScrollBar().minimum())
        self.main_widget.update()

    def _generateGridView(self, dir_conts):
        for i in range(self.btnCount):
            self.main_layout.removeWidget(self.btns[i])
            self.btns[i].deleteLater()

        try:
            QObjectCleanupHandler().add(self.main_layout)
        except AttributeError:
            pass
        self.main_layout = QGridLayout()
        self.main_widget.setLayout(self.main_layout)
        self.main_layout.activate()
        del self.btns
        self.rows = 0
        self.columns = 0
        self.btnCount = 0
        self.btns = []

        self.setWindowTitle(os.getcwd())
        for name, t in zip(dir_conts.keys(), dir_conts.values()):
            if ((not self.showHidden) and (name[0] == '.') and (name != '..')):
                continue
            else:
                self.btns.append(QPushButton())
                self.btnCount = len(self.btns)
                self.btns[self.btnCount - 1].setText('\t' + name)
                if (t == 'dir'):
                    self.btns[self.btnCount - 1].setObjectName('dir')
                else:
                    self.btns[self.btnCount - 1].setObjectName('file')
                self.btns[self.btnCount - 1].setStyleSheet(
                    'QPushbutton {\n'
                    'text-align: center;\n'
                    'padding: -25px 0 10px 0;\n'
                    'border: 1px solid black;\n'
                    'border-radius: 2px;\n'
                    '}\n'
                    '#dir {\n'
                    f'background-image: url("{os.path.join(self.path, "images/folder.png")}");\n'
                    'background-repeat: no-repeat;\n'
                    'background-position: center top;\n'
                    'background-origin: content;\n'
                    '}\n'
                    '#file {\n'
                    f'background-image: url("{os.path.join(self.path, "images/file.png")}");\n'
                    'background-repeat: no-repeat;\n'
                    'background-position: center top;\n'
                    'background-origin: content;\n'
                    '}')
                self.btns[self.btnCount - 1].setMinimumWidth(100)
                self.btns[self.btnCount - 1].setMinimumHeight(100)
                self.btns[self.btnCount - 1].setFlat(True)
                self.btns[self.btnCount - 1].setSizePolicy(self.listSizePolicy)
                self.btns[self.btnCount - 1].clicked.connect(
                    partial(self._clickHandle, self.btns[self.btnCount - 1], t))
                self.main_layout.addWidget(self.btns[self.btnCount - 1],
                                            self.rows, self.columns)
                self.columns += 1
                if ((self.columns % self.maxCols) == 0):
                    self.columns = 0
                    self.rows += 1
        self.scroll.verticalScrollBar().setValue(
            self.scroll.verticalScrollBar().minimum())
        self.main_widget.update()


def main():
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)

    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
