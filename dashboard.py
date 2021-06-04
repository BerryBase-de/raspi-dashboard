import sys
import logging
import os
import json
import time
import datetime
import requests
import twitter
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps
from waveshare_epd import epd7in5b_HD

# Ordner für Bilder und Schriftarten
pic_dir  = 'pics'
font_dir = 'fonts'

# verschiedene Schriftarten fuer Ueberschriften, Text und Icons
heading            = ImageFont.truetype(os.path.join(font_dir, 'Roboto-Regular.ttf'), 24)
body               = ImageFont.truetype(os.path.join(font_dir, 'Roboto-Regular.ttf'), 18)
body_large         = ImageFont.truetype(os.path.join(font_dir, 'Roboto-Regular.ttf'), 62)
font_awesome       = ImageFont.truetype(os.path.join(font_dir, 'fontawesome-regular.ttf'), 18)
font_awesome_large = ImageFont.truetype(os.path.join(font_dir, 'fontawesome-regular.ttf'), 62)

# hier die API-Keys/Tokens fuer die Twitter-API eintragen
consumer_key        = 
consumer_secret     = 
access_token_key    = 
access_token_secret = 

api = twitter.Api(
    consumer_key = consumer_key,
    consumer_secret = consumer_secret,
    access_token_key = access_token_key,
    access_token_secret = access_token_secret
)

# neuesten Tweet eines Accounts holen
def get_latest_tweet(account):
    statuses = api.GetUserTimeline(screen_name=account)
    
    return statuses[0].text

# Funktion von Sandy von Pimoroni
# Fkt. passt 'text' auf Breite 'width' mit Schriftart 'font' an
def reflow_text(text, width, font):
    words = text.split(" ")
    reflowed = ' '
    line_length = 0

    for i in range(len(words)):
        word = words[i] + " "
        word_length = font.getsize(word) [0]
        line_length += word_length

        if line_length < width:
            reflowed += word
        else:
            line_length = word_length
            reflowed = reflowed[:-1] + "\n" + word

    return reflowed

# Dad Joke von Dad Joke API holen
# https://icanhazdadjoke.com/api
# hier wird kein API-Key benoetigt, 
def get_dad_joke():
    url = 'https://icanhazdadjoke.com/'
    headers = {'Accept':'application/json'}
    dad_joke = requests.get(url, headers=headers).json().get('joke')
    
    return str(dad_joke)

# GitHub Stars fuer ein Repo holen
# fuer diese Fkt. der GitHub API wird kein Key benoetigt
# allerdings koennen damit hoechstens 6 Anfragen pro Stunde gemacht werden
# das Repo kann bei url angepasst werden
def get_github_stars():
    url = 'https://api.github.com/repos/bitshiftcrazy/blog'
    data = requests.get(url)
    data = data.json()

    watchers = data['watchers']
    
    return str(watchers)

# Pokemon Sprite holen
# Die Pokemon API selbst liefert bei Anfragen eine Menge an Informationen,
# die fuer unseren Zweck nicht benoetigt wird
# deshalb holen wir zufaellige Sprites (Bilder) direkt von ihrer GitHub Seite
def get_pokemon():
    rand_int = random.randint(0, 120)
    url = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{}.png".format(rand_int)
    response = requests.get(url)

    if response.status_code != 200:
        return 0

    else:
        file = open("pokemon.png", "wb")
        file.write(response.content)
        file.close()
        return 1


def main():
    try:
        # EPD Klasse initialisieren
        display = epd7in5b_HD.EPD()
        display.init()

        # erstmal weisser Hintergrund
        display.Clear()

        # Display-Hoehe und Breite
        w = display.width
        h = display.height

        # GitHub-Repo Sternchen holen und auf Breite anpassen
        github_stars = get_github_stars()

        # Dad Joke holen und auf Breite anpassen
        dad_joke = get_dad_joke()
        dad_joke = reflow_text(dad_joke, w/3, body)

        # Tweets von drei verschiedenen Accounts holen und auf Breite anpassen
        # die Accounts koennen hier angepasst werden
        heise_online = get_latest_tweet("heiseonline")
        heise_online = reflow_text(heise_online, w/2, body)
        golem = get_latest_tweet("golem")
        golem = reflow_text(golem, w/2, body)
        netzwelt = get_latest_tweet("netzwelt")
        netzwelt = reflow_text(netzwelt, w/2, body)

        # Pokemon-Bild holen
        # falls zufaellig erzeugtes Bild nicht geladen werden kann,
        # wird per default Pikachu angezeigt
        if get_pokemon() != 1:
            pokemon = Image.open(os.path.join(pic_dir, 'pikachu.png'))

        else:
            pokemon = Image.open(os.path.join(pic_dir, 'pokemon.png'))

        # Pokemon auf Groesse anpassen
        pokemon = pokemon.resize((110, 110))

        # leere Layer erstellen, einen fuer schwarz und einen fuer rot
        image = Image.new(mode='1', size=(w,h), color=255)
        image_red = Image.new(mode='1', size=(w,h), color=255)

        # mit schwarz zeichnen
        draw = ImageDraw.Draw(image)
        #mit rot zeichnen
        draw_red = ImageDraw.Draw(image_red)

        # Rahmen zeichen
        draw.line((0, h/3, w/3, h/3), fill = 0)
        draw.line((0, 2*(h/3), w/3, 2*(h/3)), fill = 0)
        draw.line((w/3, 0, w/3, h), fill = 0)

        # Pokemon Bild einfuegen
        image.paste(pokemon, (80, 40))

        # mit rot jeweils die Ueberschriften zeichnen, mit schwarz den restlichen Text
        draw_red.text((10, 0), "Kennst du das Pokemon?", font=heading, fill=0, align='left')

        draw_red.text((10, h/3 + 10), "Deine Repo Sternchen", font=heading, fill=0, align='left')
        draw_red.text((50, h/3 + 50), chr(0xf09b), font=font_awesome_large, fill=0, align='left')
        draw.text((115, h/3 + 50), github_stars, font=body_large, fill=0, align='left')

        draw_red.text((10, 2*(h/3) + 10), "Ein Dad Joke:", font=heading, fill=0, align='left')
        draw.text((0, 2*(h/3) + 50), dad_joke, font=body, fill=0, align='left')
        draw_red.text(((w/3) + 10, 0), "Was gibt's Neues?", font=heading, fill=0, align='left')
        draw.text(((w/3) + 10, 50), heise_online, font=body, fill=0, align='left')
        draw.text(((w/3) + 10, (h/3) + 50), golem, font=body, fill=0, align='left')
        draw.text(((w/3) + 10, 2*(h/3) + 50), netzwelt, font=body, fill=0)

        # Text/Bild anzeigen
        display.display(display.getbuffer(image), display.getbuffer(image_red))

        # eine halbe Stunde warten
        time.sleep(60*30)
        
        logging.info("Clear...")
        display.init()
        display.Clear()

    except IOError as e:
        logging.info(e)
        sys.exit()

    except KeyboardInterrupt:
        logging.info("CTRL + C:")
        epd7in5b_HD.epdconfig.module_exit()
        sys.exit()

while True:

    t = datetime.datetime.now()

    # der Screen soll nur zwischen 8h und 23h verwendet werden
    # hier fuer andere Uhrzeiten anpassen
    if 8 <= t.hour <= 23:
        main()
    else:
        time.sleep(30)
