// ==========================================
// FONCTIONS D'INSCRIPTION
// ==========================================

// Fonction d'inscription
function inscrire(event) {
    event.preventDefault();

    const formulaire = document.getElementById('formulaire-inscription');
    const donnees = {
        prenom: formulaire.prenom.value,
        nom: formulaire.nom.value,
        email: formulaire.email.value,
        ville: formulaire.ville.value,
        age: parseInt(formulaire.age.value)
    };

    fetch('/api/clients/ajouter', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(donnees)
    })
    .then(response => response.json())
    .then(data => {
        const messageDiv = document.getElementById('message');
        messageDiv.className = 'message message-succes';
        messageDiv.textContent = '✓ Inscription réussie !';
        formulaire.reset();
        chargerClients();
    })
    .catch(error => {
        const messageDiv = document.getElementById('message');
        messageDiv.className = 'message message-erreur';
        messageDiv.textContent = '✗ Erreur lors de l\'inscription';
        console.error('Erreur:', error);
    });
}

// Charger la liste des clients
function chargerClients() {
    fetch('/api/clients')
        .then(response => response.json())
        .then(clients => {
            const conteneur = document.getElementById('clients-liste');

            if (clients.length === 0) {
                conteneur.innerHTML = '<p>Aucun client inscrit.</p>';
                return;
            }

            let html = '<table class="tableau-clients">';
            html += '<tr><th>Prénom</th><th>Nom</th><th>Email</th><th>Ville</th><th>Âge</th></tr>';

            clients.forEach(client => {
                html += `
                    <tr>
                        <td>${client.prenom}</td>
                        <td>${client.nom}</td>
                        <td>${client.email}</td>
                        <td>${client.ville}</td>
                        <td>${client.age}</td>
                    </tr>
                `;
            });

            html += '</table>';
            conteneur.innerHTML = html;
        })
        .catch(error => {
            console.error('Erreur:', error);
        });
}

// Charger les clients au chargement de la page
document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('clients-liste')) {
        chargerClients();
    }
});