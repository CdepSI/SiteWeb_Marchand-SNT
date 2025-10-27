// ==========================================
// GESTION DES COOKIES - PARTAGÉ ENTRE LES PAGES
// ==========================================

/**
 * Fonction pour créer un cookie
 * Un cookie est une petite information stockée dans le navigateur
 */
function creerCookie(nom, valeur, joursExpiration) {
    // Calculer la date d'expiration
    const date = new Date();
    date.setTime(date.getTime() + (joursExpiration * 24 * 60 * 60 * 1000));
    const expiration = "expires=" + date.toUTCString();

    // Créer le cookie
    document.cookie = nom + "=" + valeur + ";" + expiration + ";path=/";

    console.log("🍪 Cookie créé :", nom, "=", valeur);
}

/**
 * Fonction pour lire un cookie
 */
function lireCookie(nom) {
    const nomCookie = nom + "=";
    const cookies = document.cookie.split(';');

    for (let i = 0; i < cookies.length; i++) {
        let cookie = cookies[i];
        // Enlever les espaces au début
        while (cookie.charAt(0) === ' ') {
            cookie = cookie.substring(1);
        }
        // Si c'est le bon cookie, retourner sa valeur
        if (cookie.indexOf(nomCookie) === 0) {
            return cookie.substring(nomCookie.length, cookie.length);
        }
    }
    return "";
}

/**
 * Fonction pour supprimer un cookie
 */
function supprimerCookie(nom) {
    // Pour supprimer un cookie, on le fait expirer dans le passé
    document.cookie = nom + "=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    console.log("🗑️ Cookie supprimé :", nom);
}

// ==========================================
// GESTION DE L'HISTORIQUE DES PRODUITS
// ==========================================

/**
 * Ajouter un produit à l'historique (dans le cookie)
 */
function ajouterAHistorique(idProduit) {
    // Lire l'historique actuel depuis le cookie
    let historique = lireCookie('historique_produits');

    // Si le cookie est vide, créer une liste vide
    let listeProduits = [];
    if (historique !== "") {
        // Convertir la chaîne de texte en liste
        listeProduits = historique.split(',');
    }

    // Retirer le produit s'il existe déjà (pour le mettre en premier)
    listeProduits = listeProduits.filter(id => id !== idProduit);

    // Ajouter le nouveau produit au début de la liste
    listeProduits.unshift(idProduit);

    // Garder seulement les 5 derniers produits
    if (listeProduits.length > 5) {
        listeProduits = listeProduits.slice(0, 5);
    }

    // Convertir la liste en chaîne de texte
    const nouvelHistorique = listeProduits.join(',');

    // Sauvegarder dans le cookie (expire dans 30 jours)
    creerCookie('historique_produits', nouvelHistorique, 30);

    console.log("📝 Historique mis à jour :", listeProduits);
}

/**
 * Récupérer l'historique depuis le cookie
 */
function recupererHistorique() {
    const historique = lireCookie('historique_produits');

    if (historique === "") {
        return [];
    }

    return historique.split(',');
}

/**
 * Afficher les produits de l'historique
 */
function afficherHistorique() {
    const historique = recupererHistorique();
    const conteneur = document.getElementById('historique-produits');

    if (!conteneur) {
        return; // Si le conteneur n'existe pas sur cette page, ne rien faire
    }

    if (historique.length === 0) {
        conteneur.innerHTML = '<p class="message-info">Aucun produit consulté récemment</p>';
        return;
    }

    // Charger les informations des produits depuis l'API
    fetch('/api/produits')
        .then(response => response.json())
        .then(tousProduits => {
            conteneur.innerHTML = '';

            historique.forEach(idProduit => {
                // Trouver le produit correspondant
                const produit = tousProduits.find(p => p.id === idProduit);

                if (produit) {
                    const carte = document.createElement('div');
                    carte.className = 'produit-carte produit-historique';

                    // Déterminer le chemin de l'image selon la page actuelle
                    const cheminImage = window.location.pathname.includes('/pages/') ? '../images/' : 'images/';

                    carte.innerHTML = `
                        <img src="${cheminImage}${produit.image}" alt="${produit.nom}">
                        <h3>${produit.nom}</h3>
                        <p class="prix">${produit.prix} €</p>
                        <a href="produit_detail.html?id=${produit.id}" class="button button-small">
                            Voir à nouveau
                        </a>
                    `;

                    conteneur.appendChild(carte);
                }
            });
        })
        .catch(error => {
            console.error('Erreur:', error);
        });
}

/**
 * Supprimer l'historique
 */
function supprimerHistorique() {
    if (confirm('Voulez-vous vraiment effacer votre historique de consultation ?')) {
        supprimerCookie('historique_produits');
        const conteneur = document.getElementById('historique-produits');
        if (conteneur) {
            conteneur.innerHTML = '<p class="message-info">Historique effacé</p>';
        }
        alert('✓ Historique effacé !');
    }
}

/**
 * Afficher tous les cookies (pédagogique)
 */
function afficherCookies() {
    const tousLesCookies = document.cookie;

    if (tousLesCookies === "") {
        alert('Aucun cookie enregistré');
        return;
    }

    const listeCookies = tousLesCookies.split(';');
    let message = '🍪 COOKIES ENREGISTRÉS :\n\n';

    listeCookies.forEach(cookie => {
        const [nom, valeur] = cookie.split('=');
        message += `${nom.trim()} = ${valeur}\n`;
    });

    message += '\n💡 Ces informations sont stockées dans votre navigateur';
    alert(message);
}

// ==========================================
// INITIALISATION
// ==========================================

// Afficher l'historique au chargement de la page (si le conteneur existe)
document.addEventListener('DOMContentLoaded', function() {
    afficherHistorique();
});