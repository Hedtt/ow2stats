import requests
import subprocess
import urllib.request
import os


def CheckVersion():
    r = requests.get('https://raw.githubusercontent.com/Hedtt/ow2stats/main/setup/version')
    if r.text > open('setup/version').read():
        UpdateApplication()


def UpdateApplication():
    url = 'https://github.com/Hedtt/ow2stats/blob/main/setup/mysetup.exe?raw=true'
    f = urllib.request.urlopen(url)
    file = f.read()
    f.close()
    f2 = open('mysetup.exe', 'wb')
    f2.write(file)
    f2.close()
    subprocess.call('mysetup.exe')
