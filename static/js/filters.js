/**
 * Client-Side Interactive Filters Module
 */

document.addEventListener('DOMContentLoaded', () => {
    initClientFilters();
});

function initClientFilters() {
    const filterForm = document.getElementById('filter-form');
    if (!filterForm) return;

    // Auto-submit filter form on radio/checkbox change
    const inputs = filterForm.querySelectorAll('input[type="radio"], input[type="checkbox"]');
    inputs.forEach(input => {
        input.addEventListener('change', () => {
            filterForm.submit();
        });
    });
}
