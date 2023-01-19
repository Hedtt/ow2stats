from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton


class InvalidUserName(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel('Error, invalid username')
        self.redoButton = QPushButton('Input username')
        self.redoButton.clicked.connect(self.closeThis)
        layout.addStretch()
        layout.addWidget(self.label)
        layout.addWidget(self.redoButton)
        layout.addStretch()
        self.setLayout(layout)

    def closeThis(self):
        self.close()

