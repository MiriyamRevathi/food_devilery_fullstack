/**
 * Cart Interactivity JavaScript Module
 * Handles AJAX quantity updates, clear cart, and coupon applications.
 */

function updateCartQty(foodId, delta) {
    fetch('/api/cart/update', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ food_id: foodId, delta: delta })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            location.reload();
        }
    });
}

function clearCart() {
    if (confirm("Are you sure you want to clear your cart?")) {
        fetch('/api/cart/clear', { method: 'POST' })
        .then(res => res.json())
        .then(() => location.reload());
    }
}

function applyCoupon() {
    const input = document.getElementById('coupon-code-input');
    if (!input || !input.value) return;

    quickApplyCoupon(input.value);
}

function quickApplyCoupon(code) {
    fetch('/api/cart/coupon', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code: code, action: 'apply' })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            showToast(data.message, 'success');
            setTimeout(() => location.reload(), 800);
        } else {
            showToast(data.message, 'danger');
        }
    });
}

function removeCoupon() {
    fetch('/api/cart/coupon', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action: 'remove' })
    })
    .then(res => res.json())
    .then(data => {
        showToast(data.message, 'info');
        setTimeout(() => location.reload(), 500);
    });
}
