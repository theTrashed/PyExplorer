from PyQt5.QtGui import QPalette, QColor


class DarkPalette(QPalette):
    def __init__(self, *__args):
        super().__init__(*__args)

        self.setColor(QPalette.Window, QColor(0x2e, 0x34, 0x40))
        self.setColor(QPalette.WindowText, QColor(0xe5, 0xe9, 0xf0))
        self.setColor(QPalette.Base, QColor(0x2e, 0x34, 0x40))
        self.setColor(QPalette.Text, QColor(0xe5, 0xe9, 0xf0))
        self.setColor(QPalette.Button, QColor(0x3b, 0x42, 0x52))
        self.setColor(QPalette.ButtonText, QColor(0xe5, 0xe9, 0xf0))
        self.setColor(QPalette.BrightText, QColor(0xec, 0xef, 0xf4))
        self.setColor(QPalette.Link, QColor(0x5e, 0x81, 0xac))
        self.setColor(QPalette.Highlight, QColor(0x5e, 0x81, 0xac))
        self.setColor(QPalette.HighlightedText, QColor(0xec, 0xef, 0xf4))
