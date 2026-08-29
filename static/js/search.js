/**
 * Live Search & Auto-suggestions Module
 */

document.addEventListener('DOMContentLoaded', () => {
    initLiveSearch();
});

function initLiveSearch() {
    const inputs = document.querySelectorAll('.navbar-search-input');

    inputs.forEach(input => {
        const wrapper = input.closest('.search-input-wrapper');
        if (!wrapper) return;

        // Create auto-suggestions dropdown element
        const dropdown = document.createElement('div');
        dropdown.className = 'search-suggestions-dropdown';
        wrapper.appendChild(dropdown);

        input.addEventListener('input', (e) => {
            const val = e.target.value.trim().toLowerCase();
            if (val.length < 2) {
                dropdown.style.display = 'none';
                return;
            }

            // Fetch search results from client page or static items
            dropdown.innerHTML = `
                <div class="suggestion-item" onclick="window.location.href='/search?q=${encodeURIComponent(val)}'">
                    <span>🔍 Search for "<strong>${val}</strong>"</span>
                </div>
                <div class="suggestion-item" onclick="window.location.href='/search?q=Biryani'">
                    <span>🍚 Quick suggestion: <strong>Biryani</strong></span>
                </div>
                <div class="suggestion-item" onclick="window.location.href='/search?q=Pizza'">
                    <span>🍕 Quick suggestion: <strong>Margherita Pizza</strong></span>
                </div>
            `;
            dropdown.style.display = 'block';
        });

        document.addEventListener('click', (e) => {
            if (!wrapper.contains(e.target)) {
                dropdown.style.display = 'none';
            }
        });
    });
}
