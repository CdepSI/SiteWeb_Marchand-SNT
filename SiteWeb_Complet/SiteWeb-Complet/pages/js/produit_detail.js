// ==========================================
// FONCTIONS DU DÉTAIL PRODUIT
// ==========================================

// ==========================================
// GESTION DES COOKIES
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

                    carte.innerHTML = `
                        <img src="../images/${produit.image}" alt="${produit.nom}">
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
        document.getElementById('historique-produits').innerHTML =
            '<p class="message-info">Historique effacé</p>';
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
// CHARGEMENT DU PRODUIT
// ==========================================

function chargerProduit() {
    // Récupérer l'ID du produit depuis l'URL
    const urlParams = new URLSearchParams(window.location.search);
    const idProduit = urlParams.get('id');

    if (!idProduit) {
        document.getElementById('detail-produit').innerHTML =
            '<p class="message-erreur">Produit non trouvé</p>';
        return;
    }

    // IMPORTANT : Ajouter ce produit à l'historique
    ajouterAHistorique(idProduit);

    // Charger les informations du produit
    fetch('/api/produit/' + idProduit)
        .then(response => response.json())
        .then(produit => {
            if (!produit) {
                throw new Error('Produit non trouvé');
            }

            // Déterminer la classe CSS et le texte selon le stock
            let stockClass = 'stock-normal';
            let stockText = `Stock disponible: ${produit.stock}`;

            if (produit.stock === 0) {
                stockClass = 'stock-epuise';
                stockText = 'Rupture de stock';
            } else if (produit.stock <= 5) {
                stockClass = 'stock-faible';
                stockText = `Stock faible: ${produit.stock} unités restantes`;
            }

            document.getElementById('detail-produit').innerHTML = `
                <div class="produit-detail">
                    <div class="produit-detail-image">
                        <img src="../images/${produit.image}" alt="${produit.nom}">
                    </div>
                    <div class="produit-detail-info">
                        <h2>${produit.nom}</h2>
                        <p class="produit-detail-description">${produit.description}</p>
                        <p class="produit-detail-prix">${produit.prix} €</p>
                        <p class="stock ${stockClass}">${stockText}</p>
                        <div class="produit-detail-actions">
                            <button onclick="ajouterAuPanier('${produit.id}', '${produit.nom}', ${produit.prix})"
                                    class="button" ${produit.stock === 0 ? 'disabled' : ''}>
                                ${produit.stock === 0 ? 'Indisponible' : 'Ajouter au panier'}
                            </button>
                            <a href="produits.html" class="button button-secondary">
                                Retour aux produits
                            </a>
                        </div>
                    </div>
                </div>
            `;

            // Afficher l'historique
            afficherHistorique();
        })
        .catch(error => {
            console.error('Erreur:', error);
            document.getElementById('detail-produit').innerHTML =
                '<p class="message-erreur">Erreur lors du chargement du produit</p>';
        });
}

// Charger le produit au chargement de la page
document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('detail-produit')) {
        chargerProduit();
    }
});