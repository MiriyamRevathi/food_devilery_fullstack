/**
 * Dark Mode Theme Switcher Module
 * Toggles light and dark themes and persists preference in localStorage.
 */

document.addEventListener('DOMContentLoaded', () => {
    initTheme();
});

function initTheme() {
    const themeBtn = document.getElementById('theme-toggle-btn');
    const htmlElement = document.documentElement;

    // Load saved theme or default to light
    const savedTheme = localStorage.getItem('foodflow_theme') || 'light';
    htmlElement.setAttribute('data-theme', savedTheme);

    if (themeBtn) {
        themeBtn.addEventListener('click', () => {
            const currentTheme = htmlElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'light' ? 'dark' : 'light';

            htmlElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('foodflow_theme', newTheme);

            showToast(`Switched to ${newTheme} mode 🌙`, 'info', 2000);
        });
    }
}
