/**
 * FoodFlow — Main JavaScript Module
 * Handles UI interactions, toast notifications, user menu dropdowns, modals, and coupon copy helpers.
 */

document.addEventListener('DOMContentLoaded', () => {
    initUserDropdown();
    initLocationModal();
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

    toast.innerHTML = `
        <span>${message}</span>
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

        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                menu.classList.remove('show');
            }
        });
    }
}

/**
 * Handle Location Selector Modal toggle cleanly without display artifacts.
 */
function initLocationModal() {
    const pill = document.querySelector('.location-pill');
    const modal = document.getElementById('locationModal');
    if (!modal) return;

    if (pill) {
        pill.addEventListener('click', () => {
            modal.style.display = 'block';
            modal.classList.add('show');
        });
    }

    const closeBtns = modal.querySelectorAll('[data-bs-dismiss="modal"], .btn-close');
    closeBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            modal.style.display = 'none';
            modal.classList.remove('show');
        });
    });

    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.style.display = 'none';
            modal.classList.remove('show');
        }
    });

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && modal.classList.contains('show')) {
            modal.style.display = 'none';
            modal.classList.remove('show');
        }
    });
}

/**
 * Copy promo coupon code to clipboard with toast notification.
 * @param {string} code - The promo coupon code string.
 */
function copyCouponCode(code) {
    if (!code) return;
    navigator.clipboard.writeText(code).then(() => {
        showToast(`Coupon code ${code} copied to clipboard!`, 'success');
    }).catch(() => {
        showToast(`Coupon code: ${code}`, 'info');
    });
}
