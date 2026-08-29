/**
 * FoodFlow — Main JavaScript Module
 * Initializes global UI features, dynamic toast notifications, and user menu dropdowns.
 */

document.addEventListener('DOMContentLoaded', () => {
    initUserDropdown();
});

/**
 * Display a dynamic toast notification popup.
 * @param {string} message - The message content.
 * @param {string} type - Toast style type ('success', 'warning', 'danger', 'info').
 * @param {number} duration - Auto-dismiss duration in milliseconds.
 */
function showToast(message, type = 'success', duration = 3500) {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = `toast-item toast-${type}`;
    
    let icon = '🔔';
    if (type === 'success') icon = '✅';
    if (type === 'warning') icon = '⚠️';
    if (type === 'danger') icon = '❌';

    toast.innerHTML = `
        <span>${icon} ${message}</span>
        <button onclick="this.parentElement.remove()" style="background:none;border:none;color:#fff;cursor:pointer;">&times;</button>
    `;

    container.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(100%)';
        toast.style.transition = 'all 0.3s ease-out';
        setTimeout(() => toast.remove(), 300);
    }, duration);
}

/**
 * Handle user dropdown avatar menu toggle.
 */
function initUserDropdown() {
    const btn = document.getElementById('user-menu-btn');
    const menu = document.getElementById('user-dropdown-menu');

    if (btn && menu) {
        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            menu.classList.toggle('show');
        });

        document.addEventListener('click', () => {
            menu.classList.remove('show');
        });
    }
}
