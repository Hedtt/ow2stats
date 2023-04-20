import sys
from PyQt5.QtCore import QFile, QTextStream, Qt
import PyQt5
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QApplication, QLabel, QStyle
# import breeze_resources
from widgetGallery import *
from enums import Enum
from game import *
import version

from player import *

# connect to google docs
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
import os

creds = 'uselessFolderINeedBecauseOfWindoof.json'


scope = ["https://www.googleapis.com/auth/spreadsheets.readonly",
         "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.readonly",
         "https://www.googleapis.com/auth/drive"]

sa = gspread.service_account(filename='uselessFolderINeedBecauseOfWindoof/creds.json')
# sh = sa.open('ow2stats')
#
# wks = sh.worksheet('data')

if __name__ == '__main__':
    version.CheckVersion()
    app = QApplication([])
    app.setStyle('Fusion')
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.black)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)
    gallery = WidgetGallery()
    gallery.show()
    # doc = GDoc()
    # game = doc.openLastGame()
    app.exec_()
