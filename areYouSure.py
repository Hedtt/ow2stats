from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout

from WidgetGallery import WidgetGallery


class AreYouSure(QWidget):
    def __init__(self, widget_gallery: WidgetGallery):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel('Are you sure? Current inputs are being deleted')
        self.openLast = QPushButton('Yes, open last game')
        self.undo = QPushButton('No, go back')
        self.openLast.clicked.connect(self.closeThis)
        self.openLast.clicked.connect(lambda: WidgetGallery.openLastClicked(self=widget_gallery, confirmed=True))
        self.undo.clicked.connect(self.closeThis)

        label_layout = QHBoxLayout()
        label_layout.addStretch()
        label_layout.addWidget(self.label)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.openLast)
        button_layout.addStretch()
        button_layout.addWidget(self.undo)
        button_layout.addStretch()

        layout.addLayout(label_layout)
        layout.addLayout(button_layout)
        self.setLayout(layout)

    def closeThis(self):
        self.close()
