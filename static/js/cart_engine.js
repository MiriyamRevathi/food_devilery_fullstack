/**
 * Advanced Client-Side Cart Engine & LocalStorage Manager
 */

class FoodFlowCartEngine {
    constructor() {
        this.storageKey = 'foodflow_local_cart';
        this.cart = this.loadCart();
    }

    loadCart() {
        try {
            const data = localStorage.getItem(this.storageKey);
            return data ? JSON.parse(data) : [];
        } catch (e) {
            return [];
        }
    }

    saveCart() {
        try {
            localStorage.setItem(this.storageKey, JSON.stringify(this.cart));
            this.updateBadge();
        } catch (e) {}
    }

    addItem(foodItem) {
        const existing = this.cart.find(i => i.food_id === foodItem.food_id && i.variant === foodItem.variant);
        if (existing) {
            existing.quantity += foodItem.quantity || 1;
        } else {
            this.cart.push(foodItem);
        }
        this.saveCart();
    }

    removeItem(foodId) {
        this.cart = this.cart.filter(i => i.food_id !== foodId);
        this.saveCart();
    }

    clearCart() {
        this.cart = [];
        this.saveCart();
    }

    updateBadge() {
        const badge = document.getElementById('cart-badge-count');
        if (badge) {
            const totalCount = this.cart.reduce((sum, item) => sum + (item.quantity || 1), 0);
            badge.textContent = totalCount;
        }
    }
}

const globalCartEngine = new FoodFlowCartEngine();
