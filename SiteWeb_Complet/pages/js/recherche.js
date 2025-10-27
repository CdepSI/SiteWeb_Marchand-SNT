// ==========================================
// FONCTIONS DE RECHERCHE
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
    // Rediriger vers la page de résultats de recherche
    // Vérifier si on est déjà dans le dossier pages
    const currentPath = window.location.pathname;
    if (currentPath.startsWith('/pages/')) {
        // On est déjà dans pages/, donc utiliser un chemin relatif
        window.location.href = 'recherche.html?q=' + encodeURIComponent(data.terme);
    } else {
        // On est à la racine, donc aller vers pages/
        window.location.href = 'pages/recherche.html?q=' + encodeURIComponent(data.terme);
    }
}

// Afficher l'index (pour comprendre comment fonctionne l'indexation)
function afficherIndex() {
    fetch('/api/recherche/index')
        .then(response => response.json())
        .then(data => {
            let html = '<div style="background: white; padding: 20px; border-radius: 8px; max-width: 800px; margin: 20px auto;">';
            html += '<h2>📚 Index de recherche</h2>';
            html += '<button onclick="window.history.back()" style="margin-top: 20px; padding: 10px 20px; background: #3498db; color: white; border: none; border-radius: 5px; cursor: pointer;">Retour à la page</button>';
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
});