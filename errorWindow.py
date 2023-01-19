from PyQt5.QtWidgets import QVBoxLayout, QWidget, QLabel, QPushButton


class ErrorWindow(QWidget):
    def __init__(self, error_text: str):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel(error_text)
        self.redoButton = QPushButton('Input missing things')
        self.redoButton.clicked.connect(self.closeThis)
        layout.addStretch()
        layout.addWidget(self.label)
        layout.addWidget(self.redoButton)
        layout.addStretch()
        self.setLayout(layout)

    def closeThis(self):
        self.close()



