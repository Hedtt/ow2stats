import requests
import subprocess
import urllib.request
import os
import tkinter.messagebox as messagebox


def CheckVersion():
    r = requests.get('https://raw.githubusercontent.com/Hedtt/ow2stats/main/setup/version')
    if r.text > open('setup/version').read():
        UpdateApplication(r.text)


def UpdateApplication(version):
    url = 'https://github.com/Hedtt/ow2stats/blob/main/setup/Output/ow2stats_setup.exe?raw=true'
    f = urllib.request.urlopen(url)
    file = f.read()
    f.close()
    f2 = open('setup//Output/mysetup.exe', 'wb')
    f2.write(file)
    f2.close()
