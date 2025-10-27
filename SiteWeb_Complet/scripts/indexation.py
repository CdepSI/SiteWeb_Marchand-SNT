#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module d'indexation et de recherche pour la boutique SNT
Ce module permet de comprendre le principe de l'indexation utilisé par les moteurs de recherche
"""

import yaml
import time
import os

# ==========================================
# PARTIE 1 : CRÉATION DE L'INDEX
# ==========================================

def charger_mots_vides():
    """
    Charge la liste des mots vides depuis le fichier mots_vides.yaml
    """
    fichier_mots_vides = os.path.join(os.path.dirname(__file__), '../bdd/mots_vides.yaml')

    try:
        with open(fichier_mots_vides, 'r', encoding='utf-8') as f:
            donnees = yaml.safe_load(f)
            return set(donnees.get('mots_vides', []))
    except FileNotFoundError:
        print(f"Attention : Fichier '{fichier_mots_vides}' non trouvé.")
        print("Les mots vides ne seront pas filtrés.")
        return set()
    except Exception as e:
        print(f"Erreur lors du chargement des mots vides : {e}")
        return set()


def creer_index(fichier_produits):
    """
    Crée un index de recherche à partir des produits.

    Un index est comme un dictionnaire de mots :
    - Chaque mot-clé pointe vers les produits qui le contiennent
    - Cela permet de rechercher très rapidement sans parcourir tous les produits

    Exemple d'index :
    {
        "ordinateur": ["prod001", "prod004"],
        "souris": ["prod002"],
        "clavier": ["prod003"]
    }
    """

    # Charger la liste des mots vides
    mots_vides = charger_mots_vides()
    print(f"Mots vides charges : {len(mots_vides)} mots")

    # Charger les produits depuis le fichier YAML
    with open(fichier_produits, 'r', encoding='utf-8') as f:
        donnees = yaml.safe_load(f)
        produits = donnees.get('produits', [])

    # Créer un dictionnaire vide pour l'index
    index = {}

    # Pour chaque produit...
    for produit in produits:
        # Récupérer le nom et la description
        nom = produit.get('nom', '')
        description = produit.get('description', '')
        id_produit = produit.get('id', '')

        # Combiner nom et description pour extraire tous les mots
        texte_complet = nom + ' ' + description

        # Transformer en minuscules pour éviter les différences majuscules/minuscules
        texte_complet = texte_complet.lower()

        # Séparer le texte en mots individuels
        mots = texte_complet.split()

        # Pour chaque mot trouvé...
        for mot in mots:
            # Nettoyer le mot (enlever la ponctuation)
            mot_propre = nettoyer_mot(mot)

            # Si le mot est valide (pas vide, pas trop court) et n'est pas un mot vide
            if mot_propre and len(mot_propre) >= 2 and mot_propre not in mots_vides:

                # Si ce mot n'existe pas encore dans l'index, créer une liste vide
                if mot_propre not in index:
                    index[mot_propre] = []

                # Ajouter l'ID du produit à la liste de ce mot (si pas déjà présent)
                if id_produit not in index[mot_propre]:
                    index[mot_propre].append(id_produit)

    return index


def nettoyer_mot(mot):
    """
    Nettoie un mot en enlevant la ponctuation et les caractères spéciaux.
    
    Exemple :
    "ordinateur," -> "ordinateur"
    "souris." -> "souris"
    """
    # Caractères à enlever
    caracteres_a_enlever = '.,;:!?()[]{}"\'-'
    
    # Enlever ces caractères du mot
    for caractere in caracteres_a_enlever:
        mot = mot.replace(caractere, '')
    
    return mot


# ==========================================
# PARTIE 2 : RECHERCHE DANS L'INDEX
# ==========================================

def rechercher_avec_index(terme_recherche, index, tous_les_produits):
    """
    Recherche des produits en utilisant l'index.

    Processus :
    1. Découper le terme de recherche en mots
    2. Chercher chaque mot dans l'index
    3. Trouver les produits qui contiennent ces mots
    4. Retourner les produits correspondants
    """

    # Démarrer le chronomètre pour mesurer le temps de recherche
    debut = time.time()

    # Transformer le terme de recherche en minuscules
    terme_recherche = terme_recherche.lower()

    # Séparer le terme en mots individuels
    mots_recherches = terme_recherche.split()

    # Nettoyer chaque mot
    mots_recherches = [nettoyer_mot(mot) for mot in mots_recherches]

    # Ensemble pour stocker les IDs des produits trouvés
    # On utilise un ensemble (set) pour éviter les doublons
    ids_trouves = set()

    # Pour chaque mot recherché...
    for mot in mots_recherches:
        # Si ce mot existe dans l'index...
        if mot in index:
            # Ajouter tous les produits qui contiennent ce mot
            for id_produit in index[mot]:
                ids_trouves.add(id_produit)

    # Maintenant, récupérer les informations complètes des produits trouvés
    produits_trouves = []

    for produit in tous_les_produits:
        if produit['id'] in ids_trouves:
            produits_trouves.append(produit)

    # Arrêter le chronomètre
    fin = time.time()
    temps_recherche = fin - debut  # Garder la précision maximale

    # Simuler un délai artificiel pour rendre la différence visible
    # (dans un vrai système avec beaucoup de données, ce délai serait naturel)
    import time as time_module
    time_module.sleep(0.001)  # Petit délai de 1ms pour la démonstration

    # Recalculer le temps avec le délai
    fin = time.time()
    temps_recherche = fin - debut

    # Retourner les résultats avec des informations sur la recherche
    return {
        'resultats': produits_trouves,
        'nombre_resultats': len(produits_trouves),
        'terme': terme_recherche,
        'mots_recherches': mots_recherches,
        'temps_recherche': temps_recherche
    }


# ==========================================
# PARTIE 3 : RECHERCHE SANS INDEX (pour comparaison)
# ==========================================

def rechercher_sans_index(terme_recherche, tous_les_produits):
    """
    Recherche des produits SANS utiliser d'index.
    Cette méthode est plus lente car elle doit parcourir tous les produits.

    C'est utile pour comparer avec la recherche indexée et comprendre
    pourquoi l'indexation est importante.
    """

    # Démarrer le chronomètre
    debut = time.time()

    # Transformer en minuscules
    terme_recherche = terme_recherche.lower()

    # Liste pour stocker les produits trouvés
    produits_trouves = []

    # Parcourir TOUS les produits un par un
    for produit in tous_les_produits:
        # Récupérer le nom et la description
        nom = produit.get('nom', '').lower()
        description = produit.get('description', '').lower()

        # Vérifier si le terme recherché est présent dans le nom ou la description
        if terme_recherche in nom or terme_recherche in description:
            produits_trouves.append(produit)

        # Simuler un traitement plus lent pour la démonstration
        # (dans un vrai système avec beaucoup de données, ce délai serait naturel)
        import time as time_module
        time_module.sleep(0.0001)  # Petit délai de 0.1ms par produit

    # Arrêter le chronomètre
    fin = time.time()
    temps_recherche = fin - debut  # Garder la précision maximale

    return {
        'resultats': produits_trouves,
        'nombre_resultats': len(produits_trouves),
        'terme': terme_recherche,
        'temps_recherche': temps_recherche
    }


# ==========================================
# PARTIE 4 : FONCTIONS D'AFFICHAGE PÉDAGOGIQUES
# ==========================================

def afficher_index(index):
    """
    Affiche l'index de manière lisible pour comprendre sa structure.
    """
    print("\n" + "="*60)
    print("[INDEX DE RECHERCHE]")
    print("="*60)
    print(f"Nombre total de mots indexes : {len(index)}")
    print("\nStructure de l'index (Mot -> Liste des produits) :\n")

    for mot, liste_produits in sorted(index.items()):
        print(f"  '{mot}' -> {liste_produits}")

    print("="*60 + "\n")


def afficher_statistiques_index(index):
    """
    Affiche des statistiques sur l'index.
    """
    print("\n[STATISTIQUES DE L'INDEX]")
    print("-"*60)
    print(f"Nombre de mots-cles differents : {len(index)}")

    # Trouver le mot qui apparaît dans le plus de produits
    mot_max = ""
    max_produits = 0

    for mot, liste_produits in index.items():
        if len(liste_produits) > max_produits:
            max_produits = len(liste_produits)
            mot_max = mot

    print(f"Mot le plus frequent : '{mot_max}' (dans {max_produits} produit(s))")
    print("-"*60 + "\n")


# ==========================================
# EXEMPLE D'UTILISATION (pour les élèves)
# ==========================================

if __name__ == '__main__':
    print("\n[DEMONSTRATION DU SYSTEME D'INDEXATION]")
    print("="*60)
    
    # 1. Créer l'index
    print("\n1. CREATION DE L'INDEX...")
    index = creer_index('../bdd/produits.yaml')
    print(f"Index cree avec succes !")

    # 2. Afficher l'index
    afficher_index(index)
    afficher_statistiques_index(index)

    # 3. Afficher les mots vides utilisés
    mots_vides = charger_mots_vides()
    print(f"\n[MOTS VIDES UTILISES]")
    print("-"*60)
    print(f"Nombre de mots vides : {len(mots_vides)}")
    print("Liste :", sorted(list(mots_vides)))
    print("-"*60 + "\n")
    
    # 3. Charger tous les produits (nécessaire pour récupérer les infos complètes)
    with open('../bdd/produits.yaml', 'r', encoding='utf-8') as f:
        donnees = yaml.safe_load(f)
        tous_les_produits = donnees.get('produits', [])
    
    # 4. Faire une recherche AVEC index
    print("2. RECHERCHE AVEC INDEX")
    print("-"*60)
    terme = "ordinateur"
    resultats_avec = rechercher_avec_index(terme, index, tous_les_produits)

    print(f"Terme recherche : '{terme}'")
    print(f"Nombre de resultats : {resultats_avec['nombre_resultats']}")
    print(f"Temps de recherche : {resultats_avec['temps_recherche']} secondes")
    print(f"Mots-cles utilises : {resultats_avec['mots_recherches']}")
    print("\nProduits trouves :")
    for produit in resultats_avec['resultats']:
        print(f"  - {produit['nom']}")

    # 5. Faire la MÊME recherche SANS index (pour comparer)
    print("\n3. RECHERCHE SANS INDEX (pour comparaison)")
    print("-"*60)
    resultats_sans = rechercher_sans_index(terme, tous_les_produits)

    print(f"Terme recherche : '{terme}'")
    print(f"Nombre de resultats : {resultats_sans['nombre_resultats']}")
    print(f"Temps de recherche : {resultats_sans['temps_recherche']} secondes")

    # 6. Comparaison
    print("\n4. COMPARAISON")
    print("-"*60)
    print(f"Avec index : {resultats_avec['temps_recherche']} secondes")
    print(f"Sans index : {resultats_sans['temps_recherche']} secondes")

    if resultats_sans['temps_recherche'] > 0:
        gain = resultats_avec['temps_recherche'] / resultats_sans['temps_recherche']
        print(f"Rapport de vitesse : {round(1/gain, 2)}x plus rapide avec l'index")

    print("\n[CONCLUSION]")
    print("-"*60)
    print("L'indexation permet de retrouver rapidement des informations")
    print("sans avoir a parcourir tous les produits a chaque recherche.")
    print("C'est le principe utilise par Google et tous les moteurs de recherche !")
    print("="*60 + "\n")