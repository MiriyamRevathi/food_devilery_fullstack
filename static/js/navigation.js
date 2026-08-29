/**
 * Navigation JavaScript Module
 * Handles mobile hamburger drawer menu and header sticky scroll shadow.
 */

document.addEventListener('DOMContentLoaded', () => {
    initMobileNav();
    initStickyHeader();
});

function initMobileNav() {
    const toggleBtn = document.getElementById('mobile-menu-toggle');
    const navMenu = document.querySelector('.navbar-nav');

    if (toggleBtn && navMenu) {
        toggleBtn.addEventListener('click', () => {
            navMenu.classList.toggle('mobile-active');
        });
    }
}

function initStickyHeader() {
    const navbar = document.getElementById('navbar');
    if (!navbar) return;

    window.addEventListener('scroll', () => {
        if (window.scrollY > 20) {
            navbar.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.12)';
        } else {
            navbar.style.boxShadow = 'var(--shadow-sm)';
        }
    });
}
