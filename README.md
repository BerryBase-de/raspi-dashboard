# Raspi-Dashboard
Ein Raspberry Pi e-ink Dashboard. Für das Dashboard werden Daten von der GitHub API, Dad Jokes API und der Twitter API abgerufen (und ein Bild von einem zufälligen Pokemon).


**Der Code funktioniert nur, wenn Twitter API Keys und Secrets eingetragen werden**.


Soll die Twitter-API nicht verwendet werden, müssen die entsprechenden Stellen im Code auskommentiert oder entfernt werden.
## Abhängigkeiten
Damit der Code läuft, werden folgende Abhängigkeiten benötigt (hier als Bsp. für Raspberry Pi OS, package manager entsprechend anpassen):
```shell
sudo apt-get install python3-pip
sudo apt-get install python3-numpy
sudo apt-get install python3-pil
pip3 install python-twitter
pip3 install Rpi.GPIO
pip3 install spidev
```
Für python-twitter bitte überprüfen, ob bereits eine andere Python Twitter Library installiert ist (manchmal bei Raspberry Pi OS).
Da es zu Namenskonflikten zwischen Twitter libraries kommen kann, entweder die bereits vorhandene statt python-twitter nutzen oder deinstallieren.

## Twitter-API
Bis auf die Twitter-API sind alle API-Zugriffe ohne Anmeldung und Keys möglich.
**Für die Twitter-API ist ein Twitter-Account und ein Twitter-Developer-Account nötig**.
Einen Twitter Developer Account bekommt man recht einfach auf der [Twitter Developer Seite](https://developer.twitter.com/en/), manchmal dauert es etwas, bis der Developer Account freigeschaltet wird.
Im Developer Portal wird dann eine App für das Raspberry Pi Dashboard registriert (als Name z.B. einfach Raspi-Dashboard).
Falls angegeben werden muss, wie die Twitter API für dieses Projekt verwendet wird, etwas in die Richtung:
>I want to get the newest Tweets from my favorite news accounts to use them for a personal project.
>My project is a dashboard that uses a Raspberry Pi and an e-ink display to show the latest news.

Die Namen der Keys der Twitter API v2 stimmen nicht exakt mit den Namen in der Python library überein.
Hier die Entsprechungen:
- API Key = consumer_key
- API Key Secret = consumer_secret


access_token_key und access_token_secret werden im Twitter Developer Portal in den Einstellungen der App -> Keys and Tokens generiert.

