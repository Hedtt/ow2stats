from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QMessageBox

def showConfirm():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)

    msg.setText("This will delete the current entries, are you sure?")
    msg.setWindowTitle("Confirm")
    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

    return msg.exec_()