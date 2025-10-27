#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Serveur web Flask pour la boutique SNT
Ce serveur gère les pages HTML, les produits, le panier et les clients
"""

from flask import Flask, jsonify, request, send_from_directory
import yaml
import os
from scripts import cookies
from scripts.indexation import creer_index, rechercher_avec_index

app = Flask(__name__)

# Configuration des chemins
DOSSIER_BDD = 'bdd'  # Dossier contenant les fichiers YAML
FICHIER_PRODUITS = os.path.join(DOSSIER_BDD, 'produits.yaml')
FICHIER_CLIENTS = os.path.join(DOSSIER_BDD, 'clients.yaml')

# Variables globales (déclarées avant utilisation)
INDEX_RECHERCHE = None
PRODUITS_CACHE = []

# Panier en mémoire (temporaire pour chaque session)
panier = []


# === ROUTES POUR LES PAGES HTML ===
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/pages/<path:path>')
def servir_pages(path):
    # Handle JS files in pages/js/ directory
    if path.startswith('js/'):
        return send_from_directory('pages/js', path[3:])
    return send_from_directory('pages', path)

@app.route('/js/<path:path>')
def servir_scripts(path):
    return send_from_directory('js', path)

@app.route('/styles/<path:path>')
def servir_styles(path):
    return send_from_directory('styles', path)

@app.route('/images/<path:path>')
def servir_images(path):
    return send_from_directory('images', path)

@app.route('/bdd/<path:path>')
def servir_bdd(path):
    return send_from_directory('bdd', path)

@app.route('/<path:path>')
def servir_fichier(path):
    return send_from_directory('.', path)


# === API PRODUITS ===
@app.route('/api/produits', methods=['GET'])
def obtenir_produits():
    """Charge et retourne la liste des produits depuis le fichier YAML"""
    try:
        with open(FICHIER_PRODUITS, 'r', encoding='utf-8') as f:
            donnees = yaml.safe_load(f)
            return jsonify(donnees.get('produits', []))
    except FileNotFoundError:
        return jsonify([]), 404
    except Exception as e:
        return jsonify({'erreur': str(e)}), 500


@app.route('/api/produit/<id_produit>', methods=['GET'])
def obtenir_produit(id_produit):
    """Retourne les informations d'UN SEUL produit"""
    try:
        with open(FICHIER_PRODUITS, 'r', encoding='utf-8') as f:
            donnees = yaml.safe_load(f)
            produits = donnees.get('produits', [])
            
            # Chercher le produit avec l'ID correspondant
            for produit in produits:
                if produit.get('id') == id_produit:
                    return jsonify(produit)
            
            # Si le produit n'est pas trouvé
            return jsonify({'erreur': 'Produit non trouvé'}), 404
    except FileNotFoundError:
        return jsonify({'erreur': 'Fichier produits non trouvé'}), 404
    except Exception as e:
        return jsonify({'erreur': str(e)}), 500


# === API RECHERCHE ===
@app.route('/api/recherche', methods=['GET'])
def rechercher_produits():
    """Recherche des produits en utilisant l'index"""
    global INDEX_RECHERCHE, PRODUITS_CACHE
    
    terme = request.args.get('terme', '')
    
    if not terme:
        return jsonify({'erreur': 'Terme de recherche vide'}), 400
    
    try:
        # Utiliser la fonction de recherche avec index
        resultats = rechercher_avec_index(terme, INDEX_RECHERCHE, PRODUITS_CACHE)
        return jsonify(resultats)
    except Exception as e:
        return jsonify({'erreur': str(e)}), 500


@app.route('/api/recherche/index', methods=['GET'])
def obtenir_index():
    """Retourne l'index complet pour visualisation pédagogique"""
    global INDEX_RECHERCHE, PRODUITS_CACHE
    
    # Créer un dictionnaire avec les noms des produits au lieu des IDs
    index_lisible = {}
    
    for mot, liste_ids in INDEX_RECHERCHE.items():
        noms_produits = []
        for id_produit in liste_ids:
            # Trouver le nom du produit correspondant à cet ID
            for produit in PRODUITS_CACHE:
                if produit['id'] == id_produit:
                    noms_produits.append(produit['nom'])
                    break
        
        index_lisible[mot] = noms_produits
    
    return jsonify({
        'index': index_lisible,
        'nombre_mots': len(index_lisible),
        'nombre_produits': len(PRODUITS_CACHE)
    })


# === API PANIER ===
@app.route('/api/panier', methods=['GET'])
def obtenir_panier():
    """Retourne le contenu du panier avec le total"""
    total = sum(article['prix'] * article['quantite'] for article in panier)
    return jsonify({
        'articles': panier,
        'total': total
    })


@app.route('/api/panier/ajouter', methods=['POST'])
def ajouter_au_panier():
    """Ajoute un produit au panier"""
    donnees = request.json
    
    # Vérifier si le produit existe déjà dans le panier
    for article in panier:
        if article['id'] == donnees['id']:
            article['quantite'] += donnees.get('quantite', 1)
            return jsonify({'message': 'Quantité mise à jour'})
    
    # Sinon, ajouter le nouveau produit
    panier.append({
        'id': donnees['id'],
        'nom': donnees['nom'],
        'prix': donnees['prix'],
        'quantite': donnees.get('quantite', 1)
    })
    
    return jsonify({'message': 'Produit ajouté au panier'})


@app.route('/api/panier/retirer', methods=['POST'])
def retirer_du_panier():
    """Retire un produit du panier"""
    donnees = request.json
    global panier
    panier = [article for article in panier if article['id'] != donnees['id']]
    return jsonify({'message': 'Produit retiré'})


@app.route('/api/panier/vider', methods=['POST'])
def vider_panier():
    """Vide complètement le panier"""
    global panier
    panier = []
    return jsonify({'message': 'Panier vidé'})


# === API CLIENTS ===
@app.route('/api/clients', methods=['GET'])
def obtenir_clients():
    """Charge et retourne la liste des clients depuis le fichier YAML"""
    try:
        with open(FICHIER_CLIENTS, 'r', encoding='utf-8') as f:
            donnees = yaml.safe_load(f)
            return jsonify(donnees.get('clients', []))
    except FileNotFoundError:
        return jsonify([])
    except Exception as e:
        return jsonify({'erreur': str(e)}), 500


@app.route('/api/clients/ajouter', methods=['POST'])
def ajouter_client():
    """Ajoute un nouveau client dans le fichier YAML"""
    nouveau_client = request.json
    
    try:
        # Charger les clients existants
        try:
            with open(FICHIER_CLIENTS, 'r', encoding='utf-8') as f:
                donnees = yaml.safe_load(f)
                if donnees is None:
                    donnees = {'clients': []}
        except FileNotFoundError:
            donnees = {'clients': []}
        
        # Ajouter le nouveau client
        donnees['clients'].append(nouveau_client)
        
        # Sauvegarder dans le fichier
        with open(FICHIER_CLIENTS, 'w', encoding='utf-8') as f:
            yaml.dump(donnees, f, allow_unicode=True, default_flow_style=False)
        
        return jsonify({'message': 'Client ajouté avec succès'})
    
    except Exception as e:
        return jsonify({'erreur': str(e)}), 500


# === LANCEMENT DU SERVEUR ===
if __name__ == '__main__':
    # Créer le dossier data s'il n'existe pas
    if not os.path.exists(DOSSIER_BDD):
        os.makedirs(DOSSIER_BDD)
        print(f"Dossier '{DOSSIER_BDD}' cree")
    
    # Créer le fichier clients.yaml s'il n'existe pas
    if not os.path.exists(FICHIER_CLIENTS):
        with open(FICHIER_CLIENTS, 'w', encoding='utf-8') as f:
            yaml.dump({'clients': []}, f, allow_unicode=True)
        print(f"Fichier '{FICHIER_CLIENTS}' cree")
    
    # Créer l'index de recherche au démarrage
    print("\n" + "="*50)
    print("Creation de l'index de recherche...")
    
    # Vérifier si le fichier produits existe
    if not os.path.exists(FICHIER_PRODUITS):
        print(f"Attention : Le fichier '{FICHIER_PRODUITS}' n'existe pas")
        print(f"Creez ce fichier avec vos produits pour activer la recherche")
        INDEX_RECHERCHE = {}
        PRODUITS_CACHE = []
    else:
        try:
            INDEX_RECHERCHE = creer_index(FICHIER_PRODUITS)
            
            # Charger aussi les produits en cache
            with open(FICHIER_PRODUITS, 'r', encoding='utf-8') as f:
                donnees = yaml.safe_load(f)
                PRODUITS_CACHE = donnees.get('produits', [])
            
            print(f"Index cree avec {len(INDEX_RECHERCHE)} mots-cles")
            print(f"{len(PRODUITS_CACHE)} produits charges depuis {FICHIER_PRODUITS}")
        except Exception as e:
            print(f"Erreur lors de la creation de l'index: {e}")
            INDEX_RECHERCHE = {}
            PRODUITS_CACHE = []
    
    # Lancer le serveur accessible depuis le réseau local
    print("=" * 50)
    print("Serveur web demarre !")
    print("=" * 50)
    print("Acces local : http://localhost:5000")
    print("Acces reseau : http://0.0.0.0:5000")
    print(f"Dossier BDD : {DOSSIER_BDD}/")
    print("=" * 50 + "\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)