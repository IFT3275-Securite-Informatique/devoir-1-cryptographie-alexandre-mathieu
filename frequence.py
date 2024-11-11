from collections import Counter
import itertools
import string


from setup import symboles

def get_symboles_freq(arr_symboles: list) -> dict:
    ''' Retourne la fréquence des symboles d'une liste '''
    arr_symboles = [symbole for symbole in arr_symboles if symbole in symboles]
    # Occurence symboles dans la liste
    dict_occurence = Counter(arr_symboles)
    # On y ajoute les symboles qui peuvnet ne pas avoir été trouvé
    missing = symboles - dict_occurence.keys()

    # On leur donne au moins une occurence
    for symbole in missing:
        dict_occurence[symbole] = 1

    total = sum(dict_occurence.values())

    dict_freq = {symbole: count / total for symbole,
                 count in dict_occurence.items()}
    dict_freq = {key: value for key, value in sorted(
        dict_freq.items(), key=lambda freq: freq[1], reverse=True)}
    return dict_freq


def get_bigramme_freq(arr_symboles: list) -> dict:
    ''' Retourne la fréquence de bigramme d'une liste '''
    # On récupère toutes les paires de symboles possible
    paires_possible_tuples = list(itertools.product(symboles, repeat=2))
    paires_possible = [''.join(paire) for paire in paires_possible_tuples]
    bigramme_occurence = {paire: 1 for paire in paires_possible}

    for i in range(len(arr_symboles) - 2):
        bigramme = arr_symboles[i] + arr_symboles[i+1]
        if bigramme in bigramme_occurence:
            bigramme_occurence[bigramme] += 1

    total = sum(bigramme_occurence.values())

    bigramme_freq = {symbole: count / total for symbole,
                     count in bigramme_occurence.items()}
    bigramme_freq = {key: value for key, value in sorted(
        bigramme_freq.items(), key=lambda freq: freq[1], reverse=True)}
    return bigramme_freq