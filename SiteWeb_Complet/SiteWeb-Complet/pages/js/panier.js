// ==========================================
// FONCTIONS DU PANIER
// ==========================================

// Chargement du panier
function chargerPanier() {
    fetch('/api/panier')
        .then(response => response.json())
        .then(data => {
            const conteneur = document.getElementById('contenu-panier');

            if (data.articles.length === 0) {
                conteneur.innerHTML = '<p class="panier-vide">Votre panier est vide.</p>';
                document.getElementById('montant-total').textContent = '0';
                return;
            }

            let html = '<table class="tableau-panier">';
            html += '<tr><th>Produit</th><th>Prix unitaire</th><th>Quantité</th><th>Total</th><th>Action</th></tr>';

            data.articles.forEach(article => {
                html += `
                    <tr>
                        <td>${article.nom}</td>
                        <td>${article.prix} €</td>
                        <td>${article.quantite}</td>
                        <td>${(article.prix * article.quantite).toFixed(2)} €</td>
                        <td>
                            <button onclick="retirerDuPanier('${article.id}')" class="button-small">
                                Retirer
                            </button>
                        </td>
                    </tr>
                `;
            });

            html += '</table>';
            conteneur.innerHTML = html;
            document.getElementById('montant-total').textContent = data.total.toFixed(2);
        })
        .catch(error => {
            console.error('Erreur:', error);
            document.getElementById('contenu-panier').innerHTML =
                '<p>Erreur lors du chargement du panier.</p>';
        });
}

// Retirer un article du panier
function retirerDuPanier(id) {
    fetch('/api/panier/retirer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ id: id })
    })
    .then(() => {
        chargerPanier();
    })
    .catch(error => console.error('Erreur:', error));
}

// Vider le panier
function viderPanier() {
    if (confirm('Voulez-vous vraiment vider le panier ?')) {
        fetch('/api/panier/vider', { method: 'POST' })
            .then(() => {
                chargerPanier();
            })
            .catch(error => console.error('Erreur:', error));
    }
}

// Valider la commande
function validerCommande() {
    alert('Commande validée ! (Fonctionnalité à développer)');
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

// Charger le panier au chargement de la page
document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('contenu-panier')) {
        chargerPanier();
    }
});