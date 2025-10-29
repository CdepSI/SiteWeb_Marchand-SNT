// ==========================================
// FONCTIONS DES PRODUITS
// ==========================================

// Chargement des produits depuis l'API Python
function chargerProduits() {
    fetch('/api/produits')
        .then(response => response.json())
        .then(produits => {
            const conteneur = document.getElementById('liste-produits');

            produits.forEach(produit => {
                const carte = document.createElement('div');
                carte.className = 'produit-carte';

                // Déterminer la classe CSS selon le stock
                let stockClass = 'stock-normal';
                let stockText = `Stock: ${produit.stock}`;

                if (produit.stock === 0) {
                    stockClass = 'stock-epuise';
                    stockText = 'Rupture de stock';
                } else if (produit.stock <= 5) {
                    stockClass = 'stock-faible';
                    stockText = `Stock faible: ${produit.stock}`;
                }

                carte.innerHTML = `
                    <img src="../images/${produit.image}" alt="${produit.nom}">
                    <h3>${produit.nom}</h3>
                    <p class="description">${produit.description}</p>
                    <p class="prix">${produit.prix} €</p>
                    <p class="stock ${stockClass}">${stockText}</p>
                    <a href="produit_detail.html?id=${produit.id}" class="button button-small">
                        Voir le détail
                    </a>
                    <button onclick="ajouterAuPanier('${produit.id}', '${produit.nom}', ${produit.prix})" ${produit.stock === 0 ? 'disabled' : ''}>
                        ${produit.stock === 0 ? 'Indisponible' : 'Ajouter au panier'}
                    </button>
                `;

                conteneur.appendChild(carte);
            });
        })
        .catch(error => {
            console.error('Erreur:', error);
            const conteneur = document.getElementById('liste-produits');
            if (conteneur) {
                conteneur.innerHTML = '<p>Erreur lors du chargement des produits.</p>';
            }
        });
}

// Charger les produits au chargement de la page
document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('liste-produits')) {
        chargerProduits();
    }
});