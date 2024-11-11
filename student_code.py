import math
import random

from checkfr import get_punitions, check_if_francais, get_symboles
from setup import appliquer_regles, get_corpus, load_text_from_web, extraire_cipher, get_cle_initiale
from frequence import get_symboles_freq, get_bigramme_freq


def decrypt(c):

  # Récupération du corpus
  corpus = get_corpus()

  symboles_corpus = get_symboles(corpus)

  # Fréquence symboles et bigrammes
  dict_freq = get_symboles_freq(symboles_corpus)
  bigramme_freq = get_bigramme_freq(symboles_corpus)

  # Fréquence du message chiffré
  chars_occurence = extraire_cipher(c)


  cle_initiale = get_cle_initiale(dict_freq, chars_occurence)

  message_initial = appliquer_regles(c, cle_initiale)

  proba_initiale = check_if_francais(message_initial, bigramme_freq)


  ancien_message = best_message = message_initial
  ancienne_proba = best_proba = proba_initiale
  ancienne_cle = best_cle = cle_initiale
  for i in range(10000):
      nouvelle_cle = ancienne_cle.copy()
      # On échange 2 règles
      # On veut au moins que une des règles soit utilisée
      changement_valide = 0
      while (not changement_valide):
          swap1 = random.choice(list(ancienne_cle.keys()))
          if swap1 in c:
              changement_valide = 1

      swap2 = random.choice(list(ancienne_cle.keys()))

      # On swap
      nouvelle_cle[swap1], nouvelle_cle[swap2] = ancienne_cle[swap2], ancienne_cle[swap1]

      nouveau_message = appliquer_regles(c, nouvelle_cle)
      nouvelle_proba = check_if_francais(nouveau_message, bigramme_freq)

      if (best_proba < nouvelle_proba):
          best_message = nouveau_message
          best_proba = nouvelle_proba
          best_cle = nouvelle_cle.copy()

      if (math.exp(nouvelle_proba - ancienne_proba) > 1):
          ancien_message = nouveau_message
          ancienne_proba = nouvelle_proba
          ancienne_cle = nouvelle_cle.copy()
      else:
          success = math.exp(nouvelle_proba - ancienne_proba)
          res = random.uniform(0, 1)
          if (res <= success):
              ancienne_cle = nouvelle_cle.copy()
              ancienne_proba = nouvelle_proba


  print("Message OG:", message_og)
  print("Proba OG", check_if_francais(message_og, bigramme_freq))

  print("Meilleur message:", best_message)
  print("Meilleure Proba:", best_proba)

  return best_message
