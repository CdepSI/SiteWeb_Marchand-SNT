#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module pédagogique sur les cookies HTTP
Ce module permet de comprendre comment fonctionnent les cookies
"""

# ==========================================
# PARTIE 1 : QU'EST-CE QU'UN COOKIE ?
# ==========================================

"""
Un COOKIE est une petite information (texte) que le serveur web enregistre
dans le navigateur de l'utilisateur.

C'est comme un POST-IT que le serveur colle sur le navigateur pour se souvenir
de quelque chose sur l'utilisateur.

EXEMPLES D'UTILISATION :
- Se souvenir que vous êtes connecté (pas besoin de retaper votre mot de passe)
- Mémoriser votre panier d'achat
- Se souvenir de vos préférences (langue, thème sombre/clair)
- Garder l'historique des produits consultés (notre cas)

STRUCTURE D'UN COOKIE :
nom=valeur; expires=date; path=/

Exemple :
historique_produits=prod001,prod002,prod003; expires=Fri, 31 Dec 2025 23:59:59 GMT; path=/
"""

# ==========================================
# PARTIE 2 : SIMULATION DE COOKIES EN PYTHON
# ==========================================

# Simulons le fonctionnement des cookies avec un dictionnaire Python
cookies_navigateur = {}


def creer_cookie_simulation(nom, valeur):
    """
    Simule la création d'un cookie.
    Dans la réalité, le navigateur stocke cette information localement.
    """
    cookies_navigateur[nom] = valeur
    print(f"🍪 Cookie créé : {nom} = {valeur}")
    print(f"   Stocké dans le navigateur")
    return True


def lire_cookie_simulation(nom):
    """
    Simule la lecture d'un cookie.
    Le navigateur renvoie la valeur au serveur quand celui-ci en a besoin.
    """
    if nom in cookies_navigateur:
        valeur = cookies_navigateur[nom]
        print(f"📖 Lecture du cookie : {nom} = {valeur}")
        return valeur
    else:
        print(f"❌ Cookie '{nom}' non trouvé")
        return None


def supprimer_cookie_simulation(nom):
    """
    Simule la suppression d'un cookie.
    On le fait 'expirer' en le retirant du navigateur.
    """
    if nom in cookies_navigateur:
        del cookies_navigateur[nom]
        print(f"🗑️ Cookie supprimé : {nom}")
        return True
    else:
        print(f"❌ Cookie '{nom}' n'existe pas")
        return False


def afficher_tous_les_cookies():
    """
    Affiche tous les cookies stockés.
    """
    print("\n" + "="*60)
    print("🍪 COOKIES ACTUELLEMENT STOCKÉS")
    print("="*60)
    
    if len(cookies_navigateur) == 0:
        print("Aucun cookie enregistré")
    else:
        for nom, valeur in cookies_navigateur.items():
            print(f"  {nom} = {valeur}")
    
    print("="*60 + "\n")


# ==========================================
# PARTIE 3 : HISTORIQUE DES PRODUITS
# ==========================================

def ajouter_produit_historique(id_produit):
    """
    Ajoute un produit à l'historique (dans un cookie).
    
    Le principe :
    1. Lire l'historique actuel depuis le cookie
    2. Ajouter le nouveau produit au début de la liste
    3. Garder seulement les 5 derniers produits
    4. Sauvegarder dans le cookie
    """
    
    print(f"\n➕ Ajout du produit {id_produit} à l'historique...")
    
    # Étape 1 : Lire l'historique actuel
    historique_texte = lire_cookie_simulation('historique_produits')
    
    # Étape 2 : Convertir le texte en liste
    if historique_texte is None or historique_texte == "":
        # Aucun historique : créer une liste vide
        liste_produits = []
    else:
        # Séparer le texte par des virgules
        liste_produits = historique_texte.split(',')
    
    print(f"   Historique actuel : {liste_produits}")
    
    # Étape 3 : Retirer le produit s'il existe déjà
    if id_produit in liste_produits:
        liste_produits.remove(id_produit)
        print(f"   Produit déjà présent, on le met en premier")
    
    # Étape 4 : Ajouter le produit au début
    liste_produits.insert(0, id_produit)
    
    # Étape 5 : Garder seulement les 5 derniers
    if len(liste_produits) > 5:
        liste_produits = liste_produits[:5]
        print(f"   Limite de 5 produits, on garde les plus récents")
    
    # Étape 6 : Convertir la liste en texte
    nouvel_historique = ','.join(liste_produits)
    
    # Étape 7 : Sauvegarder dans le cookie
    creer_cookie_simulation('historique_produits', nouvel_historique)
    
    print(f"   Nouvel historique : {liste_produits}")
    print(f"✓ Historique mis à jour !")


def afficher_historique():
    """
    Affiche l'historique des produits consultés.
    """
    print("\n📚 HISTORIQUE DES PRODUITS CONSULTÉS")
    print("-"*60)
    
    historique_texte = lire_cookie_simulation('historique_produits')
    
    if historique_texte is None or historique_texte == "":
        print("Aucun produit consulté récemment")
    else:
        liste_produits = historique_texte.split(',')
        print(f"Nombre de produits : {len(liste_produits)}")
        print("Produits consultés (du plus récent au plus ancien) :")
        for i, produit in enumerate(liste_produits, 1):
            print(f"  {i}. {produit}")
    
    print("-"*60 + "\n")


def effacer_historique():
    """
    Efface l'historique des produits.
    """
    print("\n🗑️ Effacement de l'historique...")
    supprimer_cookie_simulation('historique_produits')
    print("✓ Historique effacé !")


# ==========================================
# PARTIE 4 : PRÉFÉRENCES UTILISATEUR
# ==========================================

def definir_preference(cle, valeur):
    """
    Définit une préférence utilisateur (langue, thème, etc.)
    """
    nom_cookie = f"pref_{cle}"
    creer_cookie_simulation(nom_cookie, str(valeur))
    print(f"✓ Préférence '{cle}' définie à : {valeur}")


def obtenir_preference(cle, valeur_defaut="non définie"):
    """
    Récupère une préférence utilisateur.
    """
    nom_cookie = f"pref_{cle}"
    valeur = lire_cookie_simulation(nom_cookie)
    
    if valeur is None:
        return valeur_defaut
    return valeur


# ==========================================
# PARTIE 5 : DÉMONSTRATION COMPLÈTE
# ==========================================

def demonstration_cookies():
    """
    Démonstration complète du fonctionnement des cookies.
    """
    print("\n" + "="*60)
    print("🎓 DÉMONSTRATION : COMPRENDRE LES COOKIES")
    print("="*60)
    
    # Scénario 1 : Premier utilisateur qui visite le site
    print("\n📌 SCÉNARIO 1 : Premier utilisateur")
    print("-"*60)
    print("L'utilisateur arrive sur le site pour la première fois.")
    print("Il n'a aucun cookie.")
    afficher_tous_les_cookies()
    
    # Scénario 2 : L'utilisateur consulte des produits
    print("\n📌 SCÉNARIO 2 : Consultation de produits")
    print("-"*60)
    print("L'utilisateur consulte plusieurs produits...")
    
    ajouter_produit_historique('prod001')
    ajouter_produit_historique('prod003')
    ajouter_produit_historique('prod005')
    
    afficher_historique()
    afficher_tous_les_cookies()
    
    # Scénario 3 : L'utilisateur revient sur un produit déjà vu
    print("\n📌 SCÉNARIO 3 : Re-consultation d'un produit")
    print("-"*60)
    print("L'utilisateur revient voir le prod001...")
    
    ajouter_produit_historique('prod001')
    afficher_historique()
    
    # Scénario 4 : Dépassement de la limite
    print("\n📌 SCÉNARIO 4 : Limite de 5 produits")
    print("-"*60)
    print("L'utilisateur consulte encore plus de produits...")
    
    ajouter_produit_historique('prod002')
    ajouter_produit_historique('prod004')
    ajouter_produit_historique('prod006')  # Le 6ème produit
    
    afficher_historique()
    print("💡 Remarque : Seuls les 5 derniers produits sont conservés")
    
    # Scénario 5 : Préférences utilisateur
    print("\n📌 SCÉNARIO 5 : Préférences utilisateur")
    print("-"*60)
    print("L'utilisateur définit ses préférences...")
    
    definir_preference('langue', 'français')
    definir_preference('theme', 'sombre')
    definir_preference('notifications', 'activées')
    
    afficher_tous_les_cookies()
    
    print("\nRécupération des préférences :")
    print(f"  Langue : {obtenir_preference('langue')}")
    print(f"  Thème : {obtenir_preference('theme')}")
    print(f"  Notifications : {obtenir_preference('notifications')}")
    
    # Scénario 6 : L'utilisateur ferme son navigateur et revient
    print("\n📌 SCÉNARIO 6 : Retour de l'utilisateur")
    print("-"*60)
    print("L'utilisateur ferme son navigateur et revient le lendemain.")
    print("Ses cookies sont toujours là (jusqu'à expiration) !")
    
    afficher_historique()
    afficher_tous_les_cookies()
    
    # Scénario 7 : Effacement des cookies
    print("\n📌 SCÉNARIO 7 : Effacement des cookies")
    print("-"*60)
    print("L'utilisateur veut effacer son historique...")
    
    effacer_historique()
    afficher_tous_les_cookies()
    
    print("\n" + "="*60)
    print("💡 CONCLUSION")
    print("="*60)
    print("Les cookies permettent au site de se souvenir de l'utilisateur")
    print("entre les visites, sans avoir besoin de compte utilisateur.")
    print("Ils sont stockés dans le NAVIGATEUR, pas sur le serveur.")
    print("="*60 + "\n")


# ==========================================
# PARTIE 6 : COMPARAISON COOKIES vs BASE DE DONNÉES
# ==========================================

def comparer_cookies_base_donnees():
    """
    Compare les cookies et les bases de données pour comprendre leurs différences.
    """
    print("\n" + "="*60)
    print("📊 COMPARAISON : COOKIES vs BASE DE DONNÉES")
    print("="*60)
    
    print("\n🍪 COOKIES :")
    print("  ✓ Stockés dans le NAVIGATEUR de l'utilisateur")
    print("  ✓ Limités en taille (environ 4 Ko par cookie)")
    print("  ✓ Accessibles uniquement par le navigateur de l'utilisateur")
    print("  ✓ Persistent même si le serveur est éteint")
    print("  ✓ Peuvent expirer après un certain temps")
    print("  ✓ L'utilisateur peut les supprimer")
    print("  ✓ Idéal pour : préférences, historique, panier temporaire")
    
    print("\n💾 BASE DE DONNÉES :")
    print("  ✓ Stockées sur le SERVEUR")
    print("  ✓ Pas de limite de taille")
    print("  ✓ Accessibles par tous les utilisateurs (si partagé)")
    print("  ✓ Persistent même si le navigateur est fermé")
    print("  ✓ Ne peuvent pas être supprimées par l'utilisateur")
    print("  ✓ Nécessitent un compte utilisateur pour identifier la personne")
    print("  ✓ Idéal pour : comptes, commandes, données partagées")
    
    print("\n📝 EXEMPLE CONCRET :")
    print("-"*60)
    print("Amazon utilise :")
    print("  🍪 Cookies pour : votre panier temporaire, vos préférences")
    print("  💾 Base de données pour : votre compte, vos commandes passées")
    print("="*60 + "\n")


# ==========================================
# PARTIE 7 : SÉCURITÉ ET VIE PRIVÉE
# ==========================================

def explication_securite_cookies():
    """
    Explique les aspects de sécurité et vie privée des cookies.
    """
    print("\n" + "="*60)
    print("🔒 SÉCURITÉ ET VIE PRIVÉE DES COOKIES")
    print("="*60)
    
    print("\n✅ CE QUE PEUVENT FAIRE LES COOKIES :")
    print("  - Mémoriser vos préférences")
    print("  - Garder votre panier d'achat")
    print("  - Se souvenir que vous êtes connecté")
    print("  - Suivre les pages que vous visitez sur UN site")
    
    print("\n❌ CE QUE NE PEUVENT PAS FAIRE LES COOKIES :")
    print("  - Accéder à vos fichiers personnels")
    print("  - Lire vos emails")
    print("  - Installer des virus")
    print("  - Voler vos mots de passe (sauf si mal utilisés)")
    
    print("\n⚠️ PROBLÈMES DE VIE PRIVÉE :")
    print("  - Les cookies de SUIVI (tracking) peuvent suivre votre")
    print("    navigation sur PLUSIEURS sites (publicité ciblée)")
    print("  - C'est pourquoi l'Europe impose les bannières 'cookies'")
    print("  - Vous pouvez refuser ces cookies de suivi")
    
    print("\n💡 BONNES PRATIQUES :")
    print("  - Ne jamais stocker de mots de passe dans les cookies")
    print("  - Utiliser des cookies 'HttpOnly' pour la sécurité")
    print("  - Faire expirer les cookies après un certain temps")
    print("  - Informer les utilisateurs de l'utilisation des cookies")
    
    print("="*60 + "\n")


# ==========================================
# PARTIE 8 : EXERCICES PRATIQUES
# ==========================================

def exercice_1():
    """
    Exercice 1 : Créer un système de préférences de langue
    """
    print("\n" + "="*60)
    print("📝 EXERCICE 1 : Système de préférences")
    print("="*60)
    
    print("\nCréons un système pour mémoriser la langue préférée...")
    
    # Code à compléter par les élèves
    definir_preference('langue', 'français')
    
    langue = obtenir_preference('langue')
    
    if langue == 'français':
        print("Bienvenue sur notre site !")
    elif langue == 'anglais':
        print("Welcome to our website!")
    else:
        print("Langue non reconnue")


def exercice_2():
    """
    Exercice 2 : Compter le nombre de visites
    """
    print("\n" + "="*60)
    print("📝 EXERCICE 2 : Compteur de visites")
    print("="*60)
    
    print("\nCréons un compteur de visites...")
    
    # Lire le compteur actuel
    compteur_texte = lire_cookie_simulation('nb_visites')
    
    if compteur_texte is None:
        # Première visite
        compteur = 1
        print("👋 Bienvenue pour la première fois !")
    else:
        # Convertir le texte en nombre et ajouter 1
        compteur = int(compteur_texte) + 1
        print(f"👋 Content de vous revoir ! (Visite n°{compteur})")
    
    # Sauvegarder le nouveau compteur
    creer_cookie_simulation('nb_visites', str(compteur))


# ==========================================
# PROGRAMME PRINCIPAL
# ==========================================

if __name__ == '__main__':
    print("\n" + "🍪"*30)
    print("MODULE PÉDAGOGIQUE SUR LES COOKIES HTTP")
    print("🍪"*30)
    
    # Menu interactif
    while True:
        print("\n" + "="*60)
        print("MENU PRINCIPAL")
        print("="*60)
        print("1. Démonstration complète des cookies")
        print("2. Comparaison cookies vs base de données")
        print("3. Sécurité et vie privée")
        print("4. Exercice 1 : Préférences de langue")
        print("5. Exercice 2 : Compteur de visites")
        print("6. Tester manuellement les cookies")
        print("0. Quitter")
        print("="*60)
        
        choix = input("\nVotre choix (0-6) : ")
        
        if choix == '1':
            demonstration_cookies()
        elif choix == '2':
            comparer_cookies_base_donnees()
        elif choix == '3':
            explication_securite_cookies()
        elif choix == '4':
            exercice_1()
        elif choix == '5':
            exercice_2()
        elif choix == '6':
            print("\n" + "="*60)
            print("MODE TEST MANUEL")
            print("="*60)
            print("Commandes disponibles :")
            print("  creer <nom> <valeur>  - Créer un cookie")
            print("  lire <nom>            - Lire un cookie")
            print("  supprimer <nom>       - Supprimer un cookie")
            print("  afficher              - Afficher tous les cookies")
            print("  historique            - Afficher l'historique")
            print("  ajouter <id>          - Ajouter un produit à l'historique")
            print("  retour                - Retour au menu")
            print("="*60)
            
            while True:
                commande = input("\n>>> ").strip().split()
                
                if len(commande) == 0:
                    continue
                
                if commande[0] == 'retour':
                    break
                elif commande[0] == 'creer' and len(commande) >= 3:
                    creer_cookie_simulation(commande[1], ' '.join(commande[2:]))
                elif commande[0] == 'lire' and len(commande) >= 2:
                    lire_cookie_simulation(commande[1])
                elif commande[0] == 'supprimer' and len(commande) >= 2:
                    supprimer_cookie_simulation(commande[1])
                elif commande[0] == 'afficher':
                    afficher_tous_les_cookies()
                elif commande[0] == 'historique':
                    afficher_historique()
                elif commande[0] == 'ajouter' and len(commande) >= 2:
                    ajouter_produit_historique(commande[1])
                else:
                    print("❌ Commande inconnue ou arguments manquants")
        
        elif choix == '0':
            print("\n👋 Au revoir !")
            break
        else:
            print("\n❌ Choix invalide, réessayez.")
    
    print("\n" + "🍪"*30 + "\n")