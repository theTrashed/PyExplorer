from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtWidgets import QVBoxLayout, QGridLayout, QScrollArea
from PyQt5.QtWidgets import QPushButton, QSizePolicy, QFrame, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

import sys
import os

from functools import partial

import directory as d


def resource_path(relative_path):
    if (hasattr(sys, '_MEIPASS')):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath(__file__), relative_path)


class MainWindow(QMainWindow):
    def __init__(self, listView=True):
        super().__init__()
        self.path = os.path.dirname(__file__)
        self.btns = []
        self.btn_count = len(self.btns)
        self.ascending = False
        self.sort = False
        self.showHidden = False
        self.listView = True

        self.initUI()

    def initUI(self):
        self.sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.main_widget = QWidget()
        self.main_widget.setSizePolicy(self.sizePolicy)
        if (self.listView):
            self.main_layout = QVBoxLayout()

            self.main_widget.setLayout(self.main_layout)

            dir_conts = d.get_dir_cont(sort=self.sort)
            self._generateFileItems(dir_conts, self.showHidden)

            self.scroll.setWidget(self.main_widget)
            self.setCentralWidget(self.scroll)

    def _generateFileItems(self, dir_conts, showHidden):
        for i in range(self.main_layout.count()):
            self.main_layout.itemAt(i).widget().deleteLater()

        del self.btns
        self.btns = []
        self.btn_count = 0

        for name, t in zip(dir_conts.keys(), dir_conts.values()):
            if ((not showHidden) and (name[0] == '.') and (name != '..')):
                continue
            else:
                self.btns.append(QPushButton())
                self.btn_count = len(self.btns)
                self.btns[self.btn_count - 1].setText(name)
                if (t == 'dir'):
                    self.btns[self.btn_count -
                              1].setIcon(QIcon(resource_path('images/folder.png')))
                else:
                    self.btns[self.btn_count -
                              1].setIcon(QIcon(resource_path('images/file.png')))
                self.btns[self.btn_count -
                          1].setStyleSheet('text-align: left;')
                self.btns[self.btn_count - 1].setFlat(True)
                self.btns[self.btn_count - 1].setSizePolicy(self.sizePolicy)
                self.btns[self.btn_count - 1].clicked.connect(
                    partial(self._clickHandle, self.btns[self.btn_count - 1], t))
                self.main_layout.addWidget(self.btns[self.btn_count - 1])
                separator = QFrame()
                separator.setFrameShape(QFrame.HLine)
                separator.setLineWidth(1)
                self.main_layout.addWidget(separator)

        self.main_widget.update()

    def _clickHandle(self, bt, t):
        if (t == 'file'):
            d.open_file(bt.text())
        else:
            txt = bt.text()
            try:
                dir_conts = d.get_dir_cont(txt, self.sort, self.ascending)
                self._generateFileItems(dir_conts, self.showHidden)
            except PermissionError:
                dialog = QMessageBox()
                dialog.setText('Failed to open directory/file.')
                dialog.setStyleSheet('text-align: center;')
                dialog.setStandardButtons(QMessageBox.Close)
                dialog.exec()

    def _generateToolBar(self):
        pass

    def _toggleHidden(self, dir_conts):
        self.showHidden = not self.showHidden
        self._generateFileItems(dir_conts, self.showHidden)

    def _toggleSort(self, dir_conts):
        self.sort = not self.sort
        dir_conts = d.sort_dir_list(dir_conts, r=self.ascending)
        self._generateFileItems(dir_conts, self.showHidden)

    def _toggleSortOrder(self, dir_conts):
        if self.sort:
            self.ascending = not self.ascending
            dir_conts = d.sort_dir_list(dir_conts, r=self.ascending)
            self._generateFileItems(dir_conts, self.showHidden)


def main():
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
