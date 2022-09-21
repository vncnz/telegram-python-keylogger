import base64
import sys, os

from shutil import copyfile
from time import sleep

bytes = None
finalpath = 'V:/Progetto Sicurezza/dist/test_lettura_scrittura_copy.exe'

if not 'test_lettura_scrittura_copy.exe' in sys.executable:
  copyfile(sys.executable, finalpath)

  with open('V:/Progetto Sicurezza/dist/88794_1.pdf', 'rb') as f:
    bytes = f.read()
    #bytes = bytes.encode('ascii')
    #encoded = base64.encode(bytes)
    #encoded = encoded.decode('ascii')
    # print(bytes)

  with open('V:/Progetto Sicurezza/dist/88794_1_COPY.pdf', 'wb') as f:
    f.write(bytes)

  os.system(f'"{finalpath}"')
  os.system('"V:/Progetto Sicurezza/dist/88794_1_COPY.pdf"')
  sys.exit(0)
  # sleep(1)

else:
  for i in range(10):
    print('Già fatto ' + str(i + 1))
    sleep(1)