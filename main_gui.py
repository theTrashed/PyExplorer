from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtWidgets import QVBoxLayout, QGridLayout
from PyQt5.QtWidgets import QPushButton, QSizePolicy, QFrame
from PyQt5.QtGui import QIcon

from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtCore import Qt

import sys

from functools import partial

import directory as d


class MainWindow(QMainWindow):
    def __init__(self, listView=True):
        super().__init__()
        self.btns = []
        self.btn_count = len(self.btns)

        self.initUI(listView, showHidden=True)

    def initUI(self, listView, showHidden=False):
        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        if (listView):
            self.main_widget = QWidget()
            self.main_layout = QVBoxLayout()

            self.main_widget.setLayout(self.main_layout)
            sizePolicy = QSizePolicy(QSizePolicy.Expanding,
                                     QSizePolicy.Expanding)

            dir_conts = d.get_dir_cont(sort=True)
            for name, t in zip(dir_conts.keys(), dir_conts.values()):
                if ((not showHidden) and (name[0] == '.')):
                    continue
                else:
                    self.btns.append(QPushButton(f'button{self.btn_count}'))
                    self.btn_count = len(self.btns)
                    print(self.btn_count)
                    index = self.btn_count
                    self.btns[index - 1].setText(name)
                    if (t == 'dir'):
                        self.btns[index- 1].setStyleSheet('color: rgba(0,0,0,100);')
                    else:
                        pass
                    self.btns[index - 1].setStyleSheet('text-align: left;')
                    self.btns[index - 1].setFlat(True)
                    self.btns[index - 1].setSizePolicy(sizePolicy)
                    self.btns[index - 1].clicked.connect(partial(self._clickHandle, self.btns[index - 1]))
                    self.main_layout.addWidget(self.btns[index - 1])
                    print(index)
                    separator = QFrame()
                    separator.setFrameShape(QFrame.HLine)
                    separator.setLineWidth(1)
                    self.main_layout.addWidget(separator)

            del dir_conts
            self.scroll.setWidget(self.main_widget)
            self.setCentralWidget(self.scroll)

    def _clickHandle(self, bt):
        d.open_file(bt.text())
#        txt = btn.text()
#        dir_conts = d.get_dir_cont(txt, self.sort, self.ascending)
#
#        for name, t in zip(dir_conts.keys(), dir_conts.values()):
#            print(name[0], t)
#            if ((not self.showHidden) and (name[0] == '.')):
#                continue
#            else:
#                btn = QPushButton()
#                btn.setText(name)
#                if (t == 'dir'):
#                    btn.setIcon(QIcon('./images/folder.png'))
#                else:
#                    pass
#                btn.clicked.connect(lambda: self._clickHandle(btn))
#                self.main_layout.addWidget(btn)


def main():
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
