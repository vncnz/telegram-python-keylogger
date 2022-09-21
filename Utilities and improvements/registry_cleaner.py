
import winreg

def removeChatId():
  REG_PATH = 'WINEXPLORER_CH'
  try:
    registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_ALL_ACCESS)
    # winreg.DeleteKey(registry_key, NAME)
    winreg.DeleteKey(registry_key, "")
    winreg.CloseKey(registry_key)
  except WindowsError as ex:
    return None

def removeAutostart ():
  REG_PATH = 'HKCU\Software\Microsoft\Windows\CurrentVersion\Run'
  NAME = 'winexplorer'
  try:
    registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_ALL_ACCESS)
    winreg.DeleteKey(registry_key, NAME)
    # winreg.DeleteKey(registry_key, "")
    winreg.CloseKey(registry_key)
  except WindowsError as ex:
    return None

if __name__ == '__main__':
  removeAutostart()
  removeChatId()