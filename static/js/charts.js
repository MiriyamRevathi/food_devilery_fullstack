/**
 * Pure JavaScript Chart Renderer Module
 * Renders custom CSS/HTML bar charts without external chart libraries.
 */

function renderBarChart(containerId, dataSeries) {
    const container = document.getElementById(containerId);
    if (!container || !dataSeries) return;

    const maxVal = Math.max(...dataSeries.map(d => d.value), 1);

    container.innerHTML = '';
    dataSeries.forEach(item => {
        const heightPct = (item.value / maxVal) * 100;
        
        const col = document.createElement('div');
        col.className = 'chart-bar-col';
        col.innerHTML = `
            <div class="bar" style="height: ${heightPct}%;" title="${item.label}: ${item.value}"></div>
            <small>${item.label}</small>
        `;
        container.appendChild(col);
    });
}
