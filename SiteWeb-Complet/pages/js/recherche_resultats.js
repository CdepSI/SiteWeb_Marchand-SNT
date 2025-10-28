// ==========================================
// FONCTIONS DE LA PAGE DE RÉSULTATS DE RECHERCHE
// ==========================================

// Fonction de recherche (appelle l'API Python)
function rechercher() {
    const terme = document.getElementById('input-recherche').value;

    if (terme.trim() === '') {
        alert('Veuillez entrer un terme de recherche');
        return;
    }

    fetch('/api/recherche?terme=' + encodeURIComponent(terme))
        .then(response => response.json())
        .then(data => {
            afficherResultats(data);
        })
        .catch(error => {
            console.error('Erreur:', error);
            alert('Erreur lors de la recherche');
        });
}

// Afficher les résultats de recherche
function afficherResultats(data) {
    const conteneur = document.getElementById('resultats-recherche');
    conteneur.innerHTML = '';

    if (data.resultats.length === 0) {
        conteneur.innerHTML = `
            <div style="text-align: center; padding: 40px;">
                <h3>Aucun résultat trouvé pour "${data.terme}"</h3>
                <p>Essayez avec d'autres mots-clés</p>
                <a href="produits.html" class="button">Voir tous les produits</a>
            </div>
        `;
        return;
    }

    conteneur.innerHTML = `
        <div style="background: #e3f2fd; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
            <p><strong>${data.resultats.length} résultat(s)</strong> trouvé(s) pour "<strong>${data.terme}</strong>"</p>
            <p style="font-size: 0.9em; color: #555;">
                Temps de recherche : ${data.temps_recherche} secondes<br>
                Mots-clés utilisés dans l'index : ${data.mots_recherches.join(', ')}
            </p>
        </div>
    `;

    // Créer la grille de produits
    const grilleProduits = document.createElement('div');
    grilleProduits.className = 'produits-grid';

    data.resultats.forEach(produit => {
        const carte = document.createElement('div');
        carte.className = 'produit-carte';

        // Mettre en évidence les mots recherchés
        let nomAffiche = produit.nom;
        let descriptionAffichee = produit.description;

        data.mots_recherches.forEach(mot => {
            const regex = new RegExp(mot, 'gi');
            nomAffiche = nomAffiche.replace(regex, '<mark>$&</mark>');
            descriptionAffichee = descriptionAffichee.replace(regex, '<mark>$&</mark>');
        });

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
            <h3>${nomAffiche}</h3>
            <p class="description">${descriptionAffichee}</p>
            <p class="prix">${produit.prix} €</p>
            <p class="stock ${stockClass}">${stockText}</p>
            <a href="produit_detail.html?id=${produit.id}" class="button button-small">
                Voir le détail
            </a>
            <button onclick="ajouterAuPanier('${produit.id}', '${produit.nom}', ${produit.prix})" ${produit.stock === 0 ? 'disabled' : ''}>
                ${produit.stock === 0 ? 'Indisponible' : 'Ajouter au panier'}
            </button>
        `;

        grilleProduits.appendChild(carte);
    });

    conteneur.appendChild(grilleProduits);
}

// Afficher l'index (pour comprendre comment fonctionne l'indexation)
function afficherIndex() {
    fetch('/api/recherche/index')
        .then(response => response.json())
        .then(data => {
            let html = '<div style="background: white; padding: 20px; border-radius: 8px; max-width: 800px; margin: 20px auto;">';
            html += '<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">';
            html += '<h2 style="margin: 0;">📚 Index de recherche</h2>';
            html += '<button onclick="location.reload()" style="padding: 10px 20px; background: #3498db; color: white; border: none; border-radius: 5px; cursor: pointer;">Retour aux résultats</button>';
            html += '</div>';
            html += '<p><em>Cet index permet de retrouver rapidement les produits contenant un mot-clé</em></p>';
            html += '<table class="tableau-index" style="width: 100%; border-collapse: collapse; margin-top: 20px;">';
            html += '<tr style="background: #34495e; color: white;"><th style="padding: 10px; text-align: left;">Mot-clé</th><th style="padding: 10px; text-align: left;">Produits contenant ce mot</th></tr>';

            for (const [mot, produits] of Object.entries(data.index)) {
                html += `<tr style="border-bottom: 1px solid #ddd;">`;
                html += `<td style="padding: 10px;"><strong>${mot}</strong></td>`;
                html += `<td style="padding: 10px;">${produits.join(', ')}</td>`;
                html += `</tr>`;
            }

            html += '</table>';
            html += '</div>';

            document.querySelector('main').innerHTML = html;
        })
        .catch(error => {
            console.error('Erreur:', error);
        });
}

// Fonction pour ajouter un produit au panier
function ajouterAuPanier(id, nom, prix) {
    fetch('/api/panier/ajouter', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            id: id,
            nom: nom,
            prix: prix,
            quantite: 1
        })
    })
    .then(response => response.json())
    .then(data => {
        alert('✓ ' + nom + ' ajouté au panier !');
    })
    .catch(error => {
        console.error('Erreur:', error);
        alert('Erreur lors de l\'ajout au panier');
    });
}

// Recherche en temps réel (optionnel)
document.addEventListener('DOMContentLoaded', function() {
    const inputRecherche = document.getElementById('input-recherche');
    if (inputRecherche) {
        inputRecherche.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                rechercher();
            }
        });
    }

    // Charger les résultats depuis l'URL si présents
    const urlParams = new URLSearchParams(window.location.search);
    const terme = urlParams.get('q');
    if (terme) {
        document.getElementById('input-recherche').value = terme;
        rechercher();
    }
});