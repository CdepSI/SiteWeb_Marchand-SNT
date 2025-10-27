// ==========================================
// GESTION DU MENU HAMBURGER RESPONSIVE
// ==========================================

/**
 * Fonction pour basculer l'affichage du menu mobile
 * Ajoute ou retire la classe 'open' au menu de navigation
 */
function toggleMenu() {
    const nav = document.getElementById('main-nav');
    if (nav) {
        nav.classList.toggle('open');
    }
}

/**
 * Fonction d'initialisation du menu mobile
 * Configure les événements pour fermer le menu automatiquement
 */
function initMenu() {
    // Fermer le menu quand on clique sur un lien de navigation
    const navLinks = document.querySelectorAll('#main-nav a');
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            const nav = document.getElementById('main-nav');
            if (nav) {
                nav.classList.remove('open');
            }
        });
    });

    // Fermer le menu si on clique en dehors (optionnel)
    document.addEventListener('click', function(event) {
        const nav = document.getElementById('main-nav');
        const menuToggle = document.querySelector('.menu-toggle');

        // Vérifier si le clic est en dehors du menu et du bouton
        if (nav && nav.classList.contains('open') &&
            !nav.contains(event.target) &&
            !menuToggle.contains(event.target)) {
            nav.classList.remove('open');
        }
    });
}

// Initialiser le menu quand le DOM est chargé
document.addEventListener('DOMContentLoaded', initMenu);