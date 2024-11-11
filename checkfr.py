
import re
import math
import string

from words import occurence
from setup import bi_cars


def get_symboles(texte: str) -> str:
    ''' Retourne les symboles qui forment un texte '''
    symboles_du_message = []

    i = 0
    while (i <= len(texte) - 2):
        # Le prochain symbole est un bigramme
        if (texte[i:i+2] in bi_cars):
            symboles_du_message.append(texte[i:i+2])
            i += 2
        else:
            symboles_du_message.append(texte[i])
            i += 1
    # Si on a laissé un caractère à la fin
    if (i == len(texte) - 1):
        symboles_du_message.append(texte[i])

    return symboles_du_message


def get_punitions(texte: str) -> str:
    ''' Applique des punitions au texte '''
    punitions = 0

    mots_texte = re.split(' ', texte)
    # Retire mot vide
    mots_texte = [mot for mot in mots_texte if mot]
    total = len(texte)

    for i, mot in enumerate(mots_texte):
        if len(mot) == 1:
            if (mot != "a" or mot != "à" or mot != "y"):
                punitions += math.log10(1/total)
        if mot[-1] in string.punctuation:
            # Punctuation valide, on punit pas
            mot = mot[:-1]
        if any(char in string.punctuation for char in mot):
            punitions += math.log10(1/total)

        if (len(mot) == 0):
            if (i != 0 or i != len(texte) - 1):
                # Ponctuation seule
                punitions += math.log10(1/total)

        else:
            if mot in occurence:
                if len(mot) <= 4:
                    punitions += len(mot)
                else:
                    punitions += len(mot) * 2
            else:
                punitions -= len(mot) * 2

    for i, char in enumerate(texte):
        if (char == "." and i < len(texte) - 3 and not texte[i+2].isupper()):
            punitions += math.log10(1/total)

        if (char == " " and i < len(texte) - 2 and texte[i+1] == " "):
            # Double espaces
            punitions += math.log10(1/total)
        if (char == " " and i > 0 and texte[i-1] == " "):
            # Double espaces
            punitions += math.log10(1/total)

    return punitions


def check_if_francais(texte: str, freq_bigrammes: dict) -> float:
    ''' Retourne la probabilité qu'un texte soit en français '''
    symboles_msg = get_symboles(texte)

    probabilite_fr = 0
    i = 0
    while i < len(symboles_msg) - 2:
        probabilite_bigramme = freq_bigrammes.get(
            symboles_msg[i] + symboles_msg[i+1])
        probabilite_fr += math.log10(probabilite_bigramme)
        i += 1

    # Punitions "manuelles"
    probabilite_fr += get_punitions(texte)
    return probabilite_fr
