/**
 * Desktop & In-App Push Notification Alert Drawer Module
 */

function showInAppAlert(title, message, type = 'info') {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const alertBox = document.createElement('div');
    alertBox.className = `toast-item toast-${type} pulse-glow`;
    alertBox.innerHTML = `
        <div class="toast-content">
            <strong class="d-block">${title}</strong>
            <span>${message}</span>
        </div>
        <button type="button" onclick="this.parentElement.remove()" class="toast-close">&times;</button>
    `;

    container.appendChild(alertBox);

    setTimeout(() => {
        if (alertBox.parentElement) {
            alertBox.remove();
        }
    }, 4000);
}
