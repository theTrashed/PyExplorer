# Importing classes required for the building of the GUI
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtWidgets import QVBoxLayout, QGridLayout, QScrollArea
from PyQt5.QtWidgets import QPushButton, QSizePolicy, QFrame, QMessageBox
from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QObjectCleanupHandler, QSize

# Importing helper libraries
import sys
import os
from functools import partial

# Importing user defined library that retrieves directory content
import directory as d


class MainWindow(QMainWindow):
    def __init__(self):
        # Some basic initialisations
        super().__init__()
        self.path = os.path.dirname(__file__)
        self.btns = []
        self.btnCount = 0
        self.notAscending = False
        self.sort = True
        self.showHidden = True
        self.listView = False
        self.gridMaxLineLen = 16
        self.wrappingChars = ('-', '_', '.', '?', ' ', '&')
        self.listSizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.gridSizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.initUI()

    def initUI(self):
        # Initial geometry of the window
        self.setGeometry(300, 250, 600, 450)
        self.setFont(QFont('Monospace'))

        # Set a ScrollArea that allows scrolling of the main interface
        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.main_widget = QWidget()
        # Set SizePolicy on the basis of listView or gridView
        if (self.listView):
            dir_conts = d.get_dir_cont(sort=self.sort)
            self._generateFileItems(dir_conts)

            self.scroll.setWidget(self.main_widget)
            self.setCentralWidget(self.scroll)
        else:
            self.rows = 0
            self.columns = 0
            self.maxCols = 5

            dir_conts = d.get_dir_cont(sort=self.sort)
            self._generateFileItems(dir_conts)

            self.scroll.setWidget(self.main_widget)
            self.setCentralWidget(self.scroll)

    def _generateFileItems(self, dir_conts):
        # Function to generate the view, with toolbar
        self._generateToolBar(dir_conts)
        if (self.listView):
            self.main_widget.setSizePolicy(self.listSizePolicy)
            self._generateListView(dir_conts)
        else:
            self.main_widget.setSizePolicy(self.gridSizePolicy)
            self._generateGridView(dir_conts)
        self.main_widget.update()

    def _clickHandle(self, name, t):
        # If the button clicked is a file, open the file
        # Else, retrieve new directory contents and refresh view
        if (t == 'file'):
            d.open_file(name)
        else:
            try:
                dir_conts = d.get_dir_cont(name, self.sort, self.notAscending)
                self._generateToolBar(dir_conts)
                self._generateFileItems(dir_conts)
            # If unable to open directory, display pop-up box
            except PermissionError:
                dialog = QMessageBox()
                dialog.setText('Failed to open directory/file.')
                dialog.setStyleSheet('text-align: center;')
                dialog.setStandardButtons(QMessageBox.Close)
                dialog.exec()

    def _generateToolBar(self, dir_conts):
        # If toolbar already exists, clear its contents and delete it
        if (hasattr(self, 'toolbar')):
            self.toolbar.clear()
            self.toolbar.setParent(None)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Define new actions and connect them to their respective functions
        sortAct = QAction('Sort', self)
        sortAct.setShortcut('Ctrl+S')
        sortAct.triggered.connect(partial(self._toggleSort, dir_conts))

        hiddenAct = QAction('Hidden', self)
        hiddenAct.setShortcut('Ctrl+H')
        hiddenAct.triggered.connect(partial(self._toggleHidden, dir_conts))

        viewAct = QAction('View', self)
        viewAct.setShortcut('Ctrl+L')
        viewAct.triggered.connect(partial(self._toggleView, dir_conts))

        # Add the actions to the toolbar
        self.toolbar = self.addToolBar('toolbar')
        self.toolbar.setMovable(False)
        self.toolbar.addWidget(spacer)
        self.toolbar.addAction(viewAct)
        self.toolbar.addAction(hiddenAct)
        self.toolbar.addAction(sortAct)
        if (self.sort):
            ascendingAct = QAction('Ascending', self)
            ascendingAct.setShortcut('Ctrl+A')
            ascendingAct.triggered.connect(
                partial(self._toggleAscending, dir_conts))
            self.toolbar.addAction(ascendingAct)

    def _toggleHidden(self, dir_conts):
        # Toggles the visibility of hidden files (file/dir names starting with
        # a '.')
        self.showHidden = not self.showHidden
        self._generateFileItems(dir_conts)

    def _toggleSort(self, dir_conts):
        # Toggles whether the items of the directory will be sorted or not
        self.sort = not self.sort
        dir_conts = d.sort_dir_list(dir_conts, r=self.notAscending)
        self._generateFileItems(dir_conts)

    def _toggleAscending(self, dir_conts):
        # If sorting is turned on, changes the sort order between ascending,
        # or descending
        if (self.sort):
            self.notAscending = not self.notAscending
            dir_conts = d.sort_dir_list(dir_conts, r=self.notAscending)
            self._generateFileItems(dir_conts)

    def _toggleView(self, dir_conts):
        # Toggles the view from listView to gridView
        self.listView = not self.listView
        self._generateFileItems(dir_conts)

    def _deleteLayout(self):
        if (hasattr(self, 'main_layout')):
            if (type(self.main_layout) is QVBoxLayout):
                for i in range(self.main_layout.count()):
                    self.main_layout.itemAt(i).widget().deleteLater()
            else:
                for i in range(self.btnCount):
                    self.main_layout.removeWidget(self.btns[i])
                    self.btns[i].deleteLater()
            QObjectCleanupHandler().add(self.main_layout)

    def _generateListView(self, dir_conts):
        # Delete a layout if a previous one exists
        self._deleteLayout()

        self.main_layout = QVBoxLayout()
        self.main_widget.setLayout(self.main_layout)

        del self.btns
        self.btns = []
        self.btnCount = 0

        # Sets the window title as the directory, loops over contents of entire
        # directory, generates buttons, adds icons, stylesheets, text to the
        # buttons and generates a list view
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
                    partial(self._clickHandle, name, t))
                self.main_layout.addWidget(self.btns[self.btnCount - 1])
                separator = QFrame()
                separator.setFrameShape(QFrame.HLine)
                separator.setLineWidth(1)
                self.main_layout.addWidget(separator)

        self.scroll.verticalScrollBar().setValue(
            self.scroll.verticalScrollBar().minimum())
        self.main_widget.update()

    def _generateGridView(self, dir_conts):
        # Delete a layout if a previous one exists
        self._deleteLayout()

        self.main_layout = QGridLayout()
        self.main_widget.setLayout(self.main_layout)
        self.main_layout.activate()
        del self.btns
        self.rows = 0
        self.columns = 0
        self.btnCount = 0
        self.btns = []

        # Sets the window title as the directory, loops over contents of entire
        # directory, generates buttons, adds icons, stylesheets, text to the
        # buttons and generates a grid view
        self.setWindowTitle(os.getcwd())
        for name, t in zip(dir_conts.keys(), dir_conts.values()):
            if ((not self.showHidden) and (name[0] == '.') and (name != '..')):
                continue
            else:
                self.btns.append(QPushButton())
                self.btnCount = len(self.btns)
                self.btns[self.btnCount - 1].setText(self._wordWrap(name))
                if (t == 'dir'):
                    self.btns[self.btnCount - 1].setObjectName('dir')
                else:
                    self.btns[self.btnCount - 1].setObjectName('file')

                # Setting images as background for the button
                self.btns[self.btnCount - 1].setStyleSheet(
                    'QPushbutton {\n'
                    'text-align: center;\n'
                    'padding: -25px 0 10px 0;\n'
                    'border: 1px solid black;\n'
                    'border-radius: 2px;\n'
                    'opacity: 0.5;\n'
                    '}\n'
                    '#dir {\n'
                    f'background-image: url("{os.path.join(self.path, "images/folder.png")}");\n'
                    'background-repeat: no-repeat;\n'
                    'background-position: center top;\n'
                    'background-origin: content;\n'
                    'background-color: rgba(255, 255, 255, 90);\n'
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
                self.btns[self.btnCount - 1].setFixedSize(QSize(150, 150))
                self.btns[self.btnCount - 1].setSizePolicy(self.gridSizePolicy)
                self.btns[self.btnCount - 1].clicked.connect(
                    partial(self._clickHandle, name, t))
                self.main_layout.addWidget(self.btns[self.btnCount - 1],
                                           self.rows, self.columns)
                self.columns += 1
                # If number of number of buttons in row == max number of cols,
                # move to next row
                if ((self.columns % self.maxCols) == 0):
                    self.columns = 0
                    self.rows += 1
        self.scroll.verticalScrollBar().setValue(
            self.scroll.verticalScrollBar().minimum())
        self.main_widget.update()

    def _wordWrap(self, text):

        newText = ''
        rows = 1
        for i, char in enumerate(text):
            if (((i % self.gridMaxLineLen) == 0) and (i != 0)):
                if (char not in self.wrappingChars):
                    for c in reversed(newText):
                        if (c not in self.wrappingChars):
                            continue

                        j = newText[::-1].index(c)
                        rows += 1
                        if (rows > 3):
                            return newText[:len(newText) - j] + '...'
                        newText = newText[:len(newText) - j] + \
                            '\n' + \
                            newText[len(newText) - j:]
                        break
            newText += char

        return newText


def main():
    app = QApplication.instance()
    if (not app):
        app = QApplication(sys.argv)

    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())


if (__name__ == '__main__'):
    main()
