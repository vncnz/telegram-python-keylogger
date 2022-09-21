import telegram
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater, CallbackQueryHandler
from functools import wraps
from telegram import ChatAction, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.error import (TelegramError, Unauthorized, BadRequest, TimedOut, ChatMigrated, NetworkError)

from time import sleep
from threading import Thread

# from common import createLogger

# Per impostare la lista dei comandi possibili: https://stackoverflow.com/questions/34457568/how-to-show-options-in-telegram-bot

# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# logger = createLogger('telegram', ('_loglevel' in config) and config['_loglevel'].upper() or None)
# logger = createLogger('telegram', None)

token = 'A_TOKEN'
botname = 'A_BOTNAME'

reply_markup_remove_keyboard = telegram.ReplyKeyboardRemove()

def send_typing_action(func):
  """Sends typing action"""

  @wraps(func)
  def command_func(self, update, context, *args, **kwargs):
    context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    return func(update, context,  *args, **kwargs)
  return command_func

def save_chat(func):
  """Save chat id"""

  @wraps(func)
  def command_func(self, update, context, *args, **kwargs):
    if update.message.chat_id != self.chatId:
      self.chatId = update.message.chat_id
    return func(update, context,  *args, **kwargs)
  return command_func


def error_callback(update, ctx, error):
  try:
      raise error
  except Unauthorized as ex:
    # logger.error('Telegram error: Unauthorized')
    pass
  except BadRequest as ex:
    # logger.error('Telegram error: BadRequest')
    pass
  except TimedOut as ex:
    # logger.error('Telegram error: TimedOut')
    pass
  except NetworkError as ex:
    # logger.error('Telegram error: NetworkError')
    pass
  except ChatMigrated as ex:
    # logger.error('Telegram error: ChatMigrated')
    pass
  except TelegramError as ex:
    # logger.error('Telegram error: unknown')
    pass

class Bot(object):
  def __init__(self, token):
    self.managerLink = None
    self.bot = telegram.Bot(token=token)
    self.updater = Updater(token=token)
    self.dispatcher = self.updater.dispatcher
    self.dispatcher.add_error_handler(error_callback)
    self.chatId = None # 212922257

    # intercept commands
    self.handlers = [
      CommandHandler('start', self.processaComandoStart),
      CommandHandler('silent', self.processaComandoSilent),
      CommandHandler('talk', self.processaComandoTalk),
      CommandHandler('kill', self.processaComandoKill),
      CommandHandler('sendtome', self.processaComandoSendToMe),
      CommandHandler('delete', self.processaComandoDelete)
    ]
    for handler in self.handlers:
      self.dispatcher.add_handler(handler)
    # self.dispatcher.add_handler(CommandHandler('delete', self.processaComando))

    # intercept normal messages
    self.text_handler = MessageHandler(Filters.text, self.processaMessaggio)
    self.dispatcher.add_handler(self.text_handler)

    # self.dispatcher.add_handler(MessageHandler(Filters.contact, self.processaContatto))

    # capture button selection
    # self.onOptionSelected_handler = CallbackQueryHandler(self.inlineKeyboardPressed) # , pattern="__opt__"
    # self.dispatcher.add_handler(self.onOptionSelected_handler)

    self.printBotInfo()

  def run (self):
    self.updater.start_polling()
    # self.updater.idle()
  
  def shutdown(self):
    for handler in self.handlers:
      self.dispatcher.remove_handler(handler)
    self.dispatcher.remove_error_handler(error_callback)
    self.updater.stop()
    self.updater.is_idle = False

  def kill (self):
    Thread(target=self.shutdown).start()
  
  def printBotInfo (self):
    pass
    # print(self.bot.get_me())

  # def inlineKeyboardPressed(self, update, ctx):

  #   try:
  #     query = update.callback_query
  #     logger.warning('Azione su tastiera inline, ricevuto ' + query.data)
  #     # reply_markup = telegram.ReplyKeyboardRemove()
  #     data = query.data.split('&&&')

  #     buttonresult = int(data[0])
  #     # bot.send_chat_action(chat_id=query.message.chat.id, action=ChatAction.TYPING)
  #     logger.warning('Chiedo al server la reazione per {qdata}, sid {sid}, buttonresult {buttonresult}'.format(qdata=query.data, sid=query.message.message_id, buttonresult=buttonresult))

  #     response = sendAndReceive({
  #       'fromaddress': query.message.chat.id,
  #       'toaddress': botname,
  #       'body': '',
  #       'sid': query.message.message_id,
  #       'buttonresult': buttonresult
  #     }, path = config['pathtelegram'] + '/message')

  #     logger.warning('Il server ha risposto con status {status}, body {body}'.format(status=response.get('status'), body=response.get('body')))

  #     if response.get('status') == 'mcOk':
  #       query.edit_message_text(text = response.get('body') or "(" + data[1] + ')' )
  #     else:
  #       query.edit_message_text(text = 'Si è verificato un problema nell\'invio della risposta')
  #   except Exception as ex:
  #     logger.error(ex.args)

  def processaMessaggio(self, update, ctx):
    if self.chatId != update.message.chat_id: return
    update.message.reply_text("Comando o messaggio non compreso: " + update.message.text)

  # @send_typing_action
  def processaComando(self, update, ctx):
    if self.chatId != update.message.chat_id: return
    update.message.reply_text("Comando ricevuto (ma non implementato): " + update.message.text)

  def processaComandoSendToMe(self, update, ctx):
    if self.chatId != update.message.chat_id:
      self.chatId = update.message.chat_id
      update.message.reply_text("Comunicazioni attivate verso questa chat")
      if self.managerLink:
        self.managerLink.saveChatId(self.chatId)
    else:
      update.message.reply_text("Comunicazioni già attive verso questa chat")

  def processaComandoStart(self, update, ctx):
    pass

  # @send_typing_action
  def processaComandoKill (self, update, ctx):
    if self.chatId != update.message.chat_id: return
    # update.message.reply_text("Chiusura in corso")
    if self.managerLink:
      self.managerLink.kill()
    else:
      self.kill()
    exit(0)
  
  def processaComandoDelete (self, update, ctx):
    if self.chatId != update.message.chat_id: return
    if self.managerLink:
      if self.managerLink.checkAndRemove():
        update.message.reply_text("Codice rimosso da autostart e file system")
      else:
        update.message.reply_text("Codice NON rimosso")
  
  def processaComandoSilent(self, update, ctx):
    if self.chatId != update.message.chat_id: return
    if self.managerLink:
      if not self.managerLink.setStatus('silent'):
        update.message.reply_text("Cambio stato non consentito")
  
  def processaComandoTalk(self, update, ctx):
    if self.chatId != update.message.chat_id: return
    if self.managerLink:
      if not self.managerLink.setStatus('running'):
        update.message.reply_text("Cambio stato non consentito")
  
  # bot.send_message(chat_id=update.message.chat.id, text='Non mi serve un contatto', reply_markup = reply_markup_remove_keyboard)

  # def echo(self, update, ctx):
  #   reply_markup = telegram.ReplyKeyboardRemove()
  #   kb = []
  #   reply_markup = telegram.ReplyKeyboardMarkup(kb)
  #   pprint(update.message.__dict__)
  #   bot.send_message(chat_id=update.message.chat_id, text=update.message.text)
  
  # bot.send_message(chat_id=update.message.chat_id, text="Ciao! Sono una procedura automatica di registrazione. Ho bisogno di identificarti", reply_markup=reply_markup)
  
  ### DA QUI METODI NON PER TELEGRAM DIRETTAMENTE ###
  
  def sendMessage(self, chatId, msg, reply_markup=None):
    if not chatId:
      chatId = self.chatId
    if not chatId:
      # raise 'No chat known'
      return False
    return self.bot.send_message(chat_id=chatId, text=msg, reply_markup=reply_markup)
  
  def sendImage(self, chatId, path):
    if not chatId:
      chatId = self.chatId
    if not chatId:
      # raise 'No chat known'
      return False
    with open(path, 'rb') as f:
      return self.bot.send_photo(chat_id=chatId, photo=f)
  
  def deleteMessage(self, chatId, messageId):
    return self.bot.delete_message(chat_id=chatId, message_id=messageId)

if __name__ == '__main__':
  bot = Bot(token)
  #bot = Bot(token)
  bot.run()
  # print('Bot acceso')
  sleep(120)
  bot.kill()
  # print('Bot spento')
else:
  pass
  # print('Modulo telegram importato')