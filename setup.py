import requests
import re
from collections import Counter
import math
import random
import string

from words import occurence


# Symboles
bi_cars = ['e ', 's ', 't ', 'es', ' d', '\r\n', 'en', 'qu', ' l', 're', ' p', 'de', 'le', 'nt', 'on', ' c', ', ', ' e', 'ou', ' q', ' s', 'n ', 'ue', 'an', 'te', ' a', 'ai', 'se', 'it', 'me', 'is', 'oi', 'r ', 'er', ' m', 'ce', 'ne', 'et', 'in', 'ns', ' n', 'ur', 'i ', 'a ', 'eu', 'co', 'tr', 'la', 'ar', 'ie', 'ui', 'us', 'ut', 'il', ' t', 'pa', 'au', 'el', 'ti', 'st', 'un', 'em', 'ra', 'e,', 'so', 'or', 'l ', ' f', 'll', 'nd',
           ' j', 'si', 'ir', 'e\r', 'ss', 'u ', 'po', 'ro', 'ri', 'pr', 's,', 'ma', ' v', ' i', 'di', ' r', 'vo', 'pe', 'to', 'ch', '. ', 've', 'nc', 'om', ' o', 'je', 'no', 'rt', 'à ', 'lu', "'e", 'mo', 'ta', 'as', 'at', 'io', 's\r', 'sa', "u'", 'av', 'os', ' à', ' u', "l'", "'a", 'rs', 'pl', 'é ', '; ', 'ho', 'té', 'ét', 'fa', 'da', 'li', 'su', 't\r', 'ée', 'ré', 'dé', 'ec', 'nn', 'mm', "'i", 'ca', 'uv', '\n\r', 'id', ' b', 'ni', 'bl']

cars = ['b', 'j', '\r', 'J', '”', ')', 'Â', 'É', 'ê', '5', 't', '9', 'Y', '%', 'N', 'B', 'V', '\ufeff', 'Ê', '?', '’', 'i', ':', 's', 'C', 'â', 'ï', 'W', 'y', 'p', 'D', '—', '«', 'º', 'A', '3', 'n', '0', 'q', '4', 'e', 'T', 'È', '$', 'U', 'v', '»', 'l', 'P', 'X', 'Z', 'À', 'ç', 'u', '…', 'î',
        'L', 'k', 'E', 'R', '2', '_', '8', 'é', 'O', 'Î', '‘', 'a', 'F', 'H', 'c', '[', '(', "'", 'è', 'I', '/', '!', ' ', '°', 'S', '•', '#', 'x', 'à', 'g', '*', 'Q', 'w', '1', 'û', '7', 'G', 'm', '™', 'K', 'z', '\n', 'o', 'ù', ',', 'r', ']', '.', 'M', 'Ç', '“', 'h', '-', 'f', 'ë', '6', ';', 'd', 'ô']

symboles = cars + bi_cars

# Directement de l'énoncé
def load_text_from_web(url: str) -> str:
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while loading the text: {e}")
        return None


def appliquer_regles(cipher: str, cle: dict) -> str:
    ''' Applique les règles d'une clé sur un message chiffré '''
    message = ""
    for x in range(int((len(cipher) / 8))):
        pos = x*8
        char = cipher[pos:pos+8]
        message += cle[char]
    return message


def get_corpus() -> str:
    ''' Retourne un corpus de texte '''
    corpus = ""
    livres = [13846, 4650, 42064, 35444]

    for livre in livres:
        url = "https://www.gutenberg.org/ebooks/" + str(livre) + ".txt.utf-8"
        texte = load_text_from_web(url)
        if texte:
            # On garde seulement le texte entre les lignes de début et de fin
            # puisque le texte avant et après est strictement en anglais
            resultat = re.search(
                r'\*\*\*\s*START .*?\s*\*\*\*\s*(.*?)\s*\*\*\*\s*END .*?\s*\*\*\*',
                texte,
                re.DOTALL
            )
            texte_extrait = resultat.group(1)
            corpus += texte_extrait

    return corpus


def extraire_cipher(cipher: str) -> str:
    ''' Extrait les symboles d'un message chiffré '''
    chars = []

    for x in range(int((len(cipher) / 8))):
        pos = x*8
        char = cipher[pos:pos+8]
        chars.append(char)

    chars_occurence = Counter(chars)
    chars_occurence = {key: value for key, value in sorted(
        chars_occurence.items(), key=lambda freq: freq[1], reverse=True)}
    return chars_occurence

def get_cle_initiale(dict_freq_symboles: dict, dict_occurence_chars: dict) -> dict:
    ''' Construit une clé initiale à partir d'un dictionnaire de fréquence francophone et
    d'un contenant la fréquence des symboles chiffrés '''
    symboles_bin = [f"{i:08b}" for i in range(256)]

    cle_initiale = {}
    #print(dict_freq_symboles)
    symboles_keys = list(dict_freq_symboles.keys())
    cipher_keys = list(dict_occurence_chars.keys())
    #print(symboles_keys)
    #print(cipher_keys)
    # On assigne les nombres binaires du cipher les plus fréquents
    # Aux symboles les plus fréquents de notre corpus
    for i in range(len(symboles_keys)):
        if i < len(cipher_keys):
            cle_initiale[cipher_keys[i]] = symboles_keys[i]
            symboles_bin.remove(cipher_keys[i])
        else:
            # Les autres nombres sont assignés aléatoirement aux symboles restants
            cle_initiale[symboles_bin[i - len(cipher_keys)]] = symboles_keys[i]
    return cle_initiale